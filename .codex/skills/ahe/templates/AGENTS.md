# AGENTS.md

## Project Name
{{PROJECT_NAME}}

## Project Objectives
{{PROJECT_OBJECTIVES}}

## Product Specification
See `docs/PRODUCT.md` for current product requirements and tasks.

## Global Constraints
{{GLOBAL_CONSTRAINTS}}

## Working Rules
- **One feature at a time**: Pick exactly one unfinished feature from `feature-list.json`
- **Verification required**: Don't claim done without running verification commands
- **Update artifacts**: Before ending session, update `PROGRESS.md` and `feature-list.json`
- **Stay in scope**: Don't modify files unrelated to the current feature
- **Leave clean state**: Next session must be able to run `./init.sh` immediately

## Default Environment
{{DEFAULT_ENVIRONMENT}}

## Primary Verification Command
`{{PRIMARY_VERIFICATION_COMMAND}}`

## Verification Commands
{{VERIFICATION_COMMANDS}}

## File Ownership
{{FILE_OWNERSHIP}}

## Handoff Rules
- Update `PROGRESS.md`
- Update `SESSION-HANDOFF.md`
- Leave repo clean enough for next session to run `./init.sh` immediately

## Do Not Do
{{DO_NOT_DO}}
