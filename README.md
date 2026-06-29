# Awesome Harness Engineering (AHE)

AHE installs global Codex and Antigravity skills that manage harness files through chat. The repository uses a one-package, two-internal-packages layout (`packages/ahe-codex` and `packages/ahe-antigravity`) shipped as a single npm package. The
public entrypoints stay small: use `ahe new` to start or reset harness work,
`ahe` to continue existing work, `ahe fix` to create a `.plans` fix plan, and
`ahe <query>` for explicit AHE requests such as `ahe compress feature-list`.

## Installed Skills

| Skill | Role |
| --- | --- |
| `ahe-new` | New-start workflow that prepares the workspace and hands product/tracking work to `ahe-harness`. |
| `ahe-thinker` | Centered internal router that judges what is missing and chooses the next agent. |
| `ahe-reviewer` | Review agent for repo code, harness state, and CodeGraph context. |
| `ahe-conversator` | Clarification agent for recursive user conversation. |
| `ahe-harness` | Harness-management agent for product docs, instructions, feature tracking, todo sync, and compression-aware maintenance. |
| `ahe-fix` | Independent fix planner that writes `.plans/{plan_name}.md` for errors or changed user intent. |
| `ahe-solver` | Feature-solving agent that divides and plans implementation work. |
| `ahe-compression` | Internal helper that detects oversized harness files before broad reads. |
| `ahe-ship` | Independent exporter that writes the latest Codex Plan Mode plan to `.plans/*.md` for another LLM. |

## Routing Model

The internal model is centered but flexible:

`query -> ahe-thinker -> ahe-reviewer | ahe-conversator | ahe-harness | ahe-solver`

- `ahe-thinker` is the center of judgment.
- Worker agents can call each other directly when that is the logical next
  action.
- Typical direct handoffs are `ahe-harness -> ahe-conversator`,
  `ahe-solver -> ahe-reviewer`, and `ahe-reviewer -> ahe-harness`.

## Query Examples

- `ahe`
- `ahe new`
- `ahe ship`
- `ahe fix`
- `ahe compress feature-list`
- `ahe update product spec`
- `ahe add dashboard export feature`

Only exact `ahe`, exact `ahe new`, exact `ahe-new`, exact `$ahe-new`, and
exact `ahe ship`, exact `ahe-ship`, exact `$ahe-ship`, exact `ahe fix`, exact
`ahe-fix`, exact `$ahe-fix`, and explicit `ahe <query>` activate the hook.
Broad non-prefixed prompts do not.
