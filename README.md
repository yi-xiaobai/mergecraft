# MergeCraft

A shared Claude Code and Codex plugin that separates team Git rules from a
bounded Claude Code delivery command.

## Structure

```text
.
├── .agents/plugins/marketplace.json
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
├── .github/workflows/validate.yml
├── commands/
│   ├── commit-push.md
│   └── commit-push-mr.md
├── evals/
├── scripts/
├── skills/git-workflow/SKILL.md
└── tests/
```

Ordinary Git mechanics remain model-native, with the Skill supplying team
conventions and safety boundaries. Claude Code users can invoke `/commit-push`
for a pre-commit-aware push boundary or `/commit-push-mr` for the complete
cross-system workflow. Codex applies the same Skill to explicit delivery tasks.

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

The release gate verifies the narrow-Skill structure, bounded delivery command,
performance budgets, distribution, scenario catalog, and automated tests.
Before publication, record three matched trials for duration, tokens, tool calls,
and remote round trips as defined in `evals/performance-budget.json`.
