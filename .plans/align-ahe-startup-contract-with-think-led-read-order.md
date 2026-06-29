# Align AHE Startup Contract With Think-Led Read Order

## Handoff Summary

Align AHE's Codex-side startup contract so `think` is the explicit decision-maker, copied harness files are checked before reading, and the startup read order follows the user's required file sequence. Canonicalize the artifact names around `AGENTS.md`, `docs/product.md`, `docs/product{n}.md`, `docs/architecture.md`, `docs/instructions.md`, `init.sh`, `feature-list.json`, `status.json`, `progress.md`, and `session-handoff.md`.

## Source Plan

# Align AHE Startup Contract With Think-Led Read Order

## Summary

Update AHE so `think` is the explicit decision-maker for Codex-side AHE work, and change the startup contract to:

1. verify copied harness files first
2. read files strictly in this order:
   `AGENTS.md` -> `docs/product.md` plus `docs/product{n}.md` -> `docs/architecture.md` -> `docs/instructions.md` -> `init.sh` -> `feature-list.json` -> `status.json` -> `progress.md` -> `session-handoff.md`

Use the user-provided names as the new canonical contract, including a new root `status.json`.

## Key Changes

- Canonicalize the startup/read contract across AHE docs, skills, templates, hook context, and tests.
  - `think` must explicitly own “what to do next” decisions.
  - startup instructions must say “check whether the copied files are correct” before reading contents
  - `product.md` must be treated as overview context, and after reading all relevant docs, `product1.md`, `product2.md`, and later numeric stages must be checked in order
  - `architecture.md`, `instructions.md`, and `session-handoff.md` must be explicitly named in the startup order, not left implicit

- Replace the status-file contract.
  - promote workspace-root `status.json` to the canonical tracked status artifact
  - remove or migrate references that currently treat `.ahe/process_status.json` as the source of truth
  - keep read/write behavior simple: one canonical status file, no dual-source ambiguity

- Fix copy/initialization behavior to match the new artifact contract.
  - template-copy logic must verify expected files and names before later read steps
  - generated workspace artifacts must use the canonical names from the new list
  - respect the existing constraint that only allowed sections are editable for instruction-style files rather than rewriting full documents wholesale

- Update the packaged AHE surface, not just repo-root notes.
  - priority files are:
    [packages/ahe-codex/.codex/skills/think/SKILL.md](/Users/KC/Codes/awesome_harness_engineering/packages/ahe-codex/.codex/skills/think/SKILL.md)
    [packages/ahe-codex/.codex/skills/new/SKILL.md](/Users/KC/Codes/awesome_harness_engineering/packages/ahe-codex/.codex/skills/new/SKILL.md)
    [packages/ahe-codex/.codex/ahe-shared/templates/AGENTS.md](/Users/KC/Codes/awesome_harness_engineering/packages/ahe-codex/.codex/ahe-shared/templates/AGENTS.md)
  - then align related product docs, installer/setup behavior, and contract tests with the same naming and order

## Public Contract Changes

- Startup artifact order becomes explicit and mandatory.
- `status.json` becomes a required root artifact.
- `think` becomes the documented brain/decision layer for Codex AHE routing.
- `docs/product.md` remains overview, while `docs/product{n}.md` are checked as ordered stages after the broader docs pass.

## Test Plan

- Update contract tests that currently assert old names such as `docs/PRODUCT.md`, uppercase tracking files, or `.ahe/process_status.json`.
- Add or update tests for:
  - startup order includes copy-verification first
  - `think` is the central decision skill for `ahe <query>` and related Codex routing
  - `status.json` is the canonical status artifact
  - numbered product docs are checked in numeric order after the main docs context is read
  - initialization copies the expected artifacts with the new names
- Run at minimum:
  - `./init.sh`
  - `pytest tests/ -x`
  - focused setup/routing tests for startup, hook routing, and project setup

## Assumptions

- The user’s listed filenames and order override the repo’s current mixed casing and legacy naming.
- `status.json` fully replaces `.ahe/process_status.json` rather than coexisting as a second source of truth.
- Changes should be kept narrow and readability-first: align contracts, names, and tests without redesigning unrelated AHE behavior.

## Execution Context

- Repository: `/Users/KC/Codes/awesome_harness_engineering`
- User explicitly wants the `ship` workflow and provided the skill contract.
- This plan follows the latest completed `<proposed_plan>` already present in the conversation.
- Current repo state observed during planning:
  - root `AGENTS.md`, `init.sh`, and `feature-list.json` exist
  - root `PROGRESS.md` and `SESSION-HANDOFF.md` exist, while lowercase `progress.md` and `session-handoff.md` do not
  - `docs/PRODUCT.md` exists, while lowercase `docs/product.md` and root `status.json` do not
  - current tracked status file is `.ahe/process_status.json`
  - packaged Codex skills live under `packages/ahe-codex/.codex/skills/`

## Assumptions

- The latest plan title is safe to use as the basis for the plan file name.
- The next agent should update both repo-root guidance and packaged AHE contracts so behavior and tests stay aligned.
- If any legacy-name compatibility is required for rollout safety, it should be implemented intentionally rather than left implicit.

## Constraints

- Follow the user’s requested canonical file names and read order.
- Keep scope tight to startup-contract alignment; do not redesign unrelated AHE flows.
- Do not route through `think`, `harness`, `solve`, or other AHE agents during ship execution.
- Preserve template-protection rules and only edit allowed sections in instruction-style artifacts where applicable.
- Verified success requires Antigravity to emit the exact line `AHE_PLAN_COMPLETE`.

## Verification Plan

- Confirm plan file creation under `.plans/` with the sanitized title-based filename.
- Execute `ahe-antigravity ahe-ship .plans/align-ahe-startup-contract-with-think-led-read-order.md`.
- Treat the run as verified success only if Antigravity emits `AHE_PLAN_COMPLETE` and the plan file is removed.
- If execution fails, is partial, or lacks the marker, keep the plan file for manual follow-up.

## Risks and Open Questions

- The repo currently contains mixed old and new naming contracts, so changes may touch more tests and docs than the user-facing request suggests.
- Existing references to `.ahe/process_status.json` are widespread; replacing them with root `status.json` may require careful coordinated updates.
- Antigravity execution may fail outside a fully configured environment even when the saved plan is valid.

## Instructions for Next Agent

Implement the plan exactly as written. Start from the packaged Codex contract files, then align repo-root documentation and tests to the same startup ordering and naming rules. Keep the implementation readable and narrow, favor direct naming and simple control flow, and verify with the targeted startup/routing tests plus `pytest tests/ -x` before claiming completion.
