---
name: ahe-thinker
description: Internal AHE orchestration protocol for routing exact `ahe` and explicit `ahe <query>` requests through the AHE agent network.
---

# AHE Thinker

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$ahe-thinker` as a user command.
Use it as the central decision layer for AHE work.

## Purpose

- Judge what is missing before another agent acts.
- Judge the active `project`, `feature`, or `sub-feature`.
- Decide which of `Why`, `What`, and `How` are still missing.
- Choose the next internal agent: `ahe-reviewer`, `ahe-conversator`,
  `ahe-harness`, or `ahe-solver`.
- Receive each agent result, reassess the state, and decide the next step.

## Routing Inputs

- Exact `ahe` means continue existing harness work.
- Exact `ahe init`, exact `ahe-init`, and exact `$ahe-init` stay on the
  `$ahe-init` path.
- Explicit `ahe <query>` means route the query through `ahe-thinker`.
- Broad non-prefixed prompts must not activate AHE.

## Size Preflight

- Before reading full harness files, run
  `sh .codex/skills/ahe-compression/scripts/check-harness-size.sh`.
- If the detector exits with `COMPRESSION_REQUIRED` or code `2`, call
  `ahe-compression` before normal routing.
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
  CodeGraph context, call `ahe-reviewer`.
- If the need is user clarification, call `ahe-conversator`.
- If the need is updating harness artifacts, product docs, feature tracking,
  todo sync, or compression of completed history, call `ahe-harness`.
- If the need is solving or decomposing feature work, call `ahe-solver`.

## Interaction Model

- `ahe-thinker` is centered, but direct worker-to-worker calls are allowed when
  they are the obvious next step.
- Typical loops:
  - `ahe-thinker -> ahe-reviewer -> ahe-thinker`
  - `ahe-thinker -> ahe-harness -> ahe-thinker`
  - `ahe-thinker -> ahe-conversator -> ahe-thinker`
  - `ahe-thinker -> ahe-solver -> ahe-thinker`
- Allowed direct handoffs include:
  - `ahe-harness -> ahe-conversator`
  - `ahe-solver -> ahe-reviewer`
  - `ahe-reviewer -> ahe-harness`
- Every handoff must state the goal, reason, relevant files or context, and the
  expected result.

## Broad Intent Routing

- Use `ahe-reviewer` for review-first requests.
- Use `ahe-harness` for product, instructions, progress, feature-list, todo, or
  compression maintenance.
- Use `ahe-solver` for feature implementation planning or execution work.
- Use `ahe-conversator` when no safe next step exists without user input.

## Completion

- Continue to the next skill or next unfinished feature until the active unit is
  resolved.
- Keep `docs/product.md` as overview context and `feature-list.json` as a
  derived tracker.
- Derive features from only the active product stage.
- Advance from one numbered product stage to the next only after all
  feature-list items derived from the current active stage are `done`.
