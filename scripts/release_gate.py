#!/usr/bin/env python3
"""Deterministic release gate for the Codex-first Git workflow."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_CASE_FIELDS = {"id", "phase", "risk", "evidence", "prompt", "criteria", "forbidden"}
ALLOWED_RISKS = {"low", "medium", "high"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_catalog(errors: list[str]) -> None:
    path = ROOT / "evals" / "git-workflow.jsonl"
    seen: set[str] = set()
    phases: set[str] = set()
    high_risk = 0
    count = 0
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        count += 1
        try:
            case = json.loads(raw)
        except json.JSONDecodeError as error:
            errors.append(f"eval line {number}: {error}")
            continue
        missing = REQUIRED_CASE_FIELDS - set(case)
        if missing:
            errors.append(f"eval line {number}: missing {sorted(missing)}")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"eval line {number}: invalid id")
        elif case_id in seen:
            errors.append(f"eval line {number}: duplicate id {case_id}")
        else:
            seen.add(case_id)
        phases.add(case.get("phase", ""))
        if case.get("risk") not in ALLOWED_RISKS:
            errors.append(f"eval line {number}: invalid risk")
        if case.get("risk") == "high":
            high_risk += 1
        if not 2 <= len(case.get("criteria", [])) <= 5:
            errors.append(f"eval line {number}: criteria must contain 2-5 items")
        if not case.get("forbidden"):
            errors.append(f"eval line {number}: forbidden must not be empty")
    required_phases = {"branch", "commit", "checks", "sync", "request", "ci", "merge", "release", "policy"}
    if count < 10:
        errors.append("evaluation catalog must contain at least 10 cases")
    if high_risk < 4:
        errors.append("evaluation catalog must contain at least 4 high-risk cases")
    if missing := required_phases - phases:
        errors.append(f"evaluation catalog is missing phases {sorted(missing)}")


def validate_distribution(errors: list[str]) -> None:
    marketplace = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    entries = marketplace.get("plugins", [])
    if len(entries) != 1:
        errors.append("Codex marketplace must publish exactly one plugin")
    for entry in entries:
        name = entry.get("name")
        source = entry.get("source", {}).get("path", "")
        plugin = (ROOT / ".agents" / "plugins" / source).resolve()
        manifest_path = plugin / ".codex-plugin" / "plugin.json"
        if not manifest_path.exists():
            errors.append(f"{name}: missing Codex manifest")
            continue
        manifest = load_json(manifest_path)
        if manifest.get("name") != name:
            errors.append(f"{name}: marketplace and manifest names differ")
        if not (plugin / "skills").is_dir():
            errors.append(f"{name}: missing shared skills directory")
        policy = entry.get("policy", {})
        if policy.get("installation") not in {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}:
            errors.append(f"{name}: invalid installation policy")
        if policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
            errors.append(f"{name}: invalid authentication policy")


def validate_single_skill(errors: list[str]) -> None:
    skill = ROOT / "skills" / "git-workflow" / "SKILL.md"
    skills = list(ROOT.glob("**/SKILL.md"))
    if skills != [skill]:
        errors.append(f"repository must contain exactly one Skill, found {len(skills)}")
    if not skill.exists():
        return
    content = skill.read_text(encoding="utf-8")
    if not content.startswith("---\nname: git-workflow\ndescription:"):
        errors.append("git-workflow: invalid Skill frontmatter")
    if "explicit user request" not in content or "repository-local" not in content or "## Safety boundaries" not in content:
        errors.append("git-workflow: conflict precedence is incomplete")


def validate_fast_path(errors: list[str]) -> None:
    commands = {
        "commit-push": ROOT / "commands" / "commit-push.md",
        "commit-push-mr": ROOT / "commands" / "commit-push-mr.md",
    }
    for name, command in commands.items():
        if not command.exists():
            errors.append(f"missing commands/{name}.md")
            continue
        content = command.read_text(encoding="utf-8")
        if content.count("!`") > 2:
            errors.append(f"{name}: more than two eager context calls")
        for forbidden in ("git fetch", "release_gate.py", "git_context.py", "--fill"):
            if forbidden in content:
                errors.append(f"{name}: slow-path operation present: {forbidden}")

    budget_path = ROOT / "evals" / "performance-budget.json"
    if not budget_path.exists():
        errors.append("missing performance budget")
        return
    budget = load_json(budget_path)
    scenarios = {item.get("id"): item for item in budget.get("scenarios", [])}
    required = {"native-push", "commit-push", "commit-push-mr"}
    for scenario_id in required:
        scenario = scenarios.get(scenario_id)
        if not scenario:
            errors.append(f"performance budget missing {scenario_id}")
        elif scenario.get("candidate_status") not in {"pending", "measured"}:
            errors.append(f"{scenario_id}: invalid candidate status")


def run(command: list[str]) -> int:
    print(f"+ {' '.join(command)}")
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def main() -> int:
    errors: list[str] = []
    validate_catalog(errors)
    validate_distribution(errors)
    validate_single_skill(errors)
    validate_fast_path(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]):
        return 1
    print("Release gate passed: distribution, policy, scenarios, lint, and tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
