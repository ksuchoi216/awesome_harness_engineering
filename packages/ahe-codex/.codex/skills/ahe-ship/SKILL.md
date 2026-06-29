---
name: ahe-ship
description: Export the latest Codex Plan Mode `<proposed_plan>` into `.plans/{plan_name}.md` with compact handoff context for another LLM. Use when the user explicitly invokes `$ahe-ship`, `ahe-ship`, or `ahe ship` after a plan has just been created and wants a portable plan file for Antigravity or another platform.
---

# AHE Ship

`ahe-ship` is a user-facing AHE command, but it is independent from the AHE
agent network.

Use this skill only to export a completed Codex Plan Mode plan into a handoff
file. Do not route through `ahe-thinker`. You must not call `ahe-harness`,
`ahe-solver`, or any other AHE workflow agent.

## Workflow

1. Locate the most recent completed `<proposed_plan>` already visible in the
   current conversation.
2. If the latest plan is clear, use it directly. Do not ask the user to paste
   the plan again.
3. Derive `plan_name` from the plan title. Use a short lowercase hyphenated
   name. If no title or safe name can be derived, ask one focused question for
   the plan name.
4. Build a compact markdown handoff with these sections:
   - `# {Plan Title}`
   - `## Handoff Summary`
   - `## Source Plan`
   - `## Execution Context`
   - `## Assumptions`
   - `## Constraints`
   - `## Verification Plan`
   - `## Risks and Open Questions`
   - `## Instructions for Next Agent`
5. Write the final markdown through `scripts/write_plan.py`.
6. Report the created `.plans/{plan_name}.md` path.

## Missing Context

- If there is no recent `<proposed_plan>` in context, ask the user for the plan
  text instead of inventing one.
- If the target file already exists, ask whether to overwrite it or choose a
  distinct plan name.

## Writer Script

Use:

```bash
python3 .codex/skills/ahe-ship/scripts/write_plan.py \
  --root "$PWD" \
  --plan-name "Plan Title" \
  < /tmp/ahe-plan.md
```

Add `--overwrite` only after the user explicitly confirms replacing an existing
file.
