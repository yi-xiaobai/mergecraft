from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "git_context.py"


class GitContextTest(unittest.TestCase):
    def git(self, repo: Path, *args: str) -> None:
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)

    def test_reports_dirty_untracked_sensitive_path_without_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.git(repo, "init")
            self.git(repo, "config", "user.name", "Test")
            self.git(repo, "config", "user.email", "test@example.com")
            (repo / "README.md").write_text("ok\n", encoding="utf-8")
            self.git(repo, "add", "README.md")
            self.git(repo, "commit", "-m", "docs: initialize")
            (repo / ".env").write_text("TOKEN=do-not-print\n", encoding="utf-8")
            result = subprocess.run(
                ["python3", str(SCRIPT), "--repo", str(repo)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertNotIn("do-not-print", result.stdout)
            data = json.loads(result.stdout)
            self.assertTrue(data["dirty"])
            self.assertEqual(data["sensitive_paths"], [".env"])
            self.assertTrue(data["stop_reasons"])

    def test_preserves_worktree_status_columns_for_modified_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.git(repo, "init")
            self.git(repo, "config", "user.name", "Test")
            self.git(repo, "config", "user.email", "test@example.com")
            tracked = repo / ".config"
            tracked.write_text("before\n", encoding="utf-8")
            self.git(repo, "add", ".config")
            self.git(repo, "commit", "-m", "chore: initialize")
            tracked.write_text("after\n", encoding="utf-8")
            result = subprocess.run(
                ["python3", str(SCRIPT), "--repo", str(repo)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(json.loads(result.stdout)["changes"], [{"code": " M", "path": ".config"}])


class WorkflowContractTest(unittest.TestCase):
    def test_failure_evidence_commits_exist(self) -> None:
        catalog = (ROOT / "evals/git-workflow.jsonl").read_text(encoding="utf-8")
        for commit in ("393b3df", "e5f5879", "0335bba", "f41ba8a", "9f334f2"):
            self.assertIn(commit, catalog)
            result = subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=ROOT)
            self.assertEqual(result.returncode, 0)

    def test_repository_contains_one_team_rules_skill(self) -> None:
        skills = list(ROOT.glob("**/SKILL.md"))
        self.assertEqual(skills, [ROOT / "skills/git-workflow/SKILL.md"])

    def test_skill_adds_rules_without_reimplementing_git(self) -> None:
        skill = (ROOT / "skills/git-workflow/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Use the model's native Git capabilities for ordinary operations", skill)
        self.assertNotIn("/commit-push", skill)

    def test_fast_delivery_command_has_bounded_context_and_explicit_mr_defaults(self) -> None:
        command = (ROOT / "commands/commit-push-mr.md").read_text(encoding="utf-8")
        self.assertLessEqual(command.count("!`"), 2)
        self.assertIn("Apply the `git-workflow` Skill", command)
        for option in (
            "--title",
            "--description",
            "--squash-before-merge=true",
            "--remove-source-branch=true",
            "--assignee=@me",
        ):
            self.assertIn(option, command)
        for forbidden in ("git fetch", "release_gate.py", "git_context.py", "--fill"):
            self.assertNotIn(forbidden, command)

    def test_commit_push_command_delegates_policy_without_creating_mr(self) -> None:
        command = (ROOT / "commands/commit-push.md").read_text(encoding="utf-8")
        self.assertLessEqual(command.count("!`"), 2)
        self.assertIn("Apply the `git-workflow` Skill", command)
        self.assertIn("pre-commit", command)
        for forbidden in ("glab", "git fetch", "release_gate.py", "git_context.py"):
            self.assertNotIn(forbidden, command)

    def test_repository_has_only_the_two_delivery_commands(self) -> None:
        commands = sorted(path.name for path in (ROOT / "commands").glob("*.md"))
        self.assertEqual(commands, ["commit-push-mr.md", "commit-push.md"])

    def test_performance_budget_covers_native_push_and_fast_delivery(self) -> None:
        budget = json.loads((ROOT / "evals/performance-budget.json").read_text(encoding="utf-8"))
        scenarios = {item["id"]: item for item in budget["scenarios"]}
        self.assertEqual(set(scenarios), {"native-push", "commit-push", "commit-push-mr"})
        self.assertEqual(scenarios["commit-push"]["candidate_status"], "pending")
        self.assertEqual(scenarios["commit-push-mr"]["observed_baseline_seconds"], 20)
        self.assertEqual(scenarios["commit-push-mr"]["candidate_status"], "pending")


if __name__ == "__main__":
    unittest.main()
