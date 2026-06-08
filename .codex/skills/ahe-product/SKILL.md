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

If a user answer needs clarification or a more detailed description, ask question recursively to clarify the response, and use this exact prompt:

Question: {question}
Please choose one option:

1. Yes

2. No

3. Custom input

Enter 1, 2, or type your own answer:
