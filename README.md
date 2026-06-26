# Awesome Harness Engineering (AHE)

AHE installs global Codex skills that manage harness files through chat. The
public entrypoints stay small: use `ahe init` to start or reset harness work,
`ahe` to continue existing work, and `ahe <query>` for explicit AHE requests
such as `ahe compress feature-list`.

## Installed Skills

| Skill | Role |
| --- | --- |
| `ahe-init` | New-start workflow that prepares the workspace and hands product/tracking work to `ahe-harness`. |
| `ahe-thinker` | Centered internal router that judges what is missing and chooses the next agent. |
| `ahe-reviewer` | Review agent for repo code, harness state, and CodeGraph context. |
| `ahe-conversator` | Clarification agent for recursive user conversation. |
| `ahe-harness` | Harness-management agent for product docs, instructions, feature tracking, todo sync, and compression-aware maintenance. |
| `ahe-solver` | Feature-solving agent that divides and plans implementation work. |
| `ahe-compression` | Internal helper that detects oversized harness files before broad reads. |

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
- `ahe init`
- `ahe compress feature-list`
- `ahe update product spec`
- `ahe add dashboard export feature`

Only exact `ahe`, exact `ahe init`, exact `ahe-init`, exact `$ahe-init`, and
explicit `ahe <query>` activate the hook. Broad non-prefixed prompts do not.
