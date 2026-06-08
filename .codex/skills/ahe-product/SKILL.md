---
name: ahe-product
description: Update docs/PRODUCT.md through a recursive product-specification conversation.
---

# AHE Product

Use this skill when the user invokes `$ahe-product`.

## Command Workflow: ahe-product

### Product Inspection

- Read `docs/PRODUCT.md` if it exists.
- Read `AGENTS.md`, `feature-list.json`, `PROGRESS.md`, and `SESSION-HANDOFF.md`.

### Sequential Product Conversation Flow

- Ask for the product specification inputs needed to update `docs/PRODUCT.md`.
- Ask recursively for more detail until the product specification is clear.
- If the product specification is clear, finish writing `docs/PRODUCT.md`.

### Product Completion

- Update `docs/PRODUCT.md`.
- Update `.ahe/process_status.json`.
- Update `PROGRESS.md` and `SESSION-HANDOFF.md` when product scope changes.

## Clarification Rule

If a user answer needs clarification or a more detailed description, ask again recursively using a Codex-supported structured response request. Ask a short question, provide 2-3 meaningful mutually exclusive options when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect the product specification details required to update `docs/PRODUCT.md`.

### Questions to Ask

- Ask who the product is for.
- Ask what the main goal or problem is.
- Ask what the main behavior, scope boundaries, and success criteria should be.

### Clarification Criteria

- The answer must identify the target user, product goal, main behavior, scope, and a clear success signal.
- The answer must be concrete enough to write or update `docs/PRODUCT.md` without guessing missing product intent.

### Re-ask When

- Ask again when the answer is vague, contradictory, or incomplete.
- Ask again when the response gives features without explaining the user goal or success criteria.
