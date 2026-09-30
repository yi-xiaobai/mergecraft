---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(glab mr create:*)
description: Commit the current change, push it, and create a GitLab merge request through the bounded fast path
---

## Context

- Repository state: !`git status --short --branch`
- Current change: !`git diff HEAD -- .`

## Parameters

`/commit-push-mr [target branch] [--draft]`

Use the requested target branch, or `dev` when omitted. Create a normal MR
unless `--draft` is present.

## Execute

Apply the `git-workflow` Skill and complete the following workflow without
pausing between successful steps:

1. Use the supplied context without querying it again. Stop if it shows secrets
   or unrelated work; otherwise select only task-owned paths.
2. Generate one Conventional Commit message plus an English MR title and
   description from the supplied change in one reasoning pass.
3. Stage the selected paths and commit. Use `git push` when an upstream exists.
   Otherwise run `git push -u origin <current-branch>`, using the branch
   shown in the supplied status. The remote branch must use the same name as the local current branch.
   Never substitute `dev`, `main`, or `master` for
   `<current-branch>`.
4. Create the GitLab MR with explicit metadata and defaults:

   ```text
   glab mr create --target-branch <target> --title <title> --description <description> --assignee=@me --squash-before-merge=true --remove-source-branch=true [--draft] --yes
   ```

5. Return the commit and MR URL. Do not merge the MR.

Do not perform extra discovery, validation, fetches, or read-back calls. Let Git
hooks run normally. Stop immediately on a failed commit, push, or MR creation;
never use `--no-verify` or force push.
