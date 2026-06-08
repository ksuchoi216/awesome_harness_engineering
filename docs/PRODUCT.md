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

Only the eight `ahe-*` skill directories should appear as AHE skills in Codex. Shared templates and schemas must live outside `skills/`.

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

### `$ahe-agent`

- Modify only the purpose in `AGENTS.md`.

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

## 6. Clarification Prompt

If a user response needs clarification or more detail, AHE must ask with this exact format:

```text
Please choose one option:

1. Yes

2. No

3. Custom input

Enter 1, 2, or type your own answer:
```

## 7. Installation Behavior

- Local development install after cloning the repo:
  - `npx --yes --package=file:. ahe install`
- Deployed install target:
  - `npx ahe install`
- Helper scripts:
  - `scripts/install.sh` installs into `~/.codex`
  - `scripts/uninstall.sh` removes the eight installed AHE skills and `.codex/ahe-shared`

## 8. Success Criteria

- Codex shows the eight split AHE skills instead of one monolithic `ahe` skill.
- The installer copies all eight skill directories and the shared assets.
- The uninstall script removes the installed AHE skills and shared assets cleanly.
- Tests validate the split-skill structure and expected workflow contracts.
