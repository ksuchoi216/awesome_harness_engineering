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

If a user answer needs clarification or a more detailed description, ask again recursively using a Codex-supported structured response request. Ask a short question, provide 2-3 meaningful mutually exclusive options when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect an actionable todo entry for `docs/todo.md` and `feature-list.json`.

### Questions to Ask

- Ask what work needs to be done.
- Ask which file, feature area, or workflow the todo affects.
- Ask what outcome or completion signal the todo should capture.

### Clarification Criteria

- The answer must describe actionable work, the affected area, and the intended outcome.
- The answer must be specific enough to record as a useful queued task.

### Re-ask When

- Ask again when the answer is too broad, off-topic, or only names a topic without describing the work.
- Ask again when dependencies, affected area, or intended outcome are still unclear.
