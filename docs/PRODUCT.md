# AHE Project Specification

## 1. Project Name

AHE

## 2. Product Definition

AHE is a Codex chat workflow package for building and maintaining harness files in a repository.

The user works in Codex chat, not primarily in the terminal. The package installs multiple Codex skills so the user can invoke focused commands directly in chat:

- `$ahe-init`

Users should start new harness work with exact `ahe init`, exact `ahe-init`, or `$ahe-init`, and
continue existing harness work with exact `ahe`.

The package also installs `ahe-thinking`, `ahe-conversation`, `ahe-spec`, and
`ahe-update` as internal workflow skills. They are not user-facing commands.

## 3. Installed Layout

The packaged install must create the following structure inside Codex home or the current workspace:

```text
.codex/
  skills/
    ahe-init/
      SKILL.md
    ahe-thinking/
      SKILL.md
    ahe-conversation/
      SKILL.md
    ahe-spec/
      SKILL.md
    ahe-update/
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
  hooks/
    hooks.json
    ahe-hook.js
```

Only `$ahe-init` should be shown as a user-facing skill. Exact `ahe`, exact
`ahe init`, and exact `ahe-init` are the user-facing chat commands. The installed `ahe-thinking`
skill is the internal decision layer that judges what
must be clarified, what can be executed, and which workflow should run next.
The installed `ahe-conversation` skill is internal support for multi-turn
clarification, stateful conversation, and resume-aware guidance after
`ahe-thinking` identifies a missing decision. Shared templates and schemas must
live outside `skills/`. Hooks provide exact-command routing support for users
who type `ahe`.

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
- If no AHE-managed harness files exist, start initialization normally without
  asking a restart-scope question.
- If any AHE-managed harness file exists, read the existing files first,
  summarize the current project purpose and product specification state, and
  ask what restart scope the user wants before backing up, removing,
  overwriting, or refreshing existing harness files.
- Interpret restart scope from the user's free-form answer. For example,
  `purpose` means restart the whole harness from the project purpose, while
  `product` means preserve the project purpose in `AGENTS.md`, back up the
  current product/specification files in scope, and restart product
  specification work in `docs/PRODUCT.md`.
- If `AGENTS.md` already exists, ask the user whether the current `AGENTS.md` is right.
- If not, ask for the purpose of this project.
- If `AGENTS.md` does not exist, copy it from the installed templates.
- Update only the project-purpose portion of `AGENTS.md`.
- Keep product behavior, requirements, scope, success criteria, and workflow
  details out of `AGENTS.md`; these specification details belong in
  `docs/PRODUCT.md` through `ahe-spec`.
- Ask whether the project language is Python using a Codex-supported structured response request with meaningful options and custom input.
- If the user answers "No", ask again: "Which language do you use?".
- When exact `ahe init` is used for a user-scoped restart on an existing
  harness, back up the affected current harness files under `.ahe/backups/`,
  remove only the files in the chosen restart scope, and continue the
  initialization flow.
- Copy missing template-managed root files from `ahe-shared/templates`, excluding `PRODUCT.md`, and ask for explicit overwrite confirmation before replacing an existing file.
- Execute the following three sequential steps:
  1. complete init setup work
  2. call "ahe-spec"
  3. call "ahe-update"
- Ensure that the process status (e.g., `current_step` in `.ahe/process_status.json`) tracks each step and indicates the active status of the three-step sequence: `"ahe-init"`, `"ahe-spec"`, and `"ahe-update"`.

### `ahe-spec` (internal)

- Modify `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md`. `docs/ARCHITECTURE.md` is optional.
- Treat `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md` as the required harness contract. `docs/PRODUCT.md` is the canonical home for product specification
  details collected during `ahe init`.
- Ask recursively for product and instructions details until the affected specification areas are clear.
- Update only the relevant docs among the specification files.

### `ahe-update` (internal)

- If the user is adding new work, append it into the last `## TODO` section of `docs/todo.md`, create that section when needed, and update `feature-list.json`.
- Read `docs/todo.md` when it exists.
- Apply queued todo content from `docs/todo.md` into `docs/PRODUCT.md`.
- Remove the applied todo content from `docs/todo.md` because it is already reflected in `docs/PRODUCT.md`.
- Update `feature-list.json`.
- Update `PROGRESS.md`.
- Update `SESSION-HANDOFF.md`.
- Keep `.ahe/process_status.json` aligned with the active workflow.

## 6. Exact `ahe` Command Auto Operation

When the user sends exactly `ahe` in Codex chat, the installed
`UserPromptSubmit` hook must inject an AHE progress directive. When the user
sends exactly `ahe init`, exact `ahe-init`, or exact `$ahe-init`, the hook must inject a new-start directive. Normal
prompts that merely mention AHE, such as "explain ahe", must not activate the
flow.

The directive must tell Codex to:

- Inspect harness state before choosing a workflow: `AGENTS.md`, `docs/PRODUCT.md`, `docs/INSTRUCTIONS.md`, `feature-list.json`, and `PROGRESS.md`.
- Run CodeGraph preflight before harness status reporting: check `command -v codegraph`; if missing, report `NOT INSTALLATION of codegraph`, skip `codegraph init` and `codegraph sync`, and continue with normal repo inspection.
- If the CodeGraph CLI exists and `.codegraph/` is missing, run `codegraph init` before reviewing code.
- If the CodeGraph CLI exists and `.codegraph/` is present, run `codegraph sync` before reviewing code.
- Review code through CodeGraph when available after preflight succeeds by preferring CodeGraph MCP or exploration behavior.
- Make the first response a concise harness engineering status report table before proceeding to edits or workflow execution.
- Use a stable Markdown table with `Item` and `Content` columns, covering `AGENTS.md`, `PRODUCT.md`, `INSTRUCTIONS.md`, `feature-list.json`, and `PROGRESS.md`.
- Keep the table short and readable.
- Do not include the next step inside the table.
- Use `ahe-thinking` as the internal decision layer before choosing the next
  action.
- Route to `$ahe-init` when no harness files exist.
- Classify the harness into exactly one state after the table:
  - `harness engineering not enough`
  - `in the middle of building features`
  - `completed all`
- Continue harness engineering work when harness files exist but core harness
  engineering is incomplete.
- Repair or initialize harness state when `feature-list.json` is missing or invalid.
- Continue the first unfinished feature in `feature-list.json` whose
  dependencies are satisfied.
- Ask the user for the next task when all features are `done` and no obvious
  harness gap remains.
- Continue automatically after classification instead of waiting for a separate
  next-step confirmation.
- Follow this loop while routing work: `thinking -> conversation if needed ->
  execution -> thinking`.
- Treat exact `ahe` as the progress path for continuing existing harness work.
- Treat exact `ahe init`, exact `ahe-init`, and exact `$ahe-init` as the new-start path for beginning or reinitializing
  harness work through `$ahe-init`.

## 7. Thinking Protocol

Each interactive AHE workflow must follow the internal `ahe-thinking` protocol
before acting when the next safe step is not already obvious.

- Inspect the current unit as `project`, `feature`, or `sub-feature`.
- Judge the current unit against `Why`, `What`, and `How`.
- For a `project`, require `Why`, `What`, and `How` by default.
- For a `feature` or `sub-feature`, require only the minimum of `Why`, `What`,
  and `How` needed to proceed safely.
- If the current unit is already clear from the project context, do not ask all
  three questions again.
- If clarity is missing, call `ahe-conversation` with the exact missing
  question type.
- If clarity is sufficient, continue to the next skill or next unfinished
  feature.
- Reflect clarified project or feature intent into `docs/PRODUCT.md` and keep
  `feature-list.json` focused on tracking the work itself.

## 8. Conversation Protocol

If a user response needs clarification or more detail, each interactive AHE skill must follow the internal `ahe-conversation` protocol and continue the conversation recursively using a Codex-supported structured response request.

- Use `ahe-conversation` only after `ahe-thinking` identifies the missing
  decision or missing `Why`, `What`, or `How`.
- Ask a short question matched to the active skill.
- Provide 2-3 meaningful mutually exclusive options when possible.
- Allow custom input when predefined options are not enough.
- Keep asking until the answer satisfies the skill's clarification criteria.
- Treat vague, off-topic, contradictory, or incomplete answers as not clarified yet.
- Persist the pending decision, missing field, and resume context when the conversation blocks workflow completion.
- Do not expose `$ahe-conversation` as a command; it is only shared guidance for inner skills.

## 9. Installation Behavior

- Local development install after cloning the repo:
  - `npx --yes --package=file:. ahe install`
- **Global Published Installation**
  - `npx --package=@ksuchoi216/ahe ahe install` (or `npm install -g @ksuchoi216/ahe` then `ahe install`)
- `ahe install` must remove stale AHE-owned entries from `.codex/config.toml`
  before installing files. It must preserve unrelated plugin, hook, and agent
  configuration.
- `ahe uninstall` must remove installed AHE skills, shared assets, hooks, and
  stale AHE-owned entries from `.codex/config.toml`. It must preserve unrelated
  config entries.
- Helper scripts:
  - `scripts/install.sh` installs into `~/.codex`
  - `scripts/uninstall.sh` removes the installed AHE skills, `.codex/ahe-shared`, `.codex/hooks`, and AHE-owned `.codex/config.toml` entries through the packaged uninstall command.

## 10. Success Criteria

- Codex shows only `$ahe-init` as a user-facing skill instead of a broad AHE
  command list.
- Users can start new harness work with exact `ahe init`, exact `ahe-init`, or exact `$ahe-init` and continue existing
  harness work with exact `ahe`.
- Exact `ahe` prompts activate automatic status, CodeGraph, and next-workflow routing; ordinary mentions of AHE do not.
- The installer copies all user-facing skill directories, the internal
  `ahe-thinking` and `ahe-conversation` protocol skills, shared assets, and
  hooks.
- The uninstall script removes the installed AHE skills, shared assets, and hooks cleanly.
- Tests validate the split-skill structure and expected workflow contracts.
