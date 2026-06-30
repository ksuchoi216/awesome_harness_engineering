---
name: ahe-think
description: Internal AHE orchestration protocol for routing exact `ahe`, `ahe <query>`, and `<query> ahe` requests through the AHE agent network.
---

# AHE Thinker

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$ahe-think` as a user command.
Use it as the central decision layer for AHE work.

## Purpose

- Judge what is missing before another agent acts.
- Judge the active `project`, `feature`, or `sub-feature`.
- Decide which of `Why`, `What`, and `How` are still missing.
- Choose the next internal agent: `ahe-review`, `ahe-converse`,
  `ahe-harness`, or `ahe-solve`.
- Receive each agent result, reassess the state, and decide the next step.

## Routing Inputs

- Exact `ahe` means continue existing harness work.
- Exact `ahe init`, exact `ahe-new`, and exact `$ahe-new` stay on the
  `$ahe-new` path.
- `ahe <query>` and `<query> ahe` mean route the query through `ahe-think`.
- Broad non-prefixed prompts must not activate AHE.

## Size and Stale-Test Preflight

- Before reading full harness files, run
  `sh .codex/skills/ahe-compress/scripts/check-harness-size.sh`.
- Run the test-overlap detector `python .codex/skills/ahe-compress/scripts/detect_stale_tests.py`
  when the user's explicit AHE query is compression-oriented (e.g., `ahe compress`).
- Run both compression detectors before choosing the next compression step.
- If either detector exits with `COMPRESSION_REQUIRED` or code `2`, call
  `ahe-compress` before normal routing. However, `ahe-compress` must not delete tests directly;
  for test compression, `ahe-think` must decide whether the next step is `ahe-harness` for
  harness-file compaction, `ahe-review` for stale-test confirmation and keeper selection,
  or both in sequence.
- Do not read oversized harness files wholesale before compression routing is
  settled.

## Startup Contract

- Check whether the copied harness files are correct before reading their contents.
- Read files strictly in this order:
  `AGENTS.md` -> `docs/product.md` plus `docs/product{n}.md` -> `docs/architecture.md` -> `docs/instructions.md` -> `init.sh` -> `feature-list.json` -> `status.json` -> `progress.md` -> `session-handoff.md`
- `ahe-think` explicitly owns the "what to do next" decisions for Codex-side AHE work.

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
  CodeGraph context, call `ahe-review`.
- If the need is user clarification, call `ahe-converse`.
- If the need is updating harness artifacts, product docs, feature tracking,
  todo sync, or compression of completed history, call `ahe-harness`.
- If the need is solving or decomposing feature work, call `ahe-solve`.

## Interaction Model

- `ahe-think` is centered, but direct worker-to-worker calls are allowed when
  they are the obvious next step.
- Typical loops:
  - `ahe-think -> ahe-review -> ahe-think`
  - `ahe-think -> ahe-harness -> ahe-think`
  - `ahe-think -> ahe-converse -> ahe-think`
  - `ahe-think -> ahe-solve -> ahe-think`
  - `ahe-think -> ahe-harness-checker -> ahe-think`
- Allowed direct handoffs include:
  - `ahe-harness -> ahe-converse`
  - `ahe-solve -> ahe-review`
  - `ahe-review -> ahe-harness`
  - `ahe-harness -> ahe-harness-checker`
  - `ahe-new -> ahe-harness -> ahe-harness-checker`
- Every handoff must state the goal, reason, relevant files or context, and the
  expected result.

## Broad Intent Routing

- Use `ahe-review` for review-first requests.
- Use `ahe-harness` for product, instructions, progress, feature-list, todo, or
  compression maintenance.
- Use `ahe-solve` for feature implementation planning or execution work.
- Use `ahe-converse` when no safe next step exists without user input.

## Hard Editing Rule

- `AGENTS.md` and any `instructions.md` file may only be modified inside an explicitly changeable section.
- If no changeable section exists, AHE must ask via `ahe-converse` instead of editing.
- Reference and template folders must be strictly excluded from reads and edits per project rules.

## Completion

- Continue to the next skill or next unfinished feature until the active unit is
  resolved.
- Keep `docs/product.md` as overview context and `feature-list.json` as a
  derived tracker.
- Derive features from only the active product stage.
- Advance from one numbered product stage to the next only after all
  feature-list items derived from the current active stage are `done`.
