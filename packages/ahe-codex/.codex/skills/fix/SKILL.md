---
name: ahe-fix
description: Create a concrete `.plans/{plan_name}.md` fix plan for errors, bugs, or user-intent changes. Use when the user explicitly invokes `$fix`, `fix`, `ahe fix`, `ahe fix <query>`, or `<query> ahe fix`, and call `converse` when the plan needs clarification.
---

# AHE Fix

`fix` is a user-facing AHE command for creating a fix plan. It is separate
from the normal `ahe` continuation workflow, including the thinker-routed
`ahe <query>` and `<query> ahe` forms.

Use this skill when the user wants a plan for fixing errors or following their
current intention when it differs from the previous AHE flow.

## Workflow

1. Inspect the current conversation and relevant repository context.
2. Identify the fix target:
   - error, failure, regression, or broken behavior to repair.
   - user intention that differs from the existing AHE direction.
3. If the fix goal, scope, or success criteria are unclear, call
   `converse` and ask one focused question before writing the plan.
4. Derive `plan_name` from the fix goal. Use a short lowercase hyphenated name.
   If no safe name can be derived, ask one focused question for the plan name.
5. Build a compact markdown plan with these sections:
   - `# {Fix Plan Title}`
   - `## Fix Goal`
   - `## Current Evidence`
   - `## Assumptions`
   - `## Scope`
   - `## Steps`
   - `## Verification Plan`
   - `## Risks and Open Questions`
   - `## Instructions for Next Agent`
6. Write the final markdown through `scripts/write_fix_plan.py`.
7. Report the created `.plans/{plan_name}.md` path.

## Missing Context

- If the requested fix is ambiguous, use `converse` instead of guessing.
- If the target file already exists, ask whether to overwrite it or choose a
  distinct plan name.
- Do not update `feature-list.json`, `progress.md`, or `session-handoff.md`
  for a normal fix-plan export unless the user explicitly asks for harness
  tracking changes too.

## Writer Script

Use:

```bash
python3 .codex/skills/fix/scripts/write_fix_plan.py \
  --root "$PWD" \
  --plan-name "Fix Plan Title" \
  < /tmp/fix-plan.md
```

Add `--overwrite` only after the user explicitly confirms replacing an existing
file.
