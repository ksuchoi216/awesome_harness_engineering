---
name: ahe-help
description: Show a list of commands in AHE to the user.
---

# AHE Help

Use this skill when the user invokes `$ahe-help`.

## Command Workflow: ahe-help

When the user requests help or a list of commands, print a summary of the available AHE skills and how to invoke them:

- `$ahe-init`: Initialize the harness in the current workspace.
- `$ahe-spec`: Modify `docs/PRODUCT.md`, `docs/constraints.md`, and `docs/achitecture.md` through one sequential specification conversation.
- `$ahe-update`: Queue todo work in `docs/todo.md`, apply queued todo content into `docs/PRODUCT.md`, and update tracking files.
- `$ahe-clear`: Back up the current harness, reset the project goal and specification, and rebuild them.
- `$ahe-help`: Show this command summary and description of all AHE skills.
