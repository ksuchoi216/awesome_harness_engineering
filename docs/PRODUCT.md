# AHE Project Specification

## 1. Project Name

AHE

## 2. Product Definition

AHE is a Codex chat workflow package for building and maintaining harness files in a repository.

The user works in Codex chat, not primarily in the terminal. The package installs multiple Codex skills so the user can invoke focused commands directly in chat:

- `$ahe-init`
- `$ahe-agent`
- `$ahe-product`
- `$ahe-todo`
- `$ahe-constraints`
- `$ahe-architecture`
- `$ahe-update`
- `$ahe-clear`
- `$ahe-help`
- `$ahe-copy`

## 3. Installed Layout

The packaged install must create the following structure inside Codex home or the current workspace:

```text
.codex/
  skills/
    ahe-init/
      SKILL.md
    ahe-agent/
      SKILL.md
    ahe-product/
      SKILL.md
    ahe-todo/
      SKILL.md
    ahe-constraints/
      SKILL.md
    ahe-architecture/
      SKILL.md
    ahe-update/
      SKILL.md
    ahe-clear/
      SKILL.md
    ahe-help/
      SKILL.md
    ahe-copy/
      SKILL.md
  ahe-shared/
    templates/
      AGENTS.md
      PRODUCT.md
      PROGRESS.md
      SESSION-HANDOFF.md
      init.sh
      feature-list.json
    schemas/
      process_status.schema.json
      feature-list-schema.json
```

Only the ten `ahe-*` skill directories should appear as AHE skills in Codex. Shared templates and schemas must live outside `skills/`.

## 4. Workspace Runtime State

Workspace-specific state stays under `.ahe/`.

```text
.ahe/
  process_status.json
  backups/
```

The installed skills must not store workspace runtime state under `.codex/`.

## 5. Skill Responsibilities

### `$ahe-init`

- Initialize the harness in the current workspace.
- If `AGENTS.md` already exists, ask the user whether the current `AGENTS.md` is right.
- If not, ask for the purpose of this project.
- Update only the project-purpose portion of `AGENTS.md`.
- Execute the following six sequential steps and call each subprocess:
  1. call "ahe-agents"
  2. call "ahe-product"
  3. call "ahe-architecture"
  4. call "ahe-constraints"
  5. call "ahe-copy"
  6. call "ahe-update"
- Ensure that the process status (e.g., `current_step` in `.ahe/process_status.json`) tracks each step and indicates the active status of the six steps sequence: `"ahe-agents"`, `"ahe-product"`, `"ahe-architecture"`, `"ahe-constraints"`, `"ahe-copy"`, and `"ahe-update"`.

### `$ahe-agent`

- Modify only the purpose in `AGENTS.md`.
- If `AGENTS.md` does not exist in the workspace:
  1. Copy `agents.md` from the template assets (e.g. `.codex/ahe-shared/templates/`).
  2. Rename it to `AGENTS.md` (uppercase).
  3. Ask what the purpose of this project is to user.
  4. Update the project purpose in the copied `AGENTS.md`.
  5. Ask whether the project language is Python using a Codex-supported structured response request with meaningful options and custom input.
  6. If the user answers "No", ask again: "Which language do you use?".

### `$ahe-product`

- Modify `docs/PRODUCT.md`.
- Ask recursively for product details until the specification is clear.

### `$ahe-todo`

- Append fast todo items into the last `## TODO` section of `docs/todo.md`.
- Create the `## TODO` section at the end of `docs/todo.md` when it does not exist.
- Update `feature-list.json` with the queued todo work.
- Do not modify `docs/PRODUCT.md` directly.

### `$ahe-constraints`

- Modify `docs/constraints.md`.

### `$ahe-architecture`

- Modify `docs/achitecture.md`.

### `$ahe-update`

- Read `docs/todo.md` when it exists.
- Apply queued todo content from `docs/todo.md` into `docs/PRODUCT.md`.
- Remove the applied todo content from `docs/todo.md` because it is already reflected in `docs/PRODUCT.md`.
- Update `feature-list.json`.
- Update `PROGRESS.md`.
- Update `SESSION-HANDOFF.md`.
- Keep `.ahe/process_status.json` aligned with the active workflow.

### `$ahe-clear`

1. Create a timestamped backup under `.ahe/backups/`.
2. Back up:
   - `AGENTS.md`
   - `docs/`
   - `PROGRESS.md`
   - `SESSION-HANDOFF.md`
   - `feature-list.json`
   - `init.sh`
3. Remove:
   - `docs/PRODUCT.md`
   - `PROGRESS.md`
   - `SESSION-HANDOFF.md`
   - `feature-list.json`
4. Ask the user for the new goal.
5. Set up the new objective in `AGENTS.md`.
6. Ask recursively for the new product specification.
7. Finish when the new product specification is clear.

### `$ahe-help`

- Print a list of all available AHE skills and commands with brief descriptions.

### `$ahe-copy`

- Copy template files from `ahe-shared/templates/` to the workspace.
- Place `PRODUCT.md` under `docs/PRODUCT.md` and copy all other files into the workspace root.
- Convert markdown filenames to uppercase (e.g. `agents.md` -> `AGENTS.md`) when copying.

## 6. Clarification Prompt

If a user response needs clarification or more detail, each interactive AHE skill must ask again recursively using a Codex-supported structured response request.

- Ask a short question matched to the active skill.
- Provide 2-3 meaningful mutually exclusive options when possible.
- Allow custom input when predefined options are not enough.
- Keep asking until the answer satisfies the skill's clarification criteria.
- Treat vague, off-topic, contradictory, or incomplete answers as not clarified yet.

## 7. Installation Behavior

- Local development install after cloning the repo:
  - `npx --yes --package=file:. ahe install`
- Deployed install target:
  - `npx ahe install`
- Helper scripts:
  - `scripts/install.sh` installs into `~/.codex`
  - `scripts/uninstall.sh` removes the ten installed AHE skills and `.codex/ahe-shared`

## 8. Success Criteria

- Codex shows the ten split AHE skills instead of one monolithic `ahe` skill.
- The installer copies all ten skill directories and the shared assets.
- The uninstall script removes the installed AHE skills and shared assets cleanly.
- Tests validate the split-skill structure and expected workflow contracts.
