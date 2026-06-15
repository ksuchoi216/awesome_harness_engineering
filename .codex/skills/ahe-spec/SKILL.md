---
name: ahe-spec
description: Internal AHE specification workflow for updating product and instructions docs.
---

# AHE Spec

This is an internal AHE workflow skill, not a user-facing command.

Do not treat `$ahe-spec` as a user command.
Use it after `ahe-thinking` decides that specification work must continue.

## Command Workflow: ahe-spec

### Spec Inspection

- Read `docs/PRODUCT.md` if it exists.
- Read `docs/INSTRUCTIONS.md` if it exists.
- Read `AGENTS.md`, `feature-list.json`, `PROGRESS.md`, and `SESSION-HANDOFF.md`.

### Sequential Spec Conversation Flow

- `docs/PRODUCT.md` is the canonical home for product specification details collected during `ahe init`.
- Clarify product goal, scope, and success criteria when `docs/PRODUCT.md` needs to change.
- Clarify project instructions when `docs/INSTRUCTIONS.md` needs to change.
- Draft the relevant specification updates in chat and ask for user approval.
- Ask recursively for more detail until the affected specification areas are clear and approved.

### Spec Completion

- Write product behavior, scope, requirements, success criteria, and workflow details into `docs/PRODUCT.md`.
- `docs/PRODUCT.md` is the canonical source of truth. Concrete feature items for `feature-list.json` must be derived from it only after it has been populated.
- Do not move product specification details into `AGENTS.md`.
- Update only the relevant docs among `docs/PRODUCT.md` and `docs/INSTRUCTIONS.md`.
- When updating `docs/INSTRUCTIONS.md`, only allow additions/removals/edits to instructions inside `## CAN CHANGE INSTRUCTIONS`; preserve `## MUST NOT CHANGE INSTRUCTIONS`.
- Update `.ahe/process_status.json`.
- Update `PROGRESS.md` and `SESSION-HANDOFF.md` when specification changes affect active work.

## Clarification Rule

When the next specification step is not clear, follow the `ahe-thinking` protocol first. If `ahe-thinking` finds missing information, follow the `ahe-conversation` protocol. Ask again recursively using a Codex-supported structured response request, provide 2-3 meaningful mutually exclusive options when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect the product or instructions details required to update the relevant specification docs.

### Questions to Ask

- Ask who the product is for and what problem it solves when product intent is unclear.
- Ask what behavior, scope boundaries, and success criteria should be documented.
- Ask what rule, practice, or guideline should be documented as an instruction.

### Clarification Criteria

- The answer must identify the target user, product goal, main behavior, scope, and success signal when product details are changing.
- The answer must describe any instruction and its practical meaning clearly enough that another engineer can follow it.
- The answer must be concrete enough to update the relevant specification docs without guessing missing intent.

### Re-ask When

- Ask again when the answer is vague, contradictory, or incomplete.
- Ask again when the response gives features without explaining the user goal or success criteria.
- Ask again when the response names an instruction topic without the actual rule.
