---
name: git-workflow
description: Use whenever creating or updating branches, commits, pushes, PRs/MRs, merges, tags, or releases. Always create PR/MR titles and descriptions in English and enforce GitLab squash/source-branch removal defaults.
---

# Git workflow

Follow explicit user instructions first, then repository-local rules, then this
Skill. Treat Git requests as execution tasks: use the smallest set of Git
commands that safely completes the requested operation.

## Efficiency boundary

- Do not run tests, linters, builds, type checks, security scans, release gates,
  or repository-wide validation unless the user explicitly requests them or a
  repository-local instruction requires them for the requested Git operation.
  A Git hook may run normally; do not bypass it.
- Do not perform a standard diagnostic sweep. Inspect only state needed by the
  next command: for example, status for staging or switching, upstream for a
  push, and the target diff for a PR/MR.
- Do not fetch by default. Fetch once only when current remote state is needed
  to choose a base, synchronize branches, or prepare a PR/MR.
- Trust a successful Git or provider command unless its output is ambiguous or
  the operation has a specific read-back requirement below. Avoid duplicate
  status, diff, fetch, and remote queries.

## Standard flow

1. Identify the requested Git operation and inspect only its prerequisites.
   Never overwrite unrelated work or expose secrets.
2. For a new work branch, resolve the target, fetch that target once, and branch
   directly from its current remote ref. Use `dev` only when it already exists
   and no stronger target is available.
3. For a commit, stage only task-owned files and use
   `type(scope): imperative subject` for commits unless the repository differs.
4. For synchronization, fetch once before comparing branches. For an ordinary
   push, use the configured upstream directly. Preserve published history;
   force push requires an explicit user request.
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

- Do not query the PR/MR again after a successful create command merely to
  repeat values already supplied explicitly. Read it back only when the command
  response omits or contradicts a required value; correct any mismatch once and
  report any project policy that prevents the setting.

## Safety boundaries

- An explicit PR/MR or delivery request authorizes verify, commit, push, and
  PR/MR creation. A narrower request stops at its stated boundary.
- Never discard work, stash implicitly, expose secrets, use `--no-verify`,
  weaken required checks, rewrite published history, merge, tag, release, or delete a
  remote branch without the required explicit user request.
- Fix only clear in-scope hook or CI failures. Do not start unrelated validation
  to investigate them. Report infrastructure failures after one bounded retry.
- Merge only after explicit authorization and required checks. Never replace an
  existing remote tag.

## Evaluation and publication

Do not run `scripts/release_gate.py` for an ordinary commit or push. Run it only
when the user explicitly requests validation or a plugin release is being
prepared.
Historical safeguards remain covered by evidence `393b3df`, `e5f5879`,
`0335bba`, `f41ba8a`, `9f334f2`, `5d30367`, and `b2630cb`.

## Completion

Report the requested artifact, any required check that actually ran, remaining
risk, and exactly one next action. Do not run extra commands solely to populate
the report.
