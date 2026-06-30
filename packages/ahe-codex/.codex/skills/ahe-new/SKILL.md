---
name: ahe-new
description: Initialize AHE in the current workspace and create the base harness files.
---

# AHE New

Use this skill when the user invokes `$ahe-new`.

## Command Workflow: new

### Workspace Inspection

- Read `AGENTS.md` if it already exists.
- Read all `docs/*.md` files when they exist. Treat every docs file as
  supporting project context, even when `AGENTS.md` does not name it directly.
- Especially read `docs/product.md` and
  `docs/product{number}.md` files when present because they explain what to do.
- Treat `docs/product.md` as overview context and numbered
  `docs/product{number}.md` files as ordered product stages.
- Ignore non-numeric product docs such as `docs/product-alpha.md` for stage
  ordering.
- Read existing workspace-root harness files that may be copied from templates, including `progress.md`, `session-handoff.md`, `feature-list.json`, and `init.sh`.
- Read `status.json` when it exists.
- Treat `AGENTS.md`, `docs/product.md`, `docs/INSTRUCTIONS.md`, `progress.md`, `session-handoff.md`, `feature-list.json`, `init.sh`, and `status.json` as AHE-managed harness files for restart-scope decisions.

### Sequential Conversation Flow

- Treat exact `ahe new` as a possible new start request.
- If no AHE-managed harness files exist, start initialization normally without asking a restart-scope question.
- If any AHE-managed harness file already exists, read the existing files first.
- When existing harness files are present, summarize the current project purpose and product specification state, then ask what restart scope the user wants before removing, overwriting, or refreshing existing harness files.
- Do not remove, overwrite, or refresh existing harness files until the restart scope is clear.
- Interpret the restart scope from the user's free-form answer; examples are guidance only and must not limit valid answers.
- If the answer says `purpose`, full restart, or equivalent, `purpose` means restart the whole harness from the project purpose.
- If the answer says `product`, product spec, or equivalent, `product` means preserve the project purpose in `AGENTS.md` and restart product specification work in `docs/product.md`.
- If the answer names staged product work, restart only the named product stage
  files unless the user also requests the overview product spec.
- If the answer names a narrower custom scope, preserve unrelated harness files and restart only the named scope.
- If `AGENTS.md` already exists, ask the user whether the current `AGENTS.md` is right.
- If the current `AGENTS.md` is not right or does not exist, ask for the purpose of this project.
- If `AGENTS.md` does not exist, copy `AGENTS.md` from `.codex/ahe-shared/templates/`.
- Update only the `PROJECT_PURPOSE` portion of `AGENTS.md`.
- Keep `AGENTS.md` limited to the project purpose and base agent settings.
- Do not put product specification details in `AGENTS.md`.
- Send product behavior, scope, requirements, success criteria, and workflow details to `ahe-harness` so they are written in `docs/product.md` first.
- Generating an empty `feature-list.json` from a template is allowed, but do not write concrete feature items until `docs/product.md` is populated.
- When staged product docs exist, let `ahe-harness` derive concrete feature
  items from only the active product stage.
- Ask whether the project language is Python using a Codex-supported structured response request with meaningful options and custom input.
- If the user answers that the project language is not Python, ask again: "Which language do you use?".
- Do not create backup copies of the replaced harness files.
- When a restart scope replaces prior harness history, summarize the replaced harness history in the refreshed tracking artifacts instead of creating backups.
- Remove the previous `docs/product.md` and `docs/INSTRUCTIONS.md` when the chosen restart scope includes product specification.
- Remove the previous `progress.md` when the chosen restart scope includes progress tracking.
- Remove the previous `session-handoff.md` when the chosen restart scope includes session handoff.
- Remove the previous `feature-list.json` when the chosen restart scope includes feature tracking.
- Remove only the files included in the chosen restart scope before continuing the new start flow.
- Find all template files under `.codex/ahe-shared/templates/`.
- Ignore `AGENTS.md` and `product.md` when copying template files.
- Before copying a template file into the workspace root, check whether the target file already exists and ask for explicit overwrite confirmation when needed.
- Execute the following three steps sequentially, updating the progress status (`current_step` in `status.json`):
  1. complete the embedded init setup work (status: "new")
  2. call "ahe-harness" (status: "ahe-harness")
  3. call "ahe-harness-checker" (status: "ahe-harness-checker")

### Harness Generation

- Create or refresh `AGENTS.md`.
- Create or refresh missing workspace-root harness files from `.codex/ahe-shared/templates/`, converting markdown filenames to uppercase when needed.
- Create `status.json` and update it at each step to indicate the active status from the three-step sequence.
- Create missing harness files from `.codex/ahe-shared/templates/`.
- Keep the generated files aligned with the installed shared templates.
- Only allow additions/removals/edits to `docs/INSTRUCTIONS.md` inside `## CAN CHANGE INSTRUCTIONS`; preserve `## MUST NOT CHANGE INSTRUCTIONS`.

## Clarification Rule

When the next setup step is not clear, follow the `ahe-think` protocol first. If `ahe-think` finds missing information, follow the `ahe-converse` protocol. Ask again recursively using a Codex-supported structured response request, provide 2-3 meaningful mutually exclusive options when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect the project purpose, language choice, and overwrite decisions needed to continue initialization safely.

### Questions to Ask

- Ask whether the existing `AGENTS.md` is correct.
- Ask what restart scope the user wants when harness files already exist.
- Ask what the purpose of this project is when `AGENTS.md` is missing or incorrect.
- Ask whether the project language is Python and ask which language is used when the answer is no or custom.
- Ask whether template files should be overwritten when target files already exist.
- Ask follow-up questions when the restart scope, purpose, language, or overwrite choice is still unclear.

### Clarification Criteria

- The answer must be specific enough to update `PROJECT_PURPOSE`.
- The answer must make it clear whether initialization should continue with the current `AGENTS.md` or with a new purpose.
- The answer must clearly identify whether Python guidance applies.
- The answer must make the restart scope clear when existing harness files must be replaced.
- The answer must make overwrite intent explicit for existing template targets.
- The answer must resolve any setup choice that blocks the next workflow step.

### Re-ask When

- Ask again when the answer is vague, off-topic, contradictory, or incomplete.
- Ask again when the answer does not identify the project goal, target user, or intended outcome clearly enough to continue initialization.
- Ask again when the language answer is ambiguous or does not clearly name the language in use.
- Ask again when the overwrite decision is not explicit.
