---
name: ahe-copy
description: Copy template files (excluding AGENTS.md and PRODUCT.md) from ahe-shared/templates to the workspace root, converting markdown names to uppercase.
---

# AHE Copy

Use this skill when the user invokes `$ahe-copy`.

## Command Workflow: ahe-copy

Engage in an interactive conversation with the user to verify the copy operation before writing:

- Find all template files under `.codex/ahe-shared/templates/`.
- Ignore `AGENTS.md` (or `agents.md`) and `PRODUCT.md` (or `product.md`).
- For each of the remaining files:
  - If the file has a `.md` extension, convert its filename to uppercase (e.g., `progress.md` -> `PROGRESS.md`, `session-handoff.md` -> `SESSION-HANDOFF.md`).
  - The destination path is directly in the workspace root.
- Before copying, check if any of these files already exist in the workspace root:
  - If they exist, ask the user for confirmation before overwriting them using the Clarification Rule.
  - If the user confirms or if they do not exist, proceed with the copy.

## Clarification Rule

If a user answer needs clarification or a more detailed description, ask again recursively using a Codex-supported structured response request. Ask a short question, provide 2-3 meaningful mutually exclusive options when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect explicit user confirmation for the copy operation, especially when existing files may be overwritten.

### Questions to Ask

- Ask whether the copy should continue when target files already exist.
- Ask which files should be skipped when the user does not want a full overwrite.
- Ask follow-up questions when overwrite intent is still unclear.

### Clarification Criteria

- The answer must make overwrite intent explicit for existing files.
- The answer must be clear enough to decide whether to copy, skip, or partially overwrite files.

### Re-ask When

- Ask again when the answer is ambiguous, contradictory, or does not explicitly confirm overwrite behavior.
- Ask again when the user answer does not make the copy decision explicit.
