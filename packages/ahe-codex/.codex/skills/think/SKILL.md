---
name: think
description: Internal AHE orchestration protocol for routing exact `ahe` and explicit `ahe <query>` requests through the AHE agent network.
---

# AHE Thinker

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$think` as a user command.
Use it as the central decision layer for AHE work.

## Purpose

- Judge what is missing before another agent acts.
- Judge the active `project`, `feature`, or `sub-feature`.
- Decide which of `Why`, `What`, and `How` are still missing.
- Choose the next internal agent: `review`, `converse`,
  `harness`, or `solve`.
- Receive each agent result, reassess the state, and decide the next step.

## Routing Inputs

- Exact `ahe` means continue existing harness work.
- Exact `ahe init`, exact `new`, and exact `$new` stay on the
  `$new` path.
- Explicit `ahe <query>` means route the query through `think`.
- Broad non-prefixed prompts must not activate AHE.

## Size Preflight

- Before reading full harness files, run
  `sh .codex/skills/compress/scripts/check-harness-size.sh`.
- If the detector exits with `COMPRESSION_REQUIRED` or code `2`, call
  `compress` before normal routing.
- Do not read oversized harness files wholesale before compression routing is
  settled.

## Decision Rules

- For a `project`, require `Why`, `What`, and `How` by default.
- For a `feature` or `sub-feature`, require only the minimum of `Why`, `What`,
  and `How` needed to proceed safely.
- Read all existing `docs/*.md` files before choosing product work.
- Treat `docs/product.md` as overview context.
- Treat only `docs/product{number}.md` files as ordered product stages, starting
  with `docs/product1.md` and then `docs/product2.md`.
- Ignore non-numeric product docs such as `docs/product-alpha.md` for stage
  ordering.
- Choose the active product source as the lowest-numbered stage whose derived
  feature work is not complete, or `docs/product.md` when no numbered stage
  exists.
- If the need is understanding repo code, harness drift, progress evidence, or
  CodeGraph context, call `review`.
- If the need is user clarification, call `converse`.
- If the need is updating harness artifacts, product docs, feature tracking,
  todo sync, or compression of completed history, call `harness`.
- If the need is solving or decomposing feature work, call `solve`.

## Interaction Model

- `think` is centered, but direct worker-to-worker calls are allowed when
  they are the obvious next step.
- Typical loops:
  - `think -> review -> think`
  - `think -> harness -> think`
  - `think -> converse -> think`
  - `think -> solve -> think`
- Allowed direct handoffs include:
  - `harness -> converse`
  - `solve -> review`
  - `review -> harness`
- Every handoff must state the goal, reason, relevant files or context, and the
  expected result.

## Broad Intent Routing

- Use `review` for review-first requests.
- Use `harness` for product, instructions, progress, feature-list, todo, or
  compression maintenance.
- Use `solve` for feature implementation planning or execution work.
- Use `converse` when no safe next step exists without user input.

## Completion

- Continue to the next skill or next unfinished feature until the active unit is
  resolved.
- Keep `docs/product.md` as overview context and `feature-list.json` as a
  derived tracker.
- Derive features from only the active product stage.
- Advance from one numbered product stage to the next only after all
  feature-list items derived from the current active stage are `done`.
