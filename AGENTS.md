# Awesome Harness Engineering

## Project Objectives
Automatically build harness by using the templates.
user will use codex to use this skill in codex's conversation(chat), not in terminal.
for local development after cloning the repo, install with `npx --yes --package=file:. ahe install`.
after deployment, the target user command is `npx ahe install`.
templates folder is for initilizing, and for agent, product, constraint, init.sh, feature-list.json, PROGRESS.md, SESSION-HANDOFF.md, schemas, examples
don't modify the template.

## Global Rules
- MUST NOT modify the AGENTS.md file except for PROJECT_PURPOSE.
- MUST NOT modify the headers in PROGRESS.md and SESSION-HANDOFF.md like deletion of headers.
- MUST FOLLOW THE FORMAT OF init.sh, feature-list.json, PROGRESS.md, SESSION-HANDOFF.md, AGENTS.md

## Reference ONLY(DONT MODIFY)
- learn-harness-engineering folder.
- templates folder.

## Startup Workflow
Before writing code:

1. **Confirm working directory** with `pwd`
2. **Read this file** completely
3. **Read project docs if present** (`docs/ARCHITECTURE.md`, `docs/PRODUCT.md`, `docs/CONSTRAINTS.md`, `docs/TODO.md`, README, or equivalent)
4. **Run `./init.sh`** to verify environment is healthy
5. **Read `feature_list.json`** to see current feature state
6. **Review recent commits** with `git log --oneline -5`

If baseline verification is failing, repair that first before adding new scope.

## Working Rules

- **One feature at a time**: Pick exactly one unfinished feature from `feature_list.json`
- **Verification required**: Don't claim done without running verification commands
- **Update artifacts**: Before ending session, update `progress.md` and `feature_list.json`
- **Stay in scope**: Don't modify files unrelated to the current feature
- **Leave clean state**: Next session must be able to run `./init.sh` immediately

## Required Artifacts

- `feature_list.json` — Feature state tracker (source of truth)
- `progress.md` — Session continuity log
- `init.sh` — Standard startup and verification path
- `session-handoff.md` — Optional, for larger sessions

## Definition of Done

A feature is done only when ALL of the following are true:

- [ ] Target behavior is implemented
- [ ] Required verification actually ran (tests / lint / type-check)
- [ ] Evidence recorded in `feature_list.json` or `progress.md`
- [ ] Repository remains restartable from standard startup path

## End of Session

Before ending a session:

1. Update `progress.md` with current state
2. Update `feature_list.json` with new feature status
3. Record any unresolved risks or blockers
4. Commit with descriptive message once work is in safe state
5. Leave repo clean enough for next session to run `./init.sh` immediately

## Verification Commands
- Tests: pytest tests/ -x
- Type check: mypy src/ --strict
- Lint: ruff check src/
- Full verification: make check (includes all above)

## Escalation

If you encounter:
- **Architecture decisions**: Consult project architecture docs if present, otherwise ask user
- **Unclear requirements**: Check product/requirements docs if present, otherwise ask user
- **Repeated test failures**: Update progress, flag for human review
- **Scope ambiguity**: Re-read `feature_list.json` for definition of done
