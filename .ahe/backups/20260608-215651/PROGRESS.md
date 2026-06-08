# PROGRESS.md

## Current Status

**Last Updated:** 2026-06-08 21:56 +0900
**Session ID:** ahe-clear-new-goal
**Active Feature:** ahe clear - new goal reset

## Completed

- [x] Created `.ahe/backups/20260608-215651/` for the `ahe clear` workflow.
- [x] Copied `AGENTS.md` and `docs/PRODUCT.md` into the clear-workflow backup directory.
- [x] Backed up the current root AHE-managed files into `.ahe/backups/20260608-144947/`.
- [x] Added the packaged installer scaffold and embedded skill assets under `.codex/skills/ahe/`.
- [x] Verified the setup artifacts with shell checks, JSON validation, installer doctor/version, installer smoke install, and direct execution of the Python test assertions.
- [x] Implemented `feat-002 Chat Command Routing` by expanding `.codex/skills/ahe/SKILL.md` and adding `tests/test_chat_command_routing.py`.
- [x] Implemented `feat-003 Init Workflow` by adding step-by-step instructions to `.codex/skills/ahe/SKILL.md` and creating `tests/test_init_workflow.py`.
- [x] Implemented `feat-004 Product Workflow` by adding a dedicated `ahe product` workflow contract to `.codex/skills/ahe/SKILL.md` and creating `tests/test_product_workflow.py`.
- [x] Fixed the `npx ahe install` smoke-test path resolution in `bin/ahe` so packaged installs work when the shell entrypoint is invoked through npm's `.bin` symlink.
- [x] Implemented `feat-005 Check and Resume Workflows` by adding dedicated `ahe check` and `ahe resume` workflow contracts to `.codex/skills/ahe/SKILL.md`.
- [x] Added `tests/test_check_resume_workflows.py` to verify validation scope, report behavior, resume-state inspection, and next-question handling.
- [x] Implemented `feat-006 Session Tracking and Handoff` by adding a cross-workflow tracking sync contract to `.codex/skills/ahe/SKILL.md`.
- [x] Added `tests/test_session_tracking_handoff.py` to verify process-status synchronization and progress/handoff update rules.
- [x] Implemented `feat-007 Clear Workflow` by adding the `ahe clear` command contract to `.codex/skills/ahe/SKILL.md`.
- [x] Updated `docs/PRODUCT.md` so the product specification includes `ahe clear`.
- [x] Added `tests/test_clear_workflow.py` to verify backup and new-goal conversation requirements.
- [x] Implemented `feat-008 Clarification Prompt Format` by adding a global clarification rule to `.codex/skills/ahe/SKILL.md`.
- [x] Updated `docs/PRODUCT.md` with the exact three-option clarification prompt format.
- [x] Added `tests/test_clarification_prompt.py` to verify the exact prompt lines and option meanings.

## In Progress

- [ ] `ahe clear` is active and waiting for the new goal.
  - Details: Backup location is `.ahe/backups/20260608-215651/`. `.ahe/process_status.json` is paused at `ask_new_goal`.
  - Blockers: None.

## Blocked

- [ ] No current blocker.

## Decisions

- **Installer implementation is part of feat-001**: `npx ahe install` now has a concrete package scaffold instead of staying as a later placeholder.
  - Context: The product goal and user instructions both require installation to be included now.
  - Alternatives considered: Deferring the installer to a later feature would leave the setup feature incomplete.
- **The installer bin is a shell script**: The npm package exposes `./bin/ahe` instead of a Node entry file.
  - Context: This workspace has no `node` binary, but npm can still package a portable shell bin for `npx ahe install`.
  - Alternatives considered: A Node CLI would be harder to verify locally in the current environment.
- **Local development uses a file package spec**: cloned-repo testing should use `npx --yes --package=file:. ahe install`.
  - Context: The package is not deployed yet, but the user still wants the install UX to be exercised through `npx`.
  - Alternatives considered: Using only `bash bin/ahe install` does not match the intended installer entrypoint closely enough.
- **The installer must resolve its real package path before copying skill files**: `npx` executes `bin/ahe` through npm's `.bin` symlink, so the installer has to follow symlinks before computing `PACKAGE_ROOT`.
  - Context: The full pytest run exposed a failure where the installer looked for `.codex/skills/ahe` under `node_modules/.codex` instead of `node_modules/ahe/.codex`.
  - Alternatives considered: Weakening the smoke test would hide a real packaging defect and would not verify the published install path.
- **Workflow contracts should be explicit in the installed skill, not only in `docs/PRODUCT.md`**: `ahe check` and `ahe resume` now have dedicated sections in `.codex/skills/ahe/SKILL.md`.
  - Context: The installed skill is the artifact Codex will actually use in chat, so relying on the product spec alone leaves runtime behavior underspecified.
  - Alternatives considered: Leaving the behavior only in `docs/PRODUCT.md` would keep the implementation contract incomplete for the actual installed skill surface.
- **Tracking rules should live in one cross-workflow section instead of being inferred from scattered command steps**: `.ahe/process_status.json`, `PROGRESS.md`, and `SESSION-HANDOFF.md` now have explicit synchronization rules in the installed skill.
  - Context: The schema defined the shape of runtime state, but not when all three tracking artifacts must move together during active workflows.
  - Alternatives considered: Repeating partial tracking rules in each command section would leave the sync contract fragmented and easier to drift.

## Change Log

- `.ahe/backups/20260608-215651/`, `.ahe/process_status.json`, `PROGRESS.md`, `SESSION-HANDOFF.md` - Started `ahe clear`, backed up `AGENTS.md` and `docs/PRODUCT.md`, and advanced the workflow to the new-goal question.
- `package.json`, `bin/ahe` - Added the minimal installer package and CLI entrypoint.
- `.codex/skills/ahe/` - Added the embedded skill, templates, and schemas copied by the installer.
- `init.sh`, `templates/` - Normalized the setup scripts and canonical template names to the conservative product spec.
- `.ahe/process_status.json`, `tests/test_project_setup.py` - Added runtime state and setup verification coverage.
- `.codex/skills/ahe/SKILL.md`, `tests/test_chat_command_routing.py` - Added Chat Command Routing definitions and verification logic.
- `scripts/install.sh`, `scripts/uninstall.sh` - Added helper scripts for local installation and uninstallation of the AHE skill.
- `.codex/skills/ahe/SKILL.md`, `tests/test_init_workflow.py` - Implemented Init Workflow instructions and test validation.
- `tests/test_project_setup.py` - Fixed case-sensitivity issue for macOS compatibility.
- `.codex/skills/ahe/SKILL.md`, `tests/test_product_workflow.py` - Added the Product Workflow contract and verification coverage.
- `bin/ahe`, `tests/test_project_setup.py` - Made the installer smoke test hermetic and fixed symlink-aware package root resolution for `npx` installs.
- `.codex/skills/ahe/SKILL.md`, `tests/test_check_resume_workflows.py` - Added explicit Check and Resume workflow contracts and verification coverage.
- `.codex/skills/ahe/SKILL.md`, `tests/test_session_tracking_handoff.py` - Added explicit cross-workflow tracking and handoff synchronization rules and verification coverage.
- `.codex/skills/ahe/SKILL.md`, `docs/PRODUCT.md`, `feature-list.json`, `tests/test_clear_workflow.py` - Added `ahe clear` workflow routing, behavior, tracking, and tests.
- `.codex/skills/ahe/SKILL.md`, `docs/PRODUCT.md`, `feature-list.json`, `tests/test_clarification_prompt.py` - Added the exact clarification prompt format for unclear or under-detailed user responses.
