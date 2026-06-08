---
name: ahe-todo
description: Append fast todo items to docs/todo.md and reflect them in feature-list.json.
---

# AHE Todo

Use this skill when the user invokes `$ahe-todo`.

## Command Workflow: ahe-todo

- Read `docs/todo.md` if it exists.
- Read `feature-list.json`.
- Engage in an interactive conversation with the user to clarify the todo item:
  - Ask clarifying questions about target goals, scope, sub-tasks, or dependencies.
  - Suggest phrasing and details for the todo entry and ask for user approval.
  - Recursively discuss and adjust until the user approves the todo item.
- Once finalized, append the new todo content under the last `## TODO` section in `docs/todo.md`.
- If `docs/todo.md` does not contain a `## TODO` section, create one at the end of the file first.
- Update `feature-list.json` so the queued todo work is visible in the feature tracker.
- Do not modify `docs/PRODUCT.md` directly in `$ahe-todo`.

## Clarification Rule

If a user answer needs clarification or a more detailed description, ask question recursively to clarify the response, and use this exact prompt:

Question: {question}
Please choose one option:

1. Yes

2. No

3. Custom input

Enter 1, 2, or type your own answer:

