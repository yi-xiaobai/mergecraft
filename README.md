# MergeCraft

A shared Claude Code and Codex plugin containing one self-contained Skill for
safe, end-to-end Git delivery.

## Structure

```text
.
├── .agents/plugins/marketplace.json
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
├── .github/workflows/validate.yml
├── evals/
├── scripts/
├── skills/git-workflow/SKILL.md
└── tests/
```

There are no nested plugin packages, slash commands, or specialist agents. GitHub
and GitLab behavior lives in the same Skill so both agents use one source of
truth.

## Install in Claude Code

```bash
claude plugin marketplace add yi-xiaobai/mergecraft
claude plugin install git-workflow@mergecraft
```

## Install in Codex

```bash
codex plugin marketplace add ./.agents/plugins
codex plugin add git-workflow@mergecraft
```

Start a new Codex thread after installation so the Skill is discovered.

## Validate

```bash
python3 scripts/git_context.py
python3 scripts/release_gate.py
```

The release gate verifies the single-Skill structure, Codex distribution,
failure-driven scenario catalog, and automated tests. Passing deterministic
checks is necessary but not sufficient: model scenarios must also beat baseline
without a blocking safety finding before publication.
