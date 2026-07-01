---
name: ahe-feature
description: Internal AHE workflow skill for creating right-sized feature-list.json entries from product context.
---

# AHE Feature

This is an internal AHE workflow skill, not a user-facing command.
Use it when `ahe-think` or another worker decides that feature sizes must be evaluated or when generating new features from product context.

## Command Workflow: ahe-feature

### Feature Generation and Sizing

- Derive concrete feature items from only the active product stage (e.g. `docs/product1.md`), not future stages.
- Create right-sized `feature-list.json` entries from product context.
- Avoid tiny task fragments. A feature should represent a meaningful, verifiable unit of work.
- Avoid vague, oversized features. Break large epics down into testable, implementable features.
- If product context is insufficient to create right-sized features, use `ahe-converse` to ask the user for clarification.
- Update `feature-list.json` with the newly derived, well-sized features.
- Ensure that features are actionable and have clear success criteria based on the product documentation.

### Clarification Rule

When feature sizing or extraction is ambiguous, follow the `ahe-think` protocol first. If `ahe-think` finds missing information, follow the `ahe-converse` protocol to ask the user for the exact missing detail.
