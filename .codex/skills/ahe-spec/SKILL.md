---
name: ahe-spec
description: Update product, constraints, and architecture docs through one recursive specification conversation.
---

# AHE Spec

Use this skill when the user invokes `$ahe-spec`.

## Command Workflow: ahe-spec

### Spec Inspection

- Read `docs/PRODUCT.md` if it exists.
- Read `docs/constraints.md` if it exists.
- Read `docs/achitecture.md` if it exists.
- Read `AGENTS.md`, `feature-list.json`, `PROGRESS.md`, and `SESSION-HANDOFF.md`.

### Sequential Spec Conversation Flow

- Clarify product goal, scope, and success criteria when `docs/PRODUCT.md` needs to change.
- Clarify project constraints when `docs/constraints.md` needs to change.
- Clarify architecture direction when `docs/achitecture.md` needs to change.
- Draft the relevant specification updates in chat and ask for user approval.
- Ask recursively for more detail until the affected specification areas are clear and approved.

### Spec Completion

- Update only the relevant docs among `docs/PRODUCT.md`, `docs/constraints.md`, and `docs/achitecture.md`.
- Update `.ahe/process_status.json`.
- Update `PROGRESS.md` and `SESSION-HANDOFF.md` when specification changes affect active work.

## Clarification Rule

When required information is missing, follow the `ahe-conversation` protocol. Ask again recursively using a Codex-supported structured response request, provide 2-3 meaningful mutually exclusive options when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect the product, constraint, or architecture details required to update the relevant specification docs.

### Questions to Ask

- Ask who the product is for and what problem it solves when product intent is unclear.
- Ask what behavior, scope boundaries, and success criteria should be documented.
- Ask what rule, limit, or required practice should be documented as a constraint.
- Ask about the technical stack, major components, interfaces, or data flow when architecture direction is unclear.

### Clarification Criteria

- The answer must identify the target user, product goal, main behavior, scope, and success signal when product details are changing.
- The answer must describe any constraint and its practical meaning clearly enough that another engineer can follow it.
- The answer must identify the stack, components, or decision direction clearly enough to document the architecture.
- The answer must be concrete enough to update the relevant specification docs without guessing missing intent.

### Re-ask When

- Ask again when the answer is vague, contradictory, or incomplete.
- Ask again when the response gives features without explaining the user goal or success criteria.
- Ask again when the response names a constraint topic without the actual rule.
- Ask again when component responsibilities or the overall architecture direction are still unclear.
