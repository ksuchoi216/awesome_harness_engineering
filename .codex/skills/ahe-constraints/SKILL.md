---
name: ahe-constraints
description: Update docs/constraints.md for project-specific implementation constraints.
---

# AHE Constraints

Use this skill when the user invokes `$ahe-constraints`.

## Command Workflow: ahe-constraints

- Read `docs/constraints.md` if it exists.
- Engage in an interactive conversation with the user to clarify and document project constraints:
  - Ask clarifying questions about technical limits, environment constraints, and rules.
  - Draft suggestions for the constraint definitions in chat and ask for user approval.
  - Recursively ask for feedback or additional constraints until the details are clear and approved.
- Once finalized, update `docs/constraints.md`.
- Keep `PROGRESS.md` and `SESSION-HANDOFF.md` aligned when constraints change active work.

## Clarification Rule

When required information is missing, follow the `ahe-ask-user` protocol. Ask again recursively using a Codex-supported structured response request, provide 2-3 meaningful mutually exclusive options when possible, and allow custom input when predefined options are not enough.

### User Response Target

- Collect clear project constraints for `docs/constraints.md`.

### Questions to Ask

- Ask what rule, limit, or required practice should be documented.
- Ask why the constraint exists when that is not obvious.
- Ask whether the constraint is mandatory or a preference when needed.

### Clarification Criteria

- The answer must describe the rule and its practical meaning.
- The answer must be specific enough that another engineer can follow the constraint without guessing.

### Re-ask When

- Ask again when the answer is vague, contradictory, or only names a topic without the actual rule.
- Ask again when the operational meaning of the constraint is still unclear.
