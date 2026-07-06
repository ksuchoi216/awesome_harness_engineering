# Awesome Harness Engineering (AHE)

AHE installs global Codex and Antigravity skills that manage harness files through chat. The repository uses a one-package, two-internal-packages layout (`packages/ahe-codex` and `packages/ahe-antigravity`) shipped as a single npm package. The
public entrypoints stay small: use exact `ahe` for bootstrap or continuation,
`ahe ship` to save the latest plan (in Codex) or refresh and execute a saved plan (in Antigravity),
and `ahe git` for safe git orchestration. Use `ahe <query>` or `<query> ahe`
for explicit AHE requests such as `ahe update product spec` or `ahe stale tests`.
For a detailed in-chat explanation of the AHE architecture and workflows, use the helper `ahe-overview`.

## Core Command Workflows

Here are intuitive flow examples for the primary AHE commands. The public work-routing surface is `ahe`, `ahe-ship`, and `ahe-git`; conversational queries such as `ahe add dashboard export feature` are routed through `ahe`.

### `ahe` Bootstrap Flow
1. **Empty Workspace**: You have a new or existing repo that needs AHE.
2. **ahe calling**: You type `ahe` or `ahe new` in Codex.
3. **Initialization**: `ahe-think` detects the missing harness, calls internal `ahe-new`, and then hands off to `ahe-harness` to sync product docs.

### `ahe ship` Flow
1. **plan mode in codex**: Generate an implementation plan inside Codex.
2. **ahe-ship calling in codex**: If in Plan Mode, the Codex host exits Plan Mode and replays the command. Outside Plan Mode, Codex saves the plan to `.plans/` and stops.
3. **ahe-ship calling in antigravity**: Antigravity refreshes the saved plan against current code, executes it, and cleans it up.

### `ahe` Follow-Up Flow
1. **Error Encountered**: A test fails or intent changes after execution.
2. **ahe query**: You type `ahe stale tests` or another explicit follow-up request in Codex.
3. **Normal Routing**: `ahe-think` treats that request as ordinary AHE work and routes it to the right internal worker.

### General `ahe` Flow
1. **Ongoing Work**: You need to implement a feature or update docs.
2. **ahe calling**: You type `ahe` or a specific query like `ahe update product spec` in Codex.
3. **Automatic Routing**: `ahe-think` evaluates your request and automatically routes it to the right agent (like `ahe-solve` or `ahe-harness`).

## Installed Skills

| Skill | Role |
| --- | --- |
| `ahe` | Top-level user-facing continuation skill that routes exact `ahe` and `ahe` query forms through `ahe-think`. |
| `ahe-new` | Internal bootstrap workflow that `ahe-think` calls when the workspace has no usable harness yet. |
| `ahe-think` | Centered internal router that judges what is missing and chooses the next agent. |
| `ahe-review` | Review agent for repo code, harness state, and CodeGraph context. |
| `ahe-converse` | Clarification agent for recursive user conversation. |
| `ahe-harness` | Harness-management agent for product docs, instructions, feature tracking, and todo sync. |
| `ahe-feature` | Internal helper for deriving feature-list entries from product context. |
| `ahe-solve` | Feature-solving agent that divides and plans implementation work. |
| `ahe-overview` | Helper skill that explains the AHE concept, entrypoints, and main workflows in chat. |
| `ahe-ship` | In Codex: saves Plan Mode plan to `.plans/`. In Antigravity: refreshes and executes exactly one plan from `.plans/`. |
| `ahe-git` | Independent git orchestration workflow for safe fetch, review, and commit handling. |

## Routing Model

The Codex-side model is centered but flexible:

- exact `ahe` -> `ahe-think` -> `ahe-review | ahe-converse | ahe-harness | ahe-solve`
- `ahe <query>` or `<query> ahe` -> `ahe-think` -> `ahe-review | ahe-converse | ahe-harness | ahe-solve`
- `ahe-think` may call internal `ahe-new` when the workspace needs bootstrap or restart handling
- exact `ahe ship` -> independent plan-export workflow (Codex) or execution workflow (Antigravity)
- exact `ahe git` -> independent git workflow

- `ahe-think` is the center of judgment.
- Worker agents can call each other directly when that is the logical next
  action.
- Typical direct handoffs are `ahe-harness -> ahe-converse`,
  `ahe-solve -> ahe-review`, and `ahe-review -> ahe-harness`.

## Query Examples

- `ahe`
- `ahe new`
- `ahe ship`
- `ahe stale tests`
- `ahe update product spec`
- `ahe add dashboard export feature`

Only exact `ahe`, exact `ahe ship`, exact `ahe-ship`, exact `$ahe-ship`,
exact `ahe git`, exact `ahe-git`, exact `$ahe-git`, `ahe-overview`,
`ahe <query>`, and `<query> ahe` activate the hook. Middle mentions that do
not fit those command shapes do not.
