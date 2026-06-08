# PROGRESS.md

## Current Status

**Last Updated:** 2026-06-08 15:42 +0900
**Session ID:** setup-chat-routing
**Active Feature:** feat-004 - Product Workflow

## Completed

- [x] Backed up the current root AHE-managed files into `.ahe/backups/20260608-144947/`.
- [x] Added the packaged installer scaffold and embedded skill assets under `.codex/skills/ahe/`.
- [x] Verified the setup artifacts with shell checks, JSON validation, installer doctor/version, installer smoke install, and direct execution of the Python test assertions.
- [x] Implemented `feat-002 Chat Command Routing` by expanding `.codex/skills/ahe/SKILL.md` and adding `tests/test_chat_command_routing.py`.
- [x] Implemented `feat-003 Init Workflow` by adding step-by-step instructions to `.codex/skills/ahe/SKILL.md` and creating `tests/test_init_workflow.py`.

## In Progress

- [ ] Prepare `feat-004 Product Workflow`.
  - Details: Implement the `ahe product` workflow that creates or updates docs/PRODUCT.md and synchronizes tracking artifacts.
  - Blockers: None.

## Blocked

- [ ] No current product blocker. Local `pytest` is still unavailable, so the test module was executed directly with the Python standard library instead of the pytest runner.

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

## Change Log

- `package.json`, `bin/ahe` - Added the minimal installer package and CLI entrypoint.
- `.codex/skills/ahe/` - Added the embedded skill, templates, and schemas copied by the installer.
- `init.sh`, `templates/` - Normalized the setup scripts and canonical template names to the conservative product spec.
- `.ahe/process_status.json`, `tests/test_project_setup.py` - Added runtime state and setup verification coverage.
- `.codex/skills/ahe/SKILL.md`, `tests/test_chat_command_routing.py` - Added Chat Command Routing definitions and verification logic.
- `scripts/install.sh`, `scripts/uninstall.sh` - Added helper scripts for local installation and uninstallation of the AHE skill.
- `.codex/skills/ahe/SKILL.md`, `tests/test_init_workflow.py` - Implemented Init Workflow instructions and test validation.
- `tests/test_project_setup.py` - Fixed case-sensitivity issue for macOS compatibility.
