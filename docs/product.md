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
- `ahe fix <query>`
- `<query> ahe fix`
- `ahe <query>` (e.g. `ahe compress`)
- `<query> ahe` (e.g. `compress ahe`)

Internal workflow skills:

- `ahe-think`
- `ahe-review`
- `ahe-converse`
- `ahe-harness`
- `ahe-solve`
- `ahe-compress`

The independent user-facing exporter is `ahe-ship`. It detects if the current
Codex thread is in Plan Mode and exits Plan Mode first. Then it writes the
latest `<proposed_plan>` into `.plans/{plan_name}.md` and stops there.
It must not route through the internal AHE agent network.

The independent user-facing fix planner is `ahe-fix`. It writes a concrete
fix plan into `.plans/{plan_name}.md` for fixing errors or following the
user's current intention when that intention differs from the previous AHE
flow. It may call `ahe-converse` when clarification is needed. It must not
route through `ahe-think`.

AHE always installs into the global Codex home (`$CODEX_HOME` when set,
otherwise `~/.codex`). Installed skills, shared files, and hook files must not
be copied into each target workspace.

## 2. Installed Layout

The project uses an internal `packages/` workspace layout, separating `ahe-codex` and `ahe-antigravity`.

The global Codex installation (`ahe-codex`) contains:

- skills: `ahe-new`, `ahe-think`, `ahe-review`, `ahe-converse`,
  `ahe-harness`, `ahe-fix`, `ahe-solve`, `ahe-ship`, and `ahe-compress`
- shared templates: `AGENTS.md`, `product.md`, `progress.md`,
  `session-handoff.md`, `init.sh`, and `feature-list.json`
- schemas: `process_status.schema.json` and `feature-list-schema.json`
- hooks: `hooks.json` and `ahe-hook.js`

The global Antigravity installation (`ahe-antigravity`) installs the `ahe-ship` skill to `~/.gemini/config/skills/ahe-ship` for running a saved plan through `agy`.

## 3. Agent Model

The Codex-side model is:

- exact `ahe` -> `ahe-think` -> `ahe-review | ahe-converse | ahe-harness | ahe-solve`
- `ahe <query>` or `<query> ahe` -> `ahe-think` -> `ahe-review | ahe-converse | ahe-harness | ahe-solve`
- exact `ahe new` -> dedicated new-start workflow first, then `ahe-harness`
- exact `ahe ship` -> independent plan export workflow
- exact `ahe fix`, `ahe fix <query>`, or `<query> ahe fix` -> independent fix-plan workflow

- `ahe-think` is the central decision layer.
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
  `status.json`.
- For `ahe compress`, run both the harness-size detector and the stale-test detector.
- If the harness-size detector signals compression pressure, replace old
  completed feature entries with one summarized done feature and preserve
  unfinished, blocked, or active items in detail.
- If no new feature can be derived from `docs/product.md`, call
  `ahe-converse` to ask what next feature, product direction, or goal should
  be tracked.

### `ahe-think`

- Inspect the current unit as `project`, `feature`, or `sub-feature`.
- Judge the current unit against `Why`, `What`, and `How`.
- Use `ahe-compress` before reading full harness files when the detector
  returns `COMPRESSION_REQUIRED`.
- Route to `ahe-review`, `ahe-converse`, `ahe-harness`, or `ahe-solve`
  based on the missing need.

### Other Internal Skills

- `ahe-review` inspects code, harness files, progress evidence, and CodeGraph
  context when available.
- `ahe-converse` asks one focused question at a time and persists blocked
  conversation state.
- `ahe-solve` divides broad feature work and plans each smaller problem before
  implementation.
- `ahe-compress` detects oversized harness files and stale overlapping tests. It compacts stale history
  while preserving active requirements, current decisions, unfinished work,
  blockers, dependencies, required headers, and valid JSON.
  Detector markers:
  - `TEST_COMPRESSION_REQUIRED`
  - `REVIEW_TEST\t<legacy-file>\tcovered_by=<keeper-files>`

### `ahe-ship`

- Detect if the current conversation is still in Plan Mode and exit Plan Mode first before continuing.
- Export the most recent Codex Plan Mode `<proposed_plan>` already visible in
  the current conversation.
- Create `.plans/{plan_name}.md` in the active repository with compact handoff
  context for Antigravity or another LLM platform.
- Stay independent from `ahe-think`, `ahe-harness`, `ahe-solve`, and the
  normal AHE status workflow.

### `ahe-fix`

- Create a concrete fix plan for errors, bugs, broken behavior, or changed user
  intention.
- Create `.plans/{plan_name}.md` in the active repository.
- Include fix goal, current evidence, assumptions, scope, steps, verification
  plan, risks, and next-agent instructions.
- Call `ahe-converse` when the fix target, scope, or success criteria are
  unclear.
- Stay independent from `ahe-think` and the normal AHE status workflow.

## 5. Hook Behavior

- Exact `ahe` activates the progress router.
- Exact `ahe new`, exact `ahe-new`, and exact `$ahe-new` activate the new
  start router.
- Exact `ahe ship`, exact `ahe-ship`, and exact `$ahe-ship` activate the
  independent plan export workflow.
- Exact `ahe fix`, exact `ahe-fix`, and exact `$ahe-fix` activate the
  independent fix-plan workflow.
- `ahe fix <query>` and `<query> ahe fix` activate the independent fix-plan workflow.
- `ahe <query>` and `<query> ahe` activate the thinker-routed query path.
- Prompts that mention `ahe` in the middle without matching one of those command shapes must not activate AHE.
- The first response must include a concise status table covering `AGENTS.md`,
  `product.md`, `INSTRUCTIONS.md`, `feature-list.json`, and `progress.md`.
- Product routing must inspect all `docs/*.md` files, treat `docs/product.md`
  as overview context, and choose the active staged product source from
  `docs/product1.md`, `docs/product2.md`, and later numeric files when present.

## 6. Success Criteria

- AHE installs and runs from the global Codex home, not workspace-local
  `.codex` skill directories.
- Exact `ahe`, exact `ahe new`, exact `ahe ship`, exact `ahe fix`, and
  the query forms `ahe <query>`, `<query> ahe`, `ahe fix <query>`, and
  `<query> ahe fix` route to their expected workflows.
- The installer copies the current skill set into the global Codex home and no
  longer depends on removed legacy skills.
- Tests validate the split-skill structure, staged product-doc contract, and
  explicit query-routing contract.
