# AHE Project Specification

## 1. Product Definition

AHE is a global Codex and Antigravity chat workflow package for building and maintaining
harness files in any active repository. The project uses a single published npm package
that internally splits logic into `packages/ahe-codex` and `packages/ahe-antigravity`.

User-facing chat commands:

- `$ahe-new`
- exact `ahe new`
- exact `ahe-new`
- exact `ahe`
- exact `ahe ship`
- exact `ahe-ship`
- exact `$ahe-ship`
- exact `ahe fix`
- exact `ahe-fix`
- exact `$ahe-fix`
- explicit `ahe <query>`

Internal workflow skills:

- `ahe-thinker`
- `ahe-reviewer`
- `ahe-conversator`
- `ahe-harness`
- `ahe-solver`
- `ahe-compression`

The independent user-facing exporter is `ahe-ship`. It writes the latest Codex
Plan Mode `<proposed_plan>` into `.plans/{plan_name}.md`, triggers Antigravity
execution for that plan, and removes the file only after verified completion.
It must not route through the internal AHE agent network.

The independent user-facing fix planner is `ahe-fix`. It writes a concrete
fix plan into `.plans/{plan_name}.md` for fixing errors or following the
user's current intention when that intention differs from the previous AHE
flow. It may call `ahe-conversator` when clarification is needed.

AHE always installs into the global Codex home (`$CODEX_HOME` when set,
otherwise `~/.codex`). Installed skills, shared files, and hook files must not
be copied into each target workspace.

## 2. Installed Layout

The project uses an internal `packages/` workspace layout, separating `ahe-codex` and `ahe-antigravity`.

The global Codex installation (`ahe-codex`) contains:

- skills: `ahe-new`, `ahe-thinker`, `ahe-reviewer`, `ahe-conversator`,
  `ahe-harness`, `ahe-fix`, `ahe-solver`, `ahe-ship`, and `ahe-compression`
- shared templates: `AGENTS.md`, `product.md`, `progress.md`,
  `session-handoff.md`, `init.sh`, and `feature-list.json`
- schemas: `process_status.schema.json` and `feature-list-schema.json`
- hooks: `hooks.json` and `ahe-hook.js`

The global Antigravity installation (`ahe-antigravity`) installs the `ahe-ship` skill to `~/.gemini/config/skills/ahe-ship` and provides `ahe-antigravity ahe-ship <plan-path>` for running a saved plan through `agy`.

## 3. Agent Model

The centered internal model is:

`query -> ahe-thinker -> ahe-reviewer | ahe-conversator | ahe-harness | ahe-solver`

- `ahe-thinker` is the central decision layer.
- Worker agents may call each other directly when that is the logical next
  action.
- Direct handoffs must still provide a clear result back to the broader AHE
  workflow.

## 4. Responsibilities

### `$ahe-new`

- Initialize the harness in the current workspace from the global AHE skill
  installation.
- If no AHE-managed harness files exist, start initialization normally.
- If harness files exist, read them first, summarize current purpose and product
  state, then ask for restart scope before replacing anything.
- Do not create backup copies during restart; summarize replaced state in the
  refreshed tracking artifacts instead.
- Keep product behavior, requirements, scope, success criteria, and workflow
  details out of `AGENTS.md`.
- Send product behavior, scope, requirements, success criteria, and workflow
  details to `ahe-harness` so they are written in `docs/product.md` first.
- Generate an empty `feature-list.json` only as a placeholder until product
  context is populated.

### `ahe-harness`

- Modify `docs/product.md` and `docs/INSTRUCTIONS.md`.
- Treat `docs/product.md` as the overview product explanation.
- Support optional staged product docs named `docs/product1.md`,
  `docs/product2.md`, and so on.
- Use numbered staged product docs in numeric suffix order, starting with
  `docs/product1.md`.
- Ignore non-numeric product docs such as `docs/product-alpha.md` for stage
  ordering.
- When staged product docs exist, derive feature-list items from only the active
  product stage and keep future stages as context until earlier stages are
  complete.
- Advance from one numbered product stage to the next only after all
  `feature-list.json` items derived from the current active stage are `done`.
- If no numbered staged product docs exist, continue the normal overview-only
  flow from `docs/product.md`.
- Apply queued `docs/todo.md` content into the active product source, then
  update `feature-list.json`, `progress.md`, `session-handoff.md`, and
  `.ahe/process_status.json`.
- For `ahe compress feature-list`, replace old completed feature entries with
  one summarized done feature and preserve unfinished, blocked, or active items
  in detail.
- If no new feature can be derived from `docs/product.md`, call
  `ahe-conversator` to ask what next feature, product direction, or goal should
  be tracked.

### `ahe-thinker`

- Inspect the current unit as `project`, `feature`, or `sub-feature`.
- Judge the current unit against `Why`, `What`, and `How`.
- Use `ahe-compression` before reading full harness files when the detector
  returns `COMPRESSION_REQUIRED`.
- Route to `ahe-reviewer`, `ahe-conversator`, `ahe-harness`, or `ahe-solver`
  based on the missing need.

### Other Internal Skills

- `ahe-reviewer` inspects code, harness files, progress evidence, and CodeGraph
  context when available.
- `ahe-conversator` asks one focused question at a time and persists blocked
  conversation state.
- `ahe-solver` divides broad feature work and plans each smaller problem before
  implementation.
- `ahe-compression` detects oversized harness files and compacts stale history
  while preserving active requirements, current decisions, unfinished work,
  blockers, dependencies, required headers, and valid JSON.

### `ahe-ship`

- Export the most recent Codex Plan Mode `<proposed_plan>` already visible in
  the current conversation.
- Create `.plans/{plan_name}.md` in the active repository with compact handoff
  context for Antigravity or another LLM platform.
- Run `ahe-antigravity ahe-ship .plans/{plan_name}.md` after writing the plan.
- Remove the plan file only when Antigravity exits successfully and emits the
  exact marker `AHE_PLAN_COMPLETE`.
- Keep the plan file when execution fails, is partial, or cannot verify full
  completion.
- Stay independent from `ahe-thinker`, `ahe-harness`, `ahe-solver`, and the
  normal AHE status workflow.

### `ahe-fix`

- Create a concrete fix plan for errors, bugs, broken behavior, or changed user
  intention.
- Create `.plans/{plan_name}.md` in the active repository.
- Include fix goal, current evidence, assumptions, scope, steps, verification
  plan, risks, and next-agent instructions.
- Call `ahe-conversator` when the fix target, scope, or success criteria are
  unclear.
- Stay independent from `ahe-thinker` and the normal AHE status workflow.

## 5. Hook Behavior

- Exact `ahe` activates the progress router.
- Exact `ahe new`, exact `ahe-new`, and exact `$ahe-new` activate the new
  start router.
- Exact `ahe ship`, exact `ahe-ship`, and exact `$ahe-ship` activate the
  independent plan export workflow.
- Exact `ahe fix`, exact `ahe-fix`, and exact `$ahe-fix` activate the
  independent fix-plan workflow.
- Explicit `ahe <query>` activates the thinker-routed query path.
- Broad non-prefixed prompts must not activate AHE.
- The first response must include a concise status table covering `AGENTS.md`,
  `product.md`, `INSTRUCTIONS.md`, `feature-list.json`, and `progress.md`.
- Product routing must inspect all `docs/*.md` files, treat `docs/product.md`
  as overview context, and choose the active staged product source from
  `docs/product1.md`, `docs/product2.md`, and later numeric files when present.

## 6. Success Criteria

- AHE installs and runs from the global Codex home, not workspace-local
  `.codex` skill directories.
- Exact `ahe`, exact `ahe new`, exact `ahe ship`, exact `ahe fix`, and
  explicit `ahe <query>` route to their expected workflows.
- The installer copies the current skill set into the global Codex home and no
  longer depends on removed legacy skills.
- Tests validate the split-skill structure, staged product-doc contract, and
  explicit query-routing contract.
