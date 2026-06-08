---
name: ahe-help
description: Show a list of commands in AHE to the user.
---

# AHE Help

Use this skill when the user invokes `$ahe-help`.

## Command Workflow: ahe-help

When the user requests help or a list of commands, print a summary of the available AHE skills and how to invoke them:

- `$ahe-init`: Initialize the harness in the current workspace.
- `$ahe-agent`: Modify only the purpose in `AGENTS.md`.
- `$ahe-product`: Modify `docs/PRODUCT.md` recursively through a sequential conversation.
- `$ahe-todo`: Append fast todo items into the last `## TODO` section of `docs/todo.md` and update `feature-list.json`.
- `$ahe-constraints`: Modify `docs/constraints.md`.
- `$ahe-architecture`: Modify `docs/achitecture.md`.
- `$ahe-update`: Apply queued todo content from `docs/todo.md` into `docs/PRODUCT.md` and update tracking files.
- `$ahe-clear`: Back up the current harness, reset the project goal and specification, and rebuild them.
- `$ahe-help`: Show this command summary and description of all AHE skills.
