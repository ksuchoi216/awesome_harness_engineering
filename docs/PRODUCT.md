# AHE Project Specification

## 1. Product Definition

AHE is a Codex chat workflow package for building and maintaining harness files
in a repository.

The user-facing chat commands are:

- `$ahe-init`
- exact `ahe init`
- exact `ahe-init`
- exact `ahe`
- explicit `ahe <query>`

The internal skills are:

- `ahe-thinker`
- `ahe-reviewer`
- `ahe-conversator`
- `ahe-harness`
- `ahe-solver`
- `ahe-compression`

Only `$ahe-init` is user-facing as an installed skill.

## 2. Installed Layout

```text
.codex/
  skills/
    ahe-init/
      SKILL.md
    ahe-thinker/
      SKILL.md
    ahe-reviewer/
      SKILL.md
    ahe-conversator/
      SKILL.md
    ahe-harness/
      SKILL.md
    ahe-solver/
      SKILL.md
    ahe-compression/
      SKILL.md
      scripts/
        check-harness-size.sh
  ahe-shared/
    config.yaml
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
  hooks/
    hooks.json
    ahe-hook.js
```

## 3. Agent Model

The centered internal model is:

`query -> ahe-thinker -> ahe-reviewer | ahe-conversator | ahe-harness | ahe-solver`

- `ahe-thinker` is the central decision layer.
- Worker agents may call each other directly when that is the logical next
  action.
- Direct handoffs must still provide a clear result back to the broader AHE
  workflow.

## 4. Responsibilities

### `$ahe-init`

- Initialize the harness in the current workspace.
- If no AHE-managed harness files exist, start initialization normally without
  asking a restart-scope question.
- If any AHE-managed harness file exists, read the existing files first,
  summarize the current project purpose and product specification state, and ask
  what restart scope the user wants before backing up, removing, overwriting, or
  refreshing existing harness files.
- Interpret restart scope from the user's free-form answer.
- Keep product behavior, requirements, scope, success criteria, and workflow
  details out of `AGENTS.md`.
- Send product behavior, scope, requirements, success criteria, and workflow
  details to `ahe-harness` so they are written in `docs/PRODUCT.md` first.
- Generate an empty `feature-list.json` from a template only as a placeholder;
  do not write concrete feature items until `docs/PRODUCT.md` is populated.
- Track `ahe-init` then `ahe-harness` in `.ahe/process_status.json`.

### `ahe-harness`

- Modify `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md`.
- Treat `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md` as the required harness
  contract.
- If the user is adding new work, append it into the last `## TODO` section of
  `docs/todo.md`, create that section when needed, and update
  `feature-list.json`.
- Apply queued todo content from `docs/todo.md` into `docs/PRODUCT.md`.
- Remove applied todo content from `docs/todo.md`.
- Update `feature-list.json`, `PROGRESS.md`, `SESSION-HANDOFF.md`, and
  `.ahe/process_status.json`.
- For `ahe compress feature-list`, compress completed feature items while
  preserving `id`, `name`, `description`, `dependencies`, `status`, and short
  evidence.
- Preserve unfinished, blocked, or active items in detail.
- If no new feature can be derived from `docs/PRODUCT.md`, call
  `ahe-conversator` to ask what next feature, product direction, or goal should
  be tracked.

### `ahe-thinker`

- Inspect the current unit as `project`, `feature`, or `sub-feature`.
- Judge the current unit against `Why`, `What`, and `How`.
- Use `ahe-compression` before reading full harness files when the detector
  returns `COMPRESSION_REQUIRED`.
- Route to `ahe-reviewer`, `ahe-conversator`, `ahe-harness`, or `ahe-solver`
  based on the missing need.

### `ahe-reviewer`

- Inspect code, harness files, progress evidence, and `.codegraph` / CodeGraph
  context when available.
- Report evidence to `ahe-thinker` or call `ahe-harness` directly when harness
  drift is discovered.

### `ahe-conversator`

- Ask one focused question at a time.
- Clarify missing purpose, requirements, scope, next feature, or workflow
  direction.
- Persist the blocked state in `.ahe/process_status.json` and update handoff
  artifacts when necessary.

### `ahe-solver`

- Divide broad feature work into smaller problems when useful.
- Plan each smaller problem before implementation.
- Call `ahe-reviewer` for code understanding and `ahe-conversator` for missing
  requirements.

### `ahe-compression`

- Provide a shell-script line-count detector for AHE-managed harness files.
- Return a deterministic compression decision before `ahe-thinker` or
  `ahe-harness` reads large files wholesale.
- Compress only stale or noisy history while preserving active requirements,
  current decisions, unfinished work, blockers, dependencies, required headers,
  and valid JSON.

## 5. Hook Behavior

- Exact `ahe` activates the progress router.
- Exact `ahe init`, exact `ahe-init`, and exact `$ahe-init` activate the new
  start router.
- Explicit `ahe <query>` activates the thinker-routed query path.
- Broad non-prefixed prompts must not activate AHE.
- The first response must include a concise status report table covering
  `AGENTS.md`, `PRODUCT.md`, `INSTRUCTIONS.md`, `feature-list.json`, and
  `PROGRESS.md`.

## 6. Success Criteria

- Codex shows only `$ahe-init` as a user-facing installed skill.
- Exact `ahe`, exact `ahe init`, and explicit `ahe <query>` route into the new
  internal model.
- The installer copies the new internal skill set and no longer depends on
  `ahe-spec`, `ahe-update`, `ahe-thinking`, or `ahe-conversation`.
- Tests validate the new split-skill structure and explicit query-routing
  contract.
