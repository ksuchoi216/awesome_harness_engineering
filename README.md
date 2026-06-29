# Awesome Harness Engineering (AHE)

AHE installs global Codex and Antigravity skills that manage harness files through chat. The repository uses a one-package, two-internal-packages layout (`packages/ahe-codex` and `packages/ahe-antigravity`) shipped as a single npm package. The
public entrypoints stay small: use `ahe new` to start or reset harness work,
`ahe` to continue existing work, `ahe ship` to save the latest plan,
`ahe fix` to create a `.plans` fix plan, and
`ahe <query>` or `<query> ahe` for explicit AHE requests such as `ahe compress`
or `compress ahe`.

## Installed Skills

| Skill | Role |
| --- | --- |
| `ahe-new` | New-start workflow that prepares the workspace and hands product/tracking work to `ahe-harness`. |
| `ahe-think` | Centered internal router that judges what is missing and chooses the next agent. |
| `ahe-review` | Review agent for repo code, harness state, and CodeGraph context. |
| `ahe-converse` | Clarification agent for recursive user conversation. |
| `ahe-harness` | Harness-management agent for product docs, instructions, feature tracking, todo sync, and compression-aware maintenance. |
| `ahe-fix` | Independent fix planner that writes `.plans/{plan_name}.md` for errors or changed user intent. |
| `ahe-solve` | Feature-solving agent that divides and plans implementation work. |
| `ahe-compress` | Internal helper that detects oversized harness files before broad reads. |
| `ahe-ship` | Independent exporter that writes the latest Codex Plan Mode plan to `.plans/*.md` and stops there. |

## Routing Model

The Codex-side model is centered but flexible:

- exact `ahe` -> `ahe-think` -> `ahe-review | ahe-converse | ahe-harness | ahe-solve`
- `ahe <query>` or `<query> ahe` -> `ahe-think` -> `ahe-review | ahe-converse | ahe-harness | ahe-solve`
- exact `ahe new` -> dedicated new-start workflow first, then `ahe-harness`
- exact `ahe ship` -> independent plan-export workflow
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
`ahe-fix`, exact `$ahe-fix`, `ahe fix <query>`, `<query> ahe fix`,
`ahe <query>`, and `<query> ahe` activate the hook.
Middle mentions that do not fit those command shapes do not.
