# AHE Project Specification

## 1. Project Name

AHE

## 2. Product Definition

AHE is a Codex chat workflow package for building and maintaining harness files in a repository.

The user works in Codex chat, not primarily in the terminal. The package installs multiple Codex skills so the user can invoke focused commands directly in chat:

- `$ahe-init`
- `$ahe-spec`
- `$ahe-update`
- `$ahe-clear`
- `$ahe-help`

The package also installs `ahe-conversation` as an internal protocol skill for the other AHE workflow skills. It is not a user-facing command and must not be listed by `$ahe-help`.

## 3. Installed Layout

The packaged install must create the following structure inside Codex home or the current workspace:

```text
.codex/
  skills/
    ahe-init/
      SKILL.md
    ahe-conversation/
      SKILL.md
    ahe-spec/
      SKILL.md
    ahe-update/
      SKILL.md
    ahe-clear/
      SKILL.md
    ahe-help/
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

Only the five user-facing `$ahe-*` commands should be shown to users. The installed `ahe-conversation` skill is internal support for multi-turn clarification, stateful conversation, and resume-aware guidance inside other AHE skills. Shared templates and schemas must live outside `skills/`. Hooks provide exact-command routing support for users who type `ahe`.

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
- If `AGENTS.md` does not exist, copy it from the installed templates.
- Update only the project-purpose portion of `AGENTS.md`.
- Ask whether the project language is Python using a Codex-supported structured response request with meaningful options and custom input.
- If the user answers "No", ask again: "Which language do you use?".
- Copy missing template-managed root files from `ahe-shared/templates`, excluding `PRODUCT.md`, and ask for explicit overwrite confirmation before replacing an existing file.
- Execute the following three sequential steps:
  1. complete init setup work
  2. call "ahe-spec"
  3. call "ahe-update"
- Ensure that the process status (e.g., `current_step` in `.ahe/process_status.json`) tracks each step and indicates the active status of the three-step sequence: `"ahe-init"`, `"ahe-spec"`, and `"ahe-update"`.

### `$ahe-spec`

- Modify `docs/PRODUCT.md`, `docs/constraints.md`, and `docs/achitecture.md`.
- Ask recursively for product, constraint, and architecture details until the affected specification areas are clear.
- Update only the relevant docs among the three specification files.

### `$ahe-update`

- If the user is adding new work, append it into the last `## TODO` section of `docs/todo.md`, create that section when needed, and update `feature-list.json`.
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

## 6. Exact `ahe` Command Auto Operation

When the user sends exactly `ahe` in Codex chat, the installed `UserPromptSubmit` hook must inject an AHE automatic operation directive. Normal prompts that merely mention AHE, such as "explain ahe", must not activate the flow.

The directive must tell Codex to:

- Inspect harness state before choosing a workflow: `AGENTS.md`, `docs/PRODUCT.md`, `feature-list.json`, and `PROGRESS.md`.
- Run CodeGraph preflight before harness status reporting: check `command -v codegraph`; if missing, report `NOT INSTALLATION of codegraph`, skip `codegraph init` and `codegraph sync`, and continue with normal repo inspection.
- If the CodeGraph CLI exists and `.codegraph/` is missing, run `codegraph init` before reviewing code.
- If the CodeGraph CLI exists and `.codegraph/` is present, run `codegraph sync` before reviewing code.
- Review code through CodeGraph when available after preflight succeeds by preferring CodeGraph MCP or exploration behavior.
- Make the first response a concise harness engineering status report table before proceeding to edits or workflow execution.
- Use a stable Markdown table with `Item` and `Content` columns, covering `AGENTS.md`, `PRODUCT.md`, `feature-list.json`, and `PROGRESS.md`.
- Keep the table short and readable.
- Do not include the next step inside the table.
- Route to `$ahe-init` when no harness files exist.
- Continue harness engineering work when harness files exist but core harness engineering is incomplete.
- Repair or initialize harness state when `feature-list.json` is missing or invalid.
- Continue the first unfinished feature in `feature-list.json` whose dependencies are satisfied.
- Ask the user for the next task when all features are `done`.
- Ask the user a short clarification question with meaningful options when multiple next steps are plausible, feature data conflicts, dependencies are unclear, or CodeGraph review points to several valid directions.
- After the table, ask the user to confirm exactly one next-step choice: `harness engineering`, `start a new task`, or `resume existing harness work`.
- Wait for the user's confirmation such as `go ahead` before proceeding with that next step.

## 7. Conversation Protocol

If a user response needs clarification or more detail, each interactive AHE skill must follow the internal `ahe-conversation` protocol and continue the conversation recursively using a Codex-supported structured response request.

- Ask a short question matched to the active skill.
- Provide 2-3 meaningful mutually exclusive options when possible.
- Allow custom input when predefined options are not enough.
- Keep asking until the answer satisfies the skill's clarification criteria.
- Treat vague, off-topic, contradictory, or incomplete answers as not clarified yet.
- Persist the pending decision, missing field, and resume context when the conversation blocks workflow completion.
- Do not expose `$ahe-conversation` as a command; it is only shared guidance for inner skills.

## 8. Installation Behavior

- Local development install after cloning the repo:
  - `npx --yes --package=file:. ahe install`
- Deployed install target:
  - `npx ahe install`
- Helper scripts:
  - `scripts/install.sh` installs into `~/.codex`
  - `scripts/uninstall.sh` removes the installed AHE skills, `.codex/ahe-shared`, and `.codex/hooks`

## 9. Success Criteria

- Codex shows the five user-facing split AHE commands instead of one monolithic `ahe` skill.
- Exact `ahe` prompts activate automatic status, CodeGraph, and next-workflow routing; ordinary mentions of AHE do not.
- The installer copies all user-facing skill directories, the internal `ahe-conversation` protocol skill, shared assets, and hooks.
- The uninstall script removes the installed AHE skills, shared assets, and hooks cleanly.
- Tests validate the split-skill structure and expected workflow contracts.
