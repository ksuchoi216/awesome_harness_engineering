---
name: ship
description: Use when the user explicitly invokes `$ship`, `ship`, or `ahe ship` after a plan has just been created and wants Codex to save it, run it through Antigravity, and clean it up only after verified completion.
---

# AHE Ship

`ship` is a user-facing AHE command, but it is independent from the AHE
agent network.

Use this skill only to export a completed Codex Plan Mode plan, trigger its
execution through Antigravity, and keep cleanup tied to verified completion.
Do not route through `think`. You must not call `harness`, `solve`, or any
other AHE workflow agent.

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
6. Run `ahe-antigravity ahe-ship .plans/{plan_name}.md` from the active repository.
7. Report one of these outcomes only:
   - verified completion removed `.plans/{plan_name}.md`
   - execution did not verify completion, so `.plans/{plan_name}.md` was kept

## Missing Context

- If there is no recent `<proposed_plan>` in context, ask the user for the plan
  text instead of inventing one.
- If the target file already exists, ask whether to overwrite it or choose a
  distinct plan name.
- If Antigravity execution fails, is partial, or does not emit
  `AHE_PLAN_COMPLETE`, keep the plan file in `.plans/`.

## Writer Script

Use:

```bash
python3 .codex/skills/ship/scripts/write_plan.py \
  --root "$PWD" \
  --plan-name "Plan Title" \
  < /tmp/ahe-plan.md
```

Add `--overwrite` only after the user explicitly confirms replacing an existing
file.

After the file is written, run:

```bash
ahe-antigravity ahe-ship ".plans/{plan_name}.md"
```

Treat execution as verified success only when Antigravity emits the exact line
`AHE_PLAN_COMPLETE`.
