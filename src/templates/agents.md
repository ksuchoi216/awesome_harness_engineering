# AGENTS.md
## PURPOSE
You can change only this section. except for this section, you MUST NOT change this file.
{{PROJECT_PURPOSE}}

## Startup Workflow

Before writing code:

1. **Confirm working directory** with `pwd`
2. **Read this file** completely
3. **Read project docs if present** (`docs/architecture.md`, `docs/product.md`, `docs/instructions.md`, `docs/*.md`, README, or equivalent)
   - especially, product.md and product{number}.md present explanation of what to do.
4. **Run `./init.sh`** to verify environment is healthy
5. **Read `feature_list.json`** to see current feature state
6. **Review recent commits** with `git log --oneline -5`

## Working Rules

- **One feature at a time**: Pick exactly one unfinished feature from `feature-list.json`
- **Verification required**: Don't claim done without running verification commands
- **Update artifacts**: Before ending session, update `progress.md` and `feature-list.json`
- **Stay in scope**: Don't modify files unrelated to the current feature
- **Leave clean state**: Next session must be able to run `./init.sh` immediately

## Default Environment

- Python project.
- Use the existing `.venv` through `./init.sh` unless a task explicitly requires another environment.
- Keep dependency installation conservative and non-destructive.

## Primary Verification Command

`./init.sh`

## Verification Commands

- Tests: `pytest tests/ -x`
- Type check: `mypy src/ --strict`
- Lint: `ruff check src/`
- Startup verification: `./init.sh`

## File Ownership   

- `AGENTS.md`: Project and agent operating instructions.
- `docs/PRODUCT.md`: Canonical product specification when created.
- `progress.md`: Session continuity log.
- `session-handoff.md`: End-of-session handoff notes.
- `feature-list.json`: Feature state tracker.
- `init.sh`: Standard startup and verification path.
- `.ahe/process_status.json`: AHE workflow state.

## Required Artifacts

- `feature-list.json` - Feature state tracker (source of truth)
- `progress.md` - Session continuity log
- `session-handoff.md` - Session handoff notes
- `init.sh` - Standard startup and verification path

## Definition of Done

A feature is done only when ALL of the following are true:

- [ ] Target behavior is implemented
- [ ] Required verification actually ran (tests / lint / type-check)
- [ ] Evidence recorded in `feature-list.json` or `progress.md`
- [ ] Repository remains restartable from standard startup path

## Handoff Rules

- Update `progress.md`
- Update `session-handoff.md`
- Update `feature-list.json` when feature status changes
- Record unresolved risks or blockers
- Leave repo clean enough for next session to run `./init.sh` immediately

## End of Session

Before ending a session:

1. Update `progress.md` with current state
2. Update `feature-list.json` with new feature status
3. Record any unresolved risks or blockers
4. Commit with descriptive message once work is in safe state
5. Leave repo clean enough for next session to run `./init.sh` immediately

## Do Not Do

- Do not add features beyond what was asked.
- Do not refactor unrelated code.
- Do not overwrite user or agent work outside the current feature.
- Do not delete existing worktree changes unless explicitly requested.
- Do not claim verification passed unless the command actually ran and passed.

## Escalation

If you encounter:

- **Architecture decisions**: Consult project architecture docs if present, otherwise ask user
- **Unclear requirements**: Check product/requirements docs if present, otherwise ask user
- **Repeated test failures**: Update progress, flag for human review
- **Scope ambiguity**: Re-read `feature-list.json` for definition of done
