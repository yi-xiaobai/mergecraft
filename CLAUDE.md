# Repository instructions

All responses and maintained files use English.

This repository distributes one team-rules Skill at
`skills/git-workflow/SKILL.md` and two explicit Claude Code delivery commands:
`commands/commit-push.md` owns the pre-commit-aware push boundary, while
`commands/commit-push-mr.md` owns the cross-system GitLab boundary. Keep team
decisions and safety boundaries in the Skill and do not create specialist
agents for command-local behavior.

Use native model capabilities for ordinary Git mechanics and deterministic
scripts for state collection, tests, and release gates. Add a Skill rule only
from an observed costly failure or repeated workflow friction, then add an
observable scenario under `evals/`. Measure delivery cost with matched trials
defined in `evals/performance-budget.json`; do not substitute inferred budgets
for results.

Run `python3 scripts/release_gate.py` before publication. Commit messages use
`type(scope): message` unless a higher-priority repository rule changes it.
