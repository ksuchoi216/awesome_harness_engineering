# Refresh Saved AHE Ship Plans Before Antigravity Execution

## Handoff Summary
Update the Antigravity-side `ahe-ship` flow so it refreshes a selected saved `.plans/{plan_name}.md` against the current repository state before any implementation work. The refreshed plan must overwrite the same saved file, and execution must proceed from that refreshed content rather than the stale original.

## Source Plan
# Refresh Saved AHE Ship Plans Before Antigravity Execution

## Summary
Change the Antigravity-side `ahe-ship` contract so it never executes a stale saved plan directly. When Antigravity picks a `.plans/{plan_name}.md` file, it must first reconcile that plan against the current repository state, rewrite the same plan file with the refreshed plan, and only then execute the refreshed version. This keeps the plan aligned with code changes made after the original Codex export.

## Implementation Changes
- Update the Antigravity skill contract in `packages/ahe-antigravity/skills/ahe-ship/SKILL.md`:
  - Add an explicit first step: inspect current code and refresh the selected saved plan before any other implementation work.
  - Require overwriting the same `.plans/{plan_name}.md` file with the refreshed plan.
  - Clarify that execution must use the refreshed plan, not the original stale text.
  - Keep the existing single-plan selection rule and post-success deletion rule.
- Update the Antigravity wrapper prompt in `packages/ahe-antigravity/bin/ahe-antigravity`:
  - Replace “execute this saved AHE plan exactly as written” with a refresh-first instruction.
  - Make the stdin prompt require: reconcile against current code, rewrite the selected plan file, then implement every requirement from the refreshed plan.
  - Preserve the `AHE_PLAN_COMPLETE` completion gate.
- Update user-facing docs that describe `ahe ship` / Antigravity behavior:
  - `README.md`
  - `docs/product.md`
  - Change wording from “execute saved plan” to “refresh saved plan against current code, then execute it”.
- Add or update focused contract tests:
  - `tests/test_ahe_antigravity_ship.py` should assert the wrapper prompt requires refresh-before-execute and no longer claims the saved plan is executed unchanged.
  - Add a skill-text contract assertion for the new refresh-first behavior in the Antigravity skill file.
  - Keep existing tests for one-plan-only selection, model pinning, completion marker, and deletion semantics.

## Public Contract Changes
- Antigravity `ahe-ship` behavior changes from:
  - “read selected saved plan and execute it”
- To:
  - “read selected saved plan, refresh it against the current repository state, overwrite the saved file with the refreshed plan, then execute the refreshed plan”
- Codex-side `ahe-ship` remains save-only; this change is on the Antigravity execution side.

## Test Plan
- Run focused tests for Antigravity ship behavior and prompt contract.
- Run shell syntax verification for `packages/ahe-antigravity/bin/ahe-antigravity`.
- Run the broader AHE ship/hook/project-setup tests if the prompt or documented contract changes affect shared expectations.

## Assumptions
- Default chosen: Antigravity rewrites the selected `.plans/{plan_name}.md` file before execution, rather than reconciling silently or failing on drift.
- The refreshed plan stays at the same path so existing cleanup logic and user workflow do not change.
- No Codex-side plan export changes are required unless later testing shows the docs or shared contract text depend on them.

## Execution Context
This plan was produced after inspecting the current AHE contracts in the repo and the installed Codex `ahe-ship` skill. Current repo behavior is split: Codex `ahe-ship` saves the latest completed `<proposed_plan>` into `.plans/`, while Antigravity `ahe-ship` executes one selected saved plan file. The requested change is to make Antigravity refresh the saved plan against current code before execution so the saved plan cannot drift behind later code updates.

## Assumptions
- The saved plan should be rewritten in place before execution.
- Exactly one plan file is still selected and executed.
- Codex-side export remains independent from `ahe-think` and other AHE workflow agents.

## Constraints
- Do not change the Codex-side `ahe-ship` into an execution workflow.
- Preserve the existing single-plan selection behavior in Antigravity.
- Preserve the `AHE_PLAN_COMPLETE` completion contract.
- Preserve plan-file deletion only after verified successful completion.
- Keep the change scoped to the requested refresh-before-execute behavior.

## Verification Plan
- Focused Antigravity ship contract tests for the prompt and completion behavior.
- Shell syntax check for `packages/ahe-antigravity/bin/ahe-antigravity`.
- Any additional ship-related shared-contract tests touched by doc or prompt wording changes.

## Risks and Open Questions
- The main risk is wording the refresh-first prompt too loosely, which would allow Antigravity to execute the old plan without rewriting it first.
- Shared docs and tests may still encode the older “execute saved plan as written” contract and need synchronized updates.
- No open product decision remains; the chosen default is rewrite-in-place before execution.

## Instructions for Next Agent
Implement the refresh-before-execute contract on the Antigravity side only. Update the Antigravity skill text, wrapper prompt, and any directly affected docs/tests so they consistently require: select one plan, reconcile it against current code, overwrite the same `.plans/{plan_name}.md` file with the refreshed plan, then execute the refreshed plan and delete it only after verified completion.
