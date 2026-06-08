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

If a user answer needs clarification or a more detailed description, ask again recursively using a Codex-supported structured response request. Ask a short question, provide 2-3 meaningful mutually exclusive options when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect the new goal and replacement product direction required to finish the reset workflow.

### Questions to Ask

- Ask what the new goal is.
- Ask what the new product should do and who it is for.
- Ask follow-up questions about scope or success criteria when the reset target is still unclear.

### Clarification Criteria

- The answer must define a concrete new goal.
- The answer must give enough product direction to start the replacement specification.

### Re-ask When

- Ask again when the answer is vague, off-topic, or still tied to the previous objective without a clear reset direction.
- Ask again when the new goal or product direction is too incomplete to finish the reset safely.
