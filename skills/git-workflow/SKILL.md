---
name: git-workflow
description: Apply MergeCraft team conventions when creating branches, committing changes, pushing, resolving hook failures, or delivering work through a GitLab merge request. Use for Git write operations in a team repository; do not use for read-only Git inspection.
---

# Team Git workflow

Use the model's native Git capabilities for ordinary operations. This Skill
adds only team-specific decisions, safety boundaries, and GitLab defaults.
Follow an explicit user request first, then repository-local rules, then this
Skill.

## Branches

- Use the user- or repository-specified base. Fall back to `dev` only when it
  already exists.
- When the repository has no stronger convention, name work branches
  `{type}_{slug}_v{N}` using `feat`, `fix`, `hotfix`, `refactor`, or `chore`.
- Do not switch branches with a dirty worktree until every change is attributed
  to the task or the user chooses how to preserve it. Never stash implicitly.

## Commits

- Review staged, unstaged, and untracked paths before staging.
- Stage task-owned paths only. Exclude secrets, credentials, `.env` files, and
  unrelated work without reproducing sensitive values.
- Use `type(scope): imperative subject` unless repository rules differ. Keep
  unrelated changes in separate commits.
- Let repository hooks run normally. Never use `--no-verify`.

## Hook failures

- Fix a source failure only when the cause is clear and the correction remains
  within the requested change, then retry the commit.
- Stop on infrastructure, environment, security threshold, or ambiguous
  failures. Never weaken hooks, tests, baselines, thresholds, or configuration.

## Push and merge requests

- Push with upstream tracking when needed. Never force-push unless the user
  explicitly requests it and the impact has been checked.
- Use the requested MR target, or `dev` when no stronger target exists.
- Write the MR title and description in English from the actual change, while
  preserving code identifiers, paths, and commands.
- For GitLab MRs, assign the current user and pass these settings explicitly:

  ```text
  --squash-before-merge=true --remove-source-branch=true
  ```

- Create a normal MR unless the user requests a draft. Creating an MR does not
  authorize merging it.

## Safety boundaries

Never discard work, expose secrets, weaken checks, rewrite published history,
merge, tag, release, or delete a remote branch without the required explicit
authorization.

## Completion

Report the requested artifact or the failed step. Trust a successful Git or
provider response; do not run extra commands solely to enrich the report.
