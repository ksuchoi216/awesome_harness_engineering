---
name: ahe-ship
description: Use when the user explicitly invokes `$ship`, `ship`, or `ahe ship` after a plan has just been created and wants Codex to save it.
---

# AHE Ship

`ship` is a user-facing AHE command, but it is independent from the AHE
agent network.

Use this skill only to export a completed Codex Plan Mode plan and save it to `.plans/`.
Do not route through `think`. You must not call `harness`, `solve`, or any
other AHE workflow agent.

## Workflow

1. Detect if the current conversation is still in Plan Mode.
2. If Plan Mode is active, exit Plan Mode first before continuing.
3. Locate the most recent completed `<proposed_plan>` already visible in the
   current conversation.
4. If the latest plan is clear, use it directly. Do not ask the user to paste
   the plan again.
5. Derive `plan_name` from the plan title. Use a short lowercase hyphenated
   name. If no title or safe name can be derived, ask one focused question for
   the plan name.
6. Build a compact markdown handoff with these sections:
   - `# {Plan Title}`
   - `## Handoff Summary`
   - `## Source Plan`
   - `## Execution Context`
   - `## Assumptions`
   - `## Constraints`
   - `## Verification Plan`
   - `## Risks and Open Questions`
   - `## Instructions for Next Agent`
7. Write the final markdown through `scripts/write_plan.py`.
8. Report that the plan was saved to `.plans/{plan_name}.md` and stop.

## Missing Context

- If there is no recent `<proposed_plan>` in context, ask the user for the plan
  text instead of inventing one.
- If the target file already exists, ask whether to overwrite it or choose a
  distinct plan name.

## Writer Script

Use:

```bash
python .codex/skills/ship/scripts/write_plan.py \
  --root "$PWD" \
  --plan-name "Plan Title" \
  < /tmp/ahe-plan.md
```

Add `--overwrite` only after the user explicitly confirms replacing an existing
file.
