---
name: ahe-clear
description: Back up the previous harness state, remove resettable files, and start a new objective and product spec.
---

# AHE Clear

Use this skill when the user invokes `$ahe-clear`.

## Command Workflow: ahe-clear

### Clear Preparation

- Create a timestamped backup directory under `.ahe/backups/`.
- Copy `AGENTS.md` into the backup directory.
- Copy the current `docs/PRODUCT.md` into the backup directory.
- Copy the current `PROGRESS.md` into the backup directory.
- Copy the current `SESSION-HANDOFF.md` into the backup directory.
- Copy the current `feature-list.json` into the backup directory.
- Copy `init.sh` into the backup directory.
- Copy the `docs/` folder into the backup directory.
- Copy each file while preserving the `docs/PRODUCT.md` relative path.
- Copy each file while preserving the `PROGRESS.md` relative path.
- Copy each file while preserving the `SESSION-HANDOFF.md` relative path.
- Copy each file while preserving the `feature-list.json` relative path.

### Clear Removal

- Remove the previous `docs/PRODUCT.md`.
- Remove the previous `PROGRESS.md`.
- Remove the previous `SESSION-HANDOFF.md`.
- Remove the previous `feature-list.json`.

### Reset Conversation

- Ask the user what the new goal is.
- Set up the new objective in `AGENTS.md`.
- Ask recursively for the new product specification.
- If the product specification is clear, finish it.
- Update `.ahe/process_status.json` so `current_command` is `$ahe-clear`.
- Update `.ahe/process_status.json` so `workflow_complete` is `true`.

## Clarification Rule

If a user answer needs clarification or a more detailed description, ask question recursively to clarify the response, and use this exact prompt:

Question: {question}
Please choose one option:

1. Yes

2. No

3. Custom input

Enter 1, 2, or type your own answer:

