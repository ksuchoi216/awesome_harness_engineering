---
name: ahe-thinking
description: Internal AHE orchestration protocol for deciding what to clarify, what to execute, and what to do next.
---

# AHE Thinking

This is an internal AHE protocol skill, not a user-facing command.

Do not treat `$ahe-thinking` as a user command.
Use it before and between AHE workflow actions when the next safe step is not
already obvious.

## Purpose

- Judge what is missing before another AHE workflow acts.
- Decide whether the current unit is clear enough to execute safely.
- Call `ahe-conversation` only when clarification is still needed.
- Continue to the next skill or next unfinished feature when the path is clear.

## Units of Work

Inspect the current unit as `project`, `feature`, or `sub-feature`.

- `project`: overall goal, target user, expected outcome, and delivery
  direction.
- `feature`: one concrete capability or work item under the project.
- `sub-feature`: one smaller capability or step under a feature.

## Clarity Judgment

Judge the current unit against `Why`, `What`, and `How`.

- `Why`: why this unit matters, what problem it solves, or what purpose it
  serves.
- `What`: what result, behavior, or output should be built.
- `How`: how the work should be approached when methodology or architecture
  matters.

### Project Rule

For a `project`, require `Why`, `What`, and `How` by default before moving
forward.

### Feature Rule

For a `feature` or `sub-feature`, require only the minimum needed to proceed
safely.

- If the feature is already clear from the project context, do not ask all
  three again.
- If only the result is missing, ask only `What`.
- If the feature goal is clear but the implementation direction is risky or
  materially different, ask `How`.
- If the feature exists but its purpose is unclear, ask `Why`.

## Next-Step Decision

- If `docs/PRODUCT.md` or `docs/INSTRUCTIONS.md` is missing or empty, classify the state as
  `harness engineering not enough` and prioritize product/instructions specification work.
- `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md` form the required harness contract. `docs/PRODUCT.md` is the product/specification source of truth, and
  `feature-list.json` is a derived tracker. Do not write specific feature items
  to `feature-list.json` until `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md` are established.
- If other harness essentials are missing or inconsistent, classify the state as
  `harness engineering not enough` and continue the harness-building workflow.
- If the harness exists and there is unfinished tracked work, classify the
  state as `in the middle of building features` and continue the first safe
  unfinished feature.
- If tracked work is complete and no obvious essential harness gap remains,
  classify the state as `completed all` and ask for the next task.

## Broad User Intent Routing

When the user provides a broad natural-language work intent (e.g., "add features", "update spec"), use their original prompt to determine the exact path:
- Route **product/spec changes** to `ahe-spec`.
- Route **instruction changes** to `ahe-spec`.
- Route **feature/todo tracking** to `ahe-update`.
- Route **unclear AHE work** to `ahe-conversation` and ask exactly one detail question before editing if the request is vague.

## Conversation Handoff

If clarity is missing, call `ahe-conversation` with the exact missing `Why`,
`What`, or `How`.

- Explain which unit is blocked.
- Explain what answer will unlock the next action.
- Ask for only the minimum missing detail.
- When the path is clear, continue to the next skill or next unfinished feature.

## Execution Loop

Follow this loop whenever AHE is routing or continuing work:

`thinking -> conversation if needed -> execution -> thinking`

After execution, reassess the active unit before choosing the next step.
