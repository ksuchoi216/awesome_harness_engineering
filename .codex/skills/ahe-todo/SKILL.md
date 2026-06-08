---
name: ahe-todo
description: Append fast todo items to docs/todo.md and reflect them in feature-list.json.
---

# AHE Todo

Use this skill when the user invokes `$ahe-todo`.

## Command Workflow: ahe-todo

- Read `docs/todo.md` if it exists.
- Read `feature-list.json`.
- Ask for the todo content that should be tracked without editing `docs/PRODUCT.md` yet.
- Append the new todo content under the last `## TODO` section in `docs/todo.md`.
- If `docs/todo.md` does not contain a `## TODO` section, create one at the end of the file first.
- Update `feature-list.json` so the queued todo work is visible in the feature tracker.
- Do not modify `docs/PRODUCT.md` directly in `$ahe-todo`.
