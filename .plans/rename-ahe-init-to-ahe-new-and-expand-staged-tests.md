# Rename `ahe-init` to `ahe-new` and expand staged tests

## Handoff Summary
Rename the existing new-start workflow from `ahe-init` to `ahe-new` as a full contract change, then reorganize and extend the automated tests around the `ahe new` flow. Treat the provided scenario list as the primary test matrix, while keeping the existing tracker contract as `feature-list.json`.

## Source Plan
### Summary
Rename `ahe-init` to `ahe-new` and expand staged tests.

### Public Contract Changes
- Replace these public entrypoints:
  - Remove `ahe init`, `ahe-init`, `$ahe-init`
  - Add `ahe new`, `ahe-new`, `$ahe-new`
- Replace the internal shipped skill identity:
  - `.codex/skills/ahe-init/` -> `.codex/skills/ahe-new/`
  - All references in hooks, docs, installer expectations, and tests must use `ahe-new`
- Keep tracker/artifact naming unchanged:
  - `feature-list.json` remains canonical
  - Existing template/artifact filenames stay `AGENTS.md`, `INSTRUCTIONS.md`, `progress.md`, `session-handoff.md`, `feature-list.json`, `init.sh`

### Implementation Changes
- Update command routing in `.codex/hooks/ahe-hook.js`:
  - Rename the exact-command detector and directive text to `ahe new`
  - Remove old `ahe init` aliases from the recognized public contract
  - Update directive language so restart/new-start flow points to `$ahe-new`
- Rename the skill package:
  - Move `.codex/skills/ahe-init/SKILL.md` to `.codex/skills/ahe-new/SKILL.md`
  - Update the skill body headings, workflow name, and any self-references from `ahe-init` to `ahe-new`
- Update install/help/docs surfaces:
  - `bin/ahe`
  - `README.md`
  - `docs/PRODUCT.md`
  - any setup/install tests that assert shipped skill names or public commands
- Keep behavior of the workflow itself unchanged unless required by the scenario list:
  - existing restart-scope logic
  - purpose/product clarification behavior
  - template-copy behavior
  - handoff to `ahe-harness`
- Rework the test suite into explicit stages, centered on `tests/test_ahe_new.py`:
  - Stage 1: template/install copy completeness
  - Stage 2: conversation trigger requirements
  - Stage 3: multiple product-file handling
  - Stage 4: actual harness-state handling
  - Stage 5: command-routing and compatibility regression for `ahe-new`
- Tighten the scenario assertions so they test the renamed command surface directly:
  - use `ahe new` / `ahe-new` prompts where the workflow is user-facing
  - remove assertions that depend on `ahe init` remaining valid
- Extend related regression files where needed:
  - command-set tests for shipped skill names
  - hook tests for exact prompt routing
  - project-setup/install tests for installed skill paths
  - chat-command routing tests for allowed user-facing commands

## Execution Context
- The repo already contains a scenario-oriented suite at `tests/test_ahe_new.py`; it currently passes and acts as the base for the staged test structure.
- Current public commands still reference `ahe init` / `ahe-init` broadly across `.codex/hooks/ahe-hook.js`, `.codex/skills/ahe-init/SKILL.md`, `README.md`, `docs/PRODUCT.md`, `bin/ahe`, and multiple tests.
- The user explicitly chose these product decisions during planning:
  - rename `ahe-init` to `ahe-new`
  - fully replace the old public contract instead of keeping compatibility aliases
  - fully rename the underlying skill/package identity, not just the command text
  - keep `feature-list.json` and treat `feature-list.md` as a typo
- Existing `tests/test_ahe_new.py` currently uses `ahe init` in some assertions and will need to be updated to the renamed command surface.

## Assumptions
- `feature-list.json` remains the canonical tracking artifact.
- This is a breaking rename with no compatibility path for old init command names.
- Workflow semantics remain unchanged unless renamed tests reveal a missing contract.
- The main behavioral work is contract renaming plus test restructuring, not redesigning the initialization flow.

## Constraints
- Do not route through `ahe-thinker`, `ahe-harness`, or other AHE internal agents for this export artifact.
- Keep the implementation aligned with existing template artifact names; do not rename tracker files to markdown.
- The repo’s AGENTS instructions forbid modifying template contents unless directly required; the current request is about command/skill naming and tests.
- The implementation phase must still respect the project startup/verification workflow and keep changes scoped to the active feature.

## Verification Plan
- Focused contract tests:
  - `pytest tests/test_ahe_new.py -x`
  - `pytest tests/test_ahe_hook.py -x`
  - `pytest tests/test_command_set.py -x`
  - `pytest tests/test_project_setup.py -x`
  - `pytest tests/test_chat_command_routing.py -x`
  - rename or replace `tests/test_init_workflow.py` to match `ahe-new`
- Full regression:
  - `pytest tests/ -x`
- Non-py verification:
  - `./init.sh`
  - `node --check .codex/hooks/ahe-hook.js`
  - `bash -n bin/ahe`
- Manual QA gate:
  - run the hook against exact prompts `ahe new`, `ahe-new`, `$ahe-new`
  - confirm old prompts `ahe init`, `ahe-init`, `$ahe-init` no longer activate the new-start workflow
  - perform an install smoke test and confirm the installed skill path is `skills/ahe-new/SKILL.md`

## Risks and Open Questions
- This is intentionally breaking: any undocumented downstream consumer of `ahe init` will stop working.
- Renaming the skill directory affects installer expectations and tests that assert the installed skill list; those must be updated consistently.
- Historical references in `feature-list.json`, `progress.md`, or `session-handoff.md` may still mention `ahe-init`; the implementation should decide whether those historical records are left as historical evidence or normalized when touched.
- `tests/test_ahe_new.py` already passes today, so the main risk is missing a secondary command-surface reference outside the obvious hook/docs/test files.

## Instructions for Next Agent
- Treat this as a contract rename first and a test-coverage refactor second.
- Update the command router and the skill identity together; do not leave mixed `ahe-init`/`ahe-new` references in shipped surfaces.
- Preserve the current new-start behavior unless a renamed test explicitly requires a behavior change.
- Prefer updating the existing scenario suite over creating a parallel test file unless a rename of `tests/test_init_workflow.py` makes the separation clearer.
- Before declaring completion, verify both the automated suite and the exact-prompt hook behavior for the new command surface.
