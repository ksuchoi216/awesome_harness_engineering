# Add `ahe-git` To Codex And Antigravity

## Handoff Summary

Add a new user-facing `ahe-git` skill to both packaged environments.

On the Codex side, expose it as a first-class independent AHE command through exact `ahe git` and `ahe-git` hook routing, parallel to `ahe-ship` and `ahe-fix`.

On the Antigravity side, install a matching `ahe-git` skill and add wrapper support through `ahe-antigravity ahe-git [repo-root]`.

The workflow must:
1. discover the active repo plus nested Git repos and submodules,
2. fetch and safely fast-forward to latest upstream head where possible,
3. inspect pending changes repo-by-repo,
4. draft and self-check one commit message per dirty repo,
5. commit each dirty repo separately.

If Git is in a state that is not easy and safe to continue, `ahe-git` must stop, explain the exact problem, and tell the user how to resolve it manually. It must not attempt risky recovery.

## User Review Required
> [!IMPORTANT]
> The current repository state confirms that `ahe-git` is not yet implemented. The `packages/ahe-codex/bin/ahe-codex` and `packages/ahe-antigravity/bin/ahe-antigravity` files are ready to be updated, and the hooks in `packages/ahe-codex/.codex/hooks/ahe-hook.js` are ready to accept the new `ahe-git` directives. Does this refreshed plan look good to proceed?

## Source Plan

### Summary

Add a new user-facing `ahe-git` skill in both packaged environments.

The Codex side becomes a first-class AHE command, exposed through exact `ahe git` and `ahe-git` hook routing, with an independent workflow like `ahe-ship` and `ahe-fix`.

The Antigravity side gets a matching installed skill plus wrapper support through `ahe-antigravity ahe-git [repo-root]`.

The workflow is identical on both sides:
1. discover the active repo plus nested Git repos/submodules,
2. make sure each repo is at latest upstream head when that can be done safely,
3. inspect pending changes repo-by-repo,
4. draft and self-check one commit message per dirty repo,
5. commit each dirty repo separately.

If Git enters a state that is not straightforward and safe to continue, `ahe-git` must stop, explain the exact problem, and tell the user how to resolve it manually. It must not attempt risky recovery.

### Public Interfaces

- Add Codex skill: `packages/ahe-codex/.codex/skills/ahe-git/SKILL.md`
- Add Antigravity skill: `packages/ahe-antigravity/skills/ahe-git/SKILL.md`
- Add Codex hook triggers for exact `ahe git` and `ahe-git`
- Add Antigravity wrapper command: `ahe-antigravity ahe-git [repo-root]`
- Update install/doctor/uninstall flows so both packages manage `ahe-git`
- Update README and `docs/product.md` so `ahe-git` is documented beside `ahe-ship` and `ahe-fix`

### Implementation Changes

- Codex package:
  - Add `ahe-git` to the managed-skill list in the Codex installer.
  - Extend the hook with a new independent directive for `ahe git` / `ahe-git`.
  - The directive must route through `ahe-think` first, then immediately call `ahe-git`, and must explicitly skip the normal harness workflow.

- Antigravity package:
  - Install `ahe-git` into `~/.gemini/config/skills/ahe-git`.
  - Extend `ahe-antigravity` usage/help/install/doctor/uninstall to know about `ahe-git`.
  - Add `ahe-antigravity ahe-git [repo-root]` that resolves the target path, verifies `agy`, sends an execution prompt with the repo root and workflow contract, and succeeds only when a completion marker is printed.

- `ahe-git` skill behavior, both platforms:
  - Discover repos by scanning for both `.git` directories and `.git` files so submodules/worktrees are included.
  - Normalize discovered repo roots, deduplicate them, and process them deepest-first for commits so submodule repos commit before parent gitlink updates.
  - For each repo, inspect current branch and upstream state after `git fetch`.
  - Safe pull rule:
    - If the repo is clean and upstream is ahead, fast-forward with `git pull --ff-only`.
    - If the repo is already at upstream head, continue.
    - If the repo has local changes and is not already at upstream head, stop and explain the issue.
    - If upstream is missing, detached, diverged, rebasing, merging, cherry-picking, or cannot fast-forward cleanly, stop and explain the issue.
    - Never auto-stash, auto-merge, auto-rebase, auto-resolve conflicts, or change branch topology.
  - Failure policy:
    - On any hard Git state, report:
      - which repo is blocked,
      - the exact detected condition,
      - why `ahe-git` is refusing to continue,
      - concrete manual steps the user should run or perform next.
    - Keep the guidance specific to the detected state, such as:
      - set or fix upstream,
      - finish or abort merge/rebase/cherry-pick,
      - clean or stash local changes before pulling,
      - resolve divergence manually,
      - switch from detached HEAD to a branch.
    - Do not attempt partial recovery beyond safe read-only diagnosis.
  - Dirty-state review rule:
    - Inspect `git status --short`.
    - Read unstaged diffs first, then staged diffs, and include untracked files so the commit message covers the full pending change.
  - Commit-message rule:
    - Generate one concise conventional-style message per repo (`feat:`, `fix:`, `chore:` etc.) based on the actual diff.
    - Run an explicit self-check pass to reject vague or misleading messages before commit.
    - If the message is still ambiguous after self-check, stop and ask instead of committing a generic summary.
  - Commit rule:
    - Stage with `git add -A` inside that repo.
    - Commit exactly once per dirty repo with its reviewed message.
    - After submodule commits, re-evaluate parent repos so gitlink updates are committed if they became dirty.

- Tracking artifacts during implementation:
  - Add one new feature entry in `feature-list.json` for `ahe-git`.
  - Update `progress.md` and `session-handoff.md` with the new command contract, verification evidence, and any unresolved blockers.
  - Do not modify templates or `AGENTS.md`.

## Execution Context

This repository is split into two internal packages already used for AHE:
- `packages/ahe-codex`
- `packages/ahe-antigravity`

Current comparable command surface is `ahe-ship`:
- Codex-side packaged skill exists at `packages/ahe-codex/.codex/skills/ahe-ship/SKILL.md`
- Antigravity-side packaged skill exists at `packages/ahe-antigravity/skills/ahe-ship/SKILL.md`
- Codex hook routing lives in `packages/ahe-codex/.codex/hooks/ahe-hook.js`
- Codex installer surface lives in `packages/ahe-codex/bin/ahe-codex`
- Antigravity wrapper surface lives in `packages/ahe-antigravity/bin/ahe-antigravity`
- Packaging/install contract tests already cover these surfaces in `tests/test_project_setup.py`, `tests/test_command_set.py`, `tests/test_ahe_hook.py`, and `tests/test_ahe_antigravity_ship.py`

There is no existing packaged helper dedicated to Git orchestration; current deterministic helper scripts are limited to ship/fix writers and compression detectors. Prefer matching the existing AHE pattern: skill-first workflow text, plus minimal wrapper/contract changes.

## Assumptions

- `ahe-git` is a first-class command surface, not skill-only.
- Codex should recognize exact `ahe git` and `ahe-git`.
- Antigravity should install the skill and expose `ahe-antigravity ahe-git [repo-root]`.
- Commit messages should default to concise conventional-commit style.
- The implementation should stay simple and avoid introducing a shared helper library unless validation proves it is necessary.

## Constraints

- Do not modify `AGENTS.md` except for `PROJECT_PURPOSE`; this feature should not need any `AGENTS.md` change.
- Do not modify template contents under `templates/`.
- Stay aligned with existing AHE split-package layout and existing command patterns.
- `ahe-git` must remain independent from the normal harness workflow, similar to `ahe-ship` and `ahe-fix`.
- On complex Git problems, the skill must inform the user of the exact issue and how to solve it instead of trying to solve it itself.
- Never auto-stash, auto-merge, auto-rebase, auto-resolve conflicts, or otherwise perform risky Git recovery.

## Verification Plan

Run at minimum:
- `pytest tests/test_project_setup.py tests/test_command_set.py tests/test_ahe_hook.py tests/test_ahe_git_skill_contract.py tests/test_ahe_antigravity_git.py -x`
- `pytest tests/ -x`
- `bash -n bin/ahe`
- `bash -n packages/ahe-codex/bin/ahe-codex`
- `bash -n packages/ahe-antigravity/bin/ahe-antigravity`
- `node --check packages/ahe-codex/.codex/hooks/ahe-hook.js`
- `./init.sh`

If environment and approvals allow, finish with reinstall validation through `./install.sh`; otherwise record that limitation explicitly.

## Risks and Open Questions

- The Antigravity wrapper contract for `ahe-git` must be defined carefully enough that tests can validate the prompt and completion-marker behavior without coupling to implementation details.
- The exact user-facing wording for blocked Git states should be precise and stable enough for contract tests, but not so brittle that routine copy edits constantly break them.
- Parent-repo gitlink updates after submodule commits must be covered in the workflow text so implementers do not forget the second pass.

## Instructions for Next Agent

Implement this as a narrow contract extension, mirroring `ahe-ship` where possible.

Work in this order:
1. add packaged skill directories and SKILL.md contracts for Codex and Antigravity,
2. wire Codex hook detection for exact `ahe git` / `ahe-git`,
3. update Codex installer managed-skill list,
4. update Antigravity wrapper/install/doctor/uninstall for `ahe-git`,
5. add focused tests for packaging, hook routing, skill contract, and Antigravity wrapper behavior,
6. update README, `docs/product.md`, `feature-list.json`, `progress.md`, and `session-handoff.md`,
7. run verification and record any unavailable checks.

Keep the implementation conservative: when Git is messy, diagnose and instruct the user; do not attempt recovery.
