---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*)
description: Commit the current change, handle pre-commit results safely, and push without creating a merge request
---

## Context

- Current status: !`git status --short --branch`
- Current changes: !`git diff HEAD -- .`

## Parameters

`/commit-push [request]`

The optional request may identify the intended files or commit purpose.

## Your task

Apply the `git-workflow` Skill and complete this workflow in one response:

1. Use the supplied context without querying it again. Stop if it shows secrets
   or unrelated work; otherwise select only task-owned paths.
2. Stage the selected paths and create one Conventional Commit.
3. Let the repository's pre-commit hook run normally. If it fails, follow the
   Skill's hook-failure rules and do not push until the commit succeeds.
4. Push the current branch, adding upstream tracking only when the supplied
   branch status shows no upstream.
5. Report the commit and push result.

Do not run proactive validation or remote discovery. Never bypass hooks or
force-push. Stop immediately when a failure is not safely recoverable.
