---
name: ahe-git
description: Use in Antigravity to execute an ahe-git run via the `ahe-antigravity ahe-git` command.
---

# AHE Git (Antigravity)

`ahe-git` is a user-facing AHE command independent from the normal AHE agent network.

Use this skill only to orchestrate safe Git pulls and commits across the active repository and its nested Git repositories or submodules.

## Workflow

1. **Discover**: Scan for both `.git` directories and `.git` files to find all nested repositories, worktrees, and submodules. Normalize and deduplicate the repo roots. Process them deepest-first (so submodules commit before parent gitlink updates).
2. **Safe Pull**: For each repo, run `git fetch` and inspect the current branch and upstream state:
   - If the repo is clean and upstream is ahead, fast-forward with `git pull --ff-only`.
   - If the repo is already at upstream head, continue.
   - If the repo has local changes and is not already at upstream head, **stop and explain the issue**.
   - If upstream is missing, detached, diverged, rebasing, merging, cherry-picking, or cannot fast-forward cleanly, **stop and explain the issue**.
   - *Never* auto-stash, auto-merge, auto-rebase, auto-resolve conflicts, or change branch topology.
3. **Failure Policy**: On any hard Git state, stop immediately and report:
   - Which repo is blocked.
   - The exact detected condition.
   - Why `ahe-git` is refusing to continue.
   - Concrete manual steps the user should perform next (e.g., set upstream, finish merge, clean changes).
   - Do not attempt partial recovery beyond safe read-only diagnosis.
4. **Dirty-State Review**: Inspect `git status --short`. Read unstaged diffs first, then staged diffs, and include untracked files so the commit message covers the full pending change.
5. **Commit-Message Drafting**: Generate one concise conventional-style message per repo (`feat:`, `fix:`, `chore:`, etc.) based on the actual diff.
   - Run an explicit self-check pass to reject vague or misleading messages before commit.
   - If the message is still ambiguous after self-check, stop and ask the user instead of committing a generic summary.
6. **Commit**: Stage with `git add -A` inside that repo. Commit exactly once per dirty repo with its reviewed message.
7. **Re-evaluate**: After submodule commits, re-evaluate parent repos so gitlink updates are committed if they became dirty.

Print the exact line `AHE_GIT_COMPLETE` only when the full workflow is finished successfully with no skipped work. Do not print this if there are failures.
