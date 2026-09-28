---
name: git-workflow
description: Use whenever creating or updating branches, commits, pushes, PRs/MRs, merges, tags, or releases. Always create PR/MR titles and descriptions in English and enforce GitLab squash/source-branch removal defaults.
---

# Git workflow

Follow explicit user instructions first, then repository-local rules, then this
Skill. Inspect Git state before changing it and verify the result afterward.

## Standard flow

1. Inspect the current branch, status, diff, remotes, upstream, and repository
   instructions. Never overwrite unrelated work or expose secrets.
2. Resolve and fetch the target branch before creating a work branch. Use `dev`
   only when it already exists and no stronger target is available.
3. Run relevant checks, stage only task-owned files, and use
   `type(scope): imperative subject` for commits unless the repository differs.
4. Fetch before synchronizing or pushing. Preserve published history; force
   push requires an explicit user request.
5. Choose the provider from the push remote: `gh` for GitHub and `glab` for
   GitLab.

## PR/MR requirements

- Before creating or updating a PR/MR, fetch the resolved target and inspect the
  complete diff from the target branch to the current branch
  (`<target>...HEAD`). Generate the English title from the primary change shown
  by that diff, not from the branch name, commit subjects, or task wording.
  Write the English description from the same diff and actual verification,
  even when requirements or commits are Chinese. Keep code identifiers, paths,
  and commands unchanged. Do not use `--fill`.
- Create a normal PR/MR, assign the current user when supported, and use the
  resolved target branch. Creating a PR/MR does not authorize merging it.
- For every GitLab MR, pass the English metadata explicitly with `--title` and
  `--description`, and include these options in `glab mr create`:

  ```text
  --squash-before-merge=true --remove-source-branch=true
  ```

- After creation, query the MR and verify the title and description are English
  and that `squash_on_merge` and `should_remove_source_branch` are both `true`.
  Immediately update any non-English metadata. If permitted, correct false
  option values with `squash=true` and `remove_source_branch=true`, then verify
  again. Report any project policy that prevents either setting.

## Safety boundaries

- An explicit PR/MR or delivery request authorizes verify, commit, push, and
  PR/MR creation. A narrower request stops at its stated boundary.
- Never discard work, stash implicitly, expose secrets, use `--no-verify`,
  weaken checks, rewrite published history, merge, tag, release, or delete a
  remote branch without the required explicit user request.
- Fix only clear in-scope hook or CI failures. Report infrastructure failures
  after one bounded retry.
- Merge only after explicit authorization and required checks. Never replace an
  existing remote tag.

## Evaluation and publication

Run `python3 scripts/release_gate.py` before publishing changes to this Skill.
Historical safeguards remain covered by evidence `393b3df`, `e5f5879`,
`0335bba`, `f41ba8a`, `9f334f2`, `5d30367`, and `b2630cb`.

## Completion

Report the branch, commit or remote artifact, checks, worktree/upstream state,
remaining risk, and exactly one next action.
