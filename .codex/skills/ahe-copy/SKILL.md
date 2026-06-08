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

If a user answer needs clarification or a more detailed description, ask question recursively to clarify the response, and use this exact prompt:

Question: {question}
Please choose one option:

1. Yes

2. No

3. Custom input

Enter 1, 2, or type your own answer:
