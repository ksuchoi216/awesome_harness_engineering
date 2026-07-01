# Awesome Harness Engineering (AHE)

AHE installs global Codex and Antigravity skills that manage harness files through chat. The repository uses a one-package, two-internal-packages layout (`packages/ahe-codex` and `packages/ahe-antigravity`) shipped as a single npm package. The
public entrypoints stay small: use `ahe new` to start or reset harness work,
`ahe` to continue existing work, `ahe ship` to save the latest plan (in Codex) or refresh and execute a saved plan (in Antigravity),
`ahe fix` to create a `.plans` fix plan, and
`ahe <query>` or `<query> ahe` for explicit AHE requests such as `ahe compress`
or `compress ahe`. For a detailed in-chat explanation of the AHE architecture and workflows, use `ahe-overview`.

## Core Command Workflows

Here are intuitive flow examples for the primary AHE commands. While `ahe`, `ahe-new`, `ahe-ship`, and `ahe-fix` are the explicit commands, you can also use conversational queries (e.g., `ahe add dashboard export feature`) which are automatically routed.

### `ahe new` Flow
1. **Empty Workspace**: You have a new or existing repo that needs AHE.
2. **ahe-new calling**: You type `ahe new` in Codex.
3. **Initialization**: It prepares the workspace, creates templates, and hands off to `ahe-harness` to sync your product docs.

### `ahe ship` Flow
1. **plan mode in codex**: Generate an implementation plan inside Codex.
2. **ahe-ship calling in codex**: If in Plan Mode, the Codex host exits Plan Mode and replays the command. Outside Plan Mode, Codex saves the plan to `.plans/` and stops.
3. **ahe-ship calling in antigravity**: Antigravity refreshes the saved plan against current code, executes it, and cleans it up.

### `ahe fix` Flow
1. **Error Encountered**: A test fails or intent changes after execution.
2. **ahe-fix calling**: You type `ahe fix` (or `ahe fix stale tests`) in Codex.
3. **Fix Plan Creation**: It generates a dedicated fix plan in `.plans/` ready for Antigravity to refresh and execute.

### General `ahe` Flow
1. **Ongoing Work**: You need to implement a feature or update docs.
2. **ahe calling**: You type `ahe` or a specific query like `ahe update product spec` in Codex.
3. **Automatic Routing**: `ahe-think` evaluates your request and automatically routes it to the right agent (like `ahe-solve` or `ahe-harness`).

## Installed Skills

| Skill | Role |
| --- | --- |
| `ahe` | Top-level user-facing continuation skill that routes exact `ahe` and `ahe` query forms through `ahe-think`. |
| `ahe-new` | New-start workflow that prepares the workspace and hands product/tracking work to `ahe-harness`. |
| `ahe-think` | Centered internal router that judges what is missing and chooses the next agent. |
| `ahe-review` | Review agent for repo code, harness state, and CodeGraph context. |
| `ahe-converse` | Clarification agent for recursive user conversation. |
| `ahe-harness` | Harness-management agent for product docs, instructions, feature tracking, todo sync, and compression-aware maintenance. |
| `ahe-feature` | Internal helper for deriving feature-list entries from product context. |
| `ahe-fix` | Independent fix planner that writes `.plans/{plan_name}.md` for errors or changed user intent. |
| `ahe-solve` | Feature-solving agent that divides and plans implementation work. |
| `ahe-compress` | Internal helper that detects oversized harness files before broad reads. |
| `ahe-overview` | Explains the AHE concept, entrypoints, and main workflows in chat with Mermaid diagrams. |
| `ahe-ship` | In Codex: saves Plan Mode plan to `.plans/`. In Antigravity: refreshes and executes exactly one plan from `.plans/`. |

## Routing Model

The Codex-side model is centered but flexible:

- exact `ahe` -> `ahe-think` -> `ahe-review | ahe-converse | ahe-harness | ahe-solve`
- `ahe <query>` or `<query> ahe` -> `ahe-think` -> `ahe-review | ahe-converse | ahe-harness | ahe-solve`
- exact `ahe new` -> dedicated new-start workflow first, then `ahe-harness`
- exact `ahe ship` -> independent plan-export workflow (Codex) or execution workflow (Antigravity)
- exact `ahe fix`, `ahe fix <query>`, or `<query> ahe fix` -> independent fix-plan workflow

- `ahe-think` is the center of judgment.
- Worker agents can call each other directly when that is the logical next
  action.
- Typical direct handoffs are `ahe-harness -> ahe-converse`,
  `ahe-solve -> ahe-review`, and `ahe-review -> ahe-harness`.

## Query Examples

- `ahe`
- `ahe new`
- `ahe ship`
- `ahe fix`
- `ahe fix stale tests`
- `stale tests ahe fix`
- `ahe compress`
- `compress ahe`
- `ahe update product spec`
- `ahe add dashboard export feature`

Only exact `ahe`, exact `ahe new`, exact `ahe-new`, exact `$ahe-new`, and
exact `ahe ship`, exact `ahe-ship`, exact `$ahe-ship`, exact `ahe fix`, exact
exact `ahe-fix`, exact `$ahe-fix`, `ahe fix <query>`, `<query> ahe fix`,
`ahe-overview`, `ahe <query>`, and `<query> ahe` activate the hook.
Middle mentions that do not fit those command shapes do not.
