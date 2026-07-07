# progress.md

## Current Status

**Last Updated:** 2026-07-07 10:10 +0900
**Session ID:** feat-077-verify-package-version-alignment
**Active Feature:** None

## Completed

- [x] Implemented `feat-077 Verify package version alignment in test script` by checking package.json versions in `scripts/test.sh` and adding a python unit test to ensure all workspace manifests match the root. Bumped root `package.json` and `packages/ahe-antigravity/package.json` to version `0.1.12`.
- [x] Implemented `feat-076 Delete shipped ahe-fix files` by deleting the remaining `packages/ahe-codex/.codex/skills/ahe-fix/` files and `tests/test_ahe_fix_writer.py`, replacing active `ahe fix` examples with ordinary `ahe` query wording, and updating the install/contract tests plus live tracker guidance so the repository no longer ships `ahe-fix` at all.
- [x] Implemented `feat-075 Retire standalone ahe-new and ahe-fix entrypoints` by routing `ahe new`, `ahe fix`, and other explicit follow-up prompts through the normal `ahe` hook path, keeping `ahe-new` internal under `ahe-think`, retiring `ahe-fix` from the managed install surface, and updating the README, product spec, skills, installer text, and contract tests to reflect that `ahe`, `ahe-ship`, and `ahe-git` are the only operational public entrypoints.
- [x] Implemented `feat-074 Prepare v0.1.11 package metadata` by bumping the root and workspace package manifests to `0.1.11` so local release validation clears the npm published-version check while keeping package metadata aligned.
- [x] Implemented `feat-073 Add Internal AHE Clean Tracker Compaction Worker` by adding internal `ahe-clean`, making `ahe-think` route cleanup for noisy-but-valid tracker state, and making `ahe-harness` explicitly own the policy that tracking artifacts stay current-work-focused instead of acting as long-form archives.
- [x] Implemented `feat-072 Route Harness Manager Through AHE Think` by moving harness-manager invocation authority into `ahe-think`, making the manager advisory-only, tightening Codex config ownership to the explicit AHE-managed block, and preserving unrelated user-owned `[agents.ahe-*]` config during install and uninstall.
- [x] Implemented `feat-071 Retire AHE Compression Workflow` by deleting the internal `ahe-compress` skill and detector assets, removing compression references from the installer, hook, thinker, harness contract, README, product spec, and deleting compression-only tests.
- [x] Implemented `feat-070 Allow AHE Git Local-Ahead Dirty Commits` by clarifying that dirty repos which are only locally ahead of upstream continue to commit-message review, while dirty repos that need upstream commits still block.
- [x] Implemented `feat-069 Remove completed Antigravity ship plans` by deleting saved Antigravity ship plans only after `AHE_PLAN_COMPLETE`, then applying the pending work as separated commits through the `ahe-git` workflow.
- [x] Implemented `feat-068 Move install script into scripts directory` by moving the real installer to `scripts/install.sh` and leaving a root `install.sh` wrapper that forwards to the new path so the existing repo workflow still works.
- [x] Implemented `feat-067 Split deploy and local validation scripts` by moving the real npm publish flow into `scripts/deploy.sh`, adding `scripts/test.sh` for branch-local validation, and removing the root `deploy.sh`.
- [x] Implemented `feat-066 Use bare semver release tags for npm publish` by changing the GitHub Actions release trigger from `v*.*.*` tags to bare semver tags like `0.1.8`, and by requiring the pushed tag to exactly match `package.json` without a `v` prefix.
- [x] Implemented `feat-065 Prepare v0.1.8 package metadata` by bumping the root and workspace package manifest versions from `0.1.7` to `0.1.8` so the next GitFlow release tag can match the publish workflow expectation.
- [x] Implemented `feat-064 Publish npm package from release tags` by adding `.github/workflows/publish.yml` to trigger on `v*.*.*` tags, verify the tag commit is reachable from `master`, require the tag name to match the root `package.json` version, install `pytest`, and publish with `NPM_TOKEN`.
- [x] Replaced the obsolete remote release tag `v0.1.1` with `v0.1.7` so the current GitHub release tag matches the root and workspace package versions (`0.1.7`).
- [x] Implemented `feat-063 Add ahe-git command` by adding `ahe-git` as an independent git orchestration skill, wiring it to Codex hooks, updating the Codex installer and Antigravity wrapper, and expanding test suites.
- [x] Implemented `feat-062 Post-Generation Harness Checker` by adding the `ahe-harness-checker` internal skill, updating the `ahe-new` setup to sequentially execute the three-step sequence (`new -> ahe-harness -> ahe-harness-checker`), requiring `ahe-harness` completion to hand off to the checker, adding the checker to the allowed network in `ahe-think`, updating hook directives and spec docs, and expanding test suites.
- [x] Compressed the historical tracker surface into one summary feature covering `feat-001` through `feat-042` so `feature-list.json` stops carrying stale per-feature history after the AHE routing and compression work stabilized.
- [x] Implemented `feat-043 No-Backup Feature History Compression` by removing AHE workflow backup-copy guidance from the init and compression contracts, updating the exact `ahe init` and `ahe compress feature-list` hook text, and documenting that replaced harness history should be summarized in the refreshed tracking artifacts instead of copied aside.
- [x] Updated the contract tests in `tests/test_init_workflow.py`, `tests/test_ahe_hook.py`, and `tests/test_compression_workflow.py` to enforce the new no-backup and summarized-history behavior.
- [x] Refreshed `progress.md` and `session-handoff.md` to keep only current state, durable decisions, and recent verification evidence.
- [x] Implemented `feat-044 Global AHE Skill Installation and Docs Read Contract` by changing `ahe install` to target `$CODEX_HOME` or `~/.codex`, documenting global operation, and requiring AHE workflows to read all existing `docs/*.md` files as supporting project context.
- [x] Implemented `feat-045 Lowercase Harness Artifact Filenames` by renaming product/progress/session artifacts to lowercase filenames while keeping `AGENTS.md` uppercase, and updating all AHE contracts, templates, tests, and compression detection.
- [x] Implemented `feat-046 Independent AHE Skill Plan Export` by adding the standalone `ahe-ship` skill, direct `ahe ship` hook route, deterministic `.plans/{plan_name}.md` writer, installer allowlist entry, docs, and focused tests.
- [x] Implemented `feat-047 Staged Product Docs` by treating `docs/product.md` as overview context and optional numbered docs like `docs/product1.md` and `docs/product2.md` as ordered product stages.
- [x] Implemented `feat-048 Independent AHE Fix Plan Export` by adding the standalone `ahe-fix` skill, direct `ahe fix` hook route, deterministic `.plans/{plan_name}.md` fix-plan writer, installer allowlist entry, docs, and focused tests.
- [x] Implemented `feat-050 AHE Ship Executes Saved Plans Through Antigravity` by updating `ahe ship` to write `.plans/{plan_name}.md`, run `ahe-antigravity execute` through `agy`, and delete the plan only after `AHE_PLAN_COMPLETE` verifies full completion.
- [x] Implemented `feat-051 Remove .ahe Directory From AHE Contract` by removing `.ahe` as an AHE-managed workspace concept and transitioning the workflow-state artifact to root `status.json`.
- [x] Implemented `feat-052 AHE Ship Writer Uses Active Python Environment` by removing the writer's Python 3.11-only parsing syntax, changing the ship skill example to `python`, and making the writer test use `sys.executable` instead of hardcoded `python3`.
- [x] Implemented `feat-053 AHE Ship Uses Gemini 3.1 Pro High In Antigravity` by making the Antigravity wrapper call `agy --model "Gemini 3.1 Pro (High)"` for saved ship plans and updating the ship-facing docs to match that execution contract.
- [x] Implemented `feat-055 Simplify AHE Compress To One User Command` by replacing `ahe compress feature-list` and `ahe compress tests` wording with one `ahe compress` contract that checks both detectors before choosing harness or test cleanup follow-up.
- [x] Implemented `feat-056 Revert AHE Ship To Save-Only` by removing automatic Antigravity execution and cleanup from the ship workflow, updating the hook, docs, tests, and doctor checks accordingly.
- [x] Implemented `feat-057 Bidirectional AHE Query Command Matching` by letting the hook accept `ahe <query>` and `<query> ahe` for thinker-routed continuation, while keeping `ahe fix <query>` and `<query> ahe fix` on the independent fix-plan path.
- [x] Implemented `feat-058 Align AHE Startup Contract With Think-Led Read Order` by canonicalizing artifact names (`docs/product.md`, `progress.md`, `session-handoff.md`, `status.json`), setting explicit `think` routing in Codex, and aligning `AGENTS.md` and test fixtures.
- [x] Implemented `feat-059 Global-Only AHE Skill Display Cleanup` by making the Codex installer and uninstaller remove stale AHE-owned legacy skill directories such as `new`, `fix`, `ship`, `ahe-init`, and older aliases so only current global `ahe-*` skills remain visible.
- [x] Implemented `feat-060 Install AHE As A Global Codex Skill` by packaging a real `ahe` skill under `packages/ahe-codex/.codex/skills/ahe`, adding it to the managed global install set, and installing it into `/Users/KC/.codex/skills/ahe`.
- [x] Implemented `feat-061 Add CodeGraph Preflight To All AHE Entrypoints` by extracting CodeGraph preflight instructions and prepending them to all AHE hook directives (`ahe`, `ahe new`, `ahe ship`, `ahe fix`, `ahe-overview`), along with accompanying test assertions.

## In Progress

- [ ] No active implementation in progress.
Details: `feat-077 Verify package version alignment in test script` is complete.
Latest: package versions in all package.json files are aligned to 0.1.12, checked in `scripts/test.sh` and python unit tests.
Blockers: None.

## Blocked

- [ ] No current blocker.

## Decisions

- **AHE workflow restarts no longer create backup copies**: `ahe-init` now asks for restart scope, replaces only the chosen harness files, and records the replaced state through concise tracker summaries instead of `.ahe/backups/`.
- **Completed feature history compresses into one summary feature**: `ahe compress feature-list` now replaces stale done entries with one summarized done feature while preserving unfinished, blocked, or active items in full detail.
- **Tracking artifacts should stay token-aware after compression**: `feature-list.json`, `progress.md`, and `session-handoff.md` now prefer concise historical summaries over long completed-history lists once work is stable.
- **AHE installs globally**: `ahe install`, `ahe doctor`, and `ahe uninstall` now use `$CODEX_HOME` when set and `~/.codex` otherwise; installed skills, shared files, and hooks should not be copied into each target workspace.
- **AHE reads all docs context**: Startup and internal AHE workflows must read every existing `docs/*.md` file as supporting project context, with product-style docs called out as especially important.
- **Only AGENTS stays uppercase**: AHE harness artifacts now use `docs/product.md`, `progress.md`, and `session-handoff.md`; template copies follow the same lowercase filenames except `AGENTS.md`.
- **AHE ship stays independent**: `ahe ship`, `ahe-ship`, and `$ahe-ship` export the latest Codex Plan Mode `<proposed_plan>` to `.plans/{plan_name}.md` without entering the `ahe-think` routed AHE agent network.
- **Product docs can be staged**: `docs/product.md` is overview context; `docs/product1.md`, `docs/product2.md`, and later numeric docs run in order; non-numeric product docs do not affect stage order.
- **AHE no longer ships a dedicated fix workflow**: `ahe-fix` is deleted from the repository, and fix-oriented follow-up should be phrased as ordinary `ahe` queries rather than as a separate exported plan writer.
- **AHE ship is save-only**: `ahe ship` writes `.plans/{plan_name}.md` and stops. It no longer automatically executes the plan through Antigravity.
- **AHE state tracking uses root status.json**: The workflow state tracking now uses `status.json` instead of `.ahe/process_status.json`, removing `.ahe` as a workspace concept.
- **AHE ship must follow the active Python environment**: The ship writer path should not depend on a hardcoded `python3` binary because the active Conda environment may expose `python` while `python3` still resolves to the system interpreter.
- **AHE ship must use the high Gemini model in Antigravity**: The Antigravity wrapper now runs saved ship plans with `agy --model "Gemini 3.1 Pro (High)"` so ship execution does not drift with the CLI default model.
- **AHE compress should stay as one user command**: `ahe compress` is now the only documented compression entrypoint, and it always checks both harness-file pressure and stale overlapping tests before routing follow-up work.
- **AHE query matching is bidirectional**: thinker-routed continuation accepts both `ahe <query>` and `<query> ahe`, including follow-up requests such as stale-test cleanup phrased as normal `ahe` queries.
- **AHE installer cleans old skill aliases**: `ahe install` and `ahe uninstall` remove AHE-owned legacy skill directories (`new`, `fix`, `ship`, old `ahe-*` aliases) from the global Codex home so the skills picker shows only the current global `ahe-*` set.
- **AHE is now a real global skill entry**: the Codex installer manages `/Users/KC/.codex/skills/ahe` as a first-class user-facing continuation skill instead of relying on the repo's `bin/ahe` path to appear in search results.
- **AHE git orchestrates git safely**: `ahe git`, `ahe-git`, and `$ahe-git` provide safe git orchestration across a repository and its submodules without routing through `ahe-think`. It enforces fast-forward pulls, halts on conflicts, and allows commit review when a dirty repo is only locally ahead of upstream.
- **AHE compression is retired**: `ahe-compress` and the documented `ahe compress` workflow are removed from the active product surface, installer allowlist, hook guidance, and contract tests.
- **Harness-manager routing belongs to `ahe-think`**: `@ahe-harness-manager` stays installed as an advisory Codex agent, but hook prompts must defer the decision to `ahe-think`, which invokes it only when harness state is missing, invalid, mismatched, or otherwise ambiguous.
- **AHE uninstall owns only the managed config block**: installer cleanup and uninstall may remove the explicit `# BEGIN AHE MANAGED CONFIG` block and AHE-owned plugin/hook sections, but must leave unrelated user-managed `[agents.ahe-*]` entries outside that block untouched.
- **Tracker cleanup is internal and policy-driven**: `ahe-clean` is an internal worker only; `ahe-think` decides when stale completed history is hurting clarity, and `ahe-harness` owns the rule that `feature-list.json` and `session-handoff.md` should stay current-work-focused rather than serve as long-form archives.
- **npm releases are tag-driven**: GitHub Actions should publish only on bare semver tag pushes like `0.1.12`, only when the tagged commit is on `master`, and only when the pushed tag exactly matches the root `package.json` version.
- **Release tags must match package manifests**: The next GitFlow release should use `0.1.12` because the root and workspace `package.json` files now declare `0.1.12`.
- **Workspace package versions must align**: `scripts/test.sh` and Python unit tests now enforce that all package versions match the root `package.json` to prevent mismatched tags from failing at release time.
- **Local release validation should never publish**: `scripts/test.sh` is now the local verification entrypoint, while `scripts/deploy.sh` remains the explicit real publish path.
- **Installer implementation lives under `scripts/`**: `scripts/install.sh` is the real reinstall script; the root `install.sh` only forwards there to preserve the existing documented workflow.
- **Antigravity plan cleanup is marker-gated**: `packages/ahe-antigravity/bin/ahe-antigravity` removes a saved ship plan only after the exact `AHE_PLAN_COMPLETE` marker appears.
- **AHE public routing is reduced to three operational entrypoints**: normal work, bootstrap intent, and follow-up intent all enter through `ahe`; only `ahe-ship` and `ahe-git` remain separate operational public commands, while `ahe-new` stays internal and `ahe-fix` is retired from the managed install surface.
- **AHE fix files are deleted, not dormant**: there is no shipped `ahe-fix` skill or writer script left in the repo, so future work should not treat fix-plan export as latent functionality.

## Verification

- [x] `sh scripts/test.sh`
- [x] `pytest tests/test_project_setup.py -k test_all_package_versions_are_aligned`
- [x] `pytest tests/ -x`
- [x] `ruff check tests/`
- [x] `bash -n install.sh scripts/install.sh packages/ahe-codex/bin/ahe-codex packages/ahe-antigravity/bin/ahe-antigravity bin/ahe`
- [x] `packages/ahe-codex/bin/ahe-codex install --force`
- [x] `packages/ahe-antigravity/bin/ahe-antigravity install --force`
- [x] `rg -n "locally ahead of upstream|upstream has commits not present locally" /Users/KC/.codex/skills/ahe-git/SKILL.md /Users/KC/.gemini/config/skills/ahe-git/SKILL.md`
- [x] `packages/ahe-codex/bin/ahe-codex doctor`
- [x] `packages/ahe-antigravity/bin/ahe-antigravity doctor`
- [x] `./init.sh`
- [x] `pytest tests/ -x`
- [x] `ruff check tests/`
- [x] `bash -n packages/ahe-codex/bin/ahe-codex`
- [x] `node --check packages/ahe-codex/.codex/hooks/ahe-hook.js`
- [x] `pytest tests/test_command_set.py tests/test_project_setup.py tests/test_ahe_hook.py tests/test_ahe_exact.py tests/test_ahe_clean_contract.py -x`
- [x] `git diff --check`
- [x] `./bin/ahe install --force`
- [x] `./bin/ahe doctor`
- [ ] `bash scripts/install.sh`
Details: Reached the documented reinstall flow, but `sudo npm install -g .` stopped on the host password prompt. Restored the global Codex and Antigravity skill installs with `./bin/ahe install --force`.
- [x] `ruff check tests/`
- [x] `python3 -m json.tool feature-list.json`
- [x] `git diff --check`
- [x] `python3 -m json.tool package.json`
- [x] `python3 -m json.tool packages/ahe-codex/package.json`
- [x] `python3 -m json.tool packages/ahe-antigravity/package.json`
- [x] `sh scripts/test.sh`
- [x] `rg -n '"version"\s*:\s*"0\.1\.8"' package.json packages -g 'package.json'`
- [x] `python3 -m json.tool feature-list.json`
- [x] `git diff --check`
- [x] `bash -n install.sh scripts/install.sh scripts/deploy.sh scripts/test.sh`
- [x] `pytest tests/test_ahe_hook.py tests/test_command_set.py tests/test_chat_command_routing.py tests/test_project_setup.py -x`
- [x] `pytest tests/ -x`
- [x] `ruff check tests/`
- [x] `node --check packages/ahe-codex/.codex/hooks/ahe-hook.js`
- [x] `bash -n packages/ahe-codex/bin/ahe-codex`
- [x] `./init.sh`
- [x] `date '+%Y-%m-%d %H:%M %z'`
- [x] `pytest tests/test_command_set.py tests/test_project_setup.py tests/test_ahe_hook.py -x`
- [x] `pytest tests/ -x`
- [x] `ruff check tests/`
- [x] `python3 -m json.tool feature-list.json`
- [x] `git diff --check`
- [x] `bash -n scripts/deploy.sh scripts/test.sh`
- [ ] `bash scripts/test.sh`
Details: Not rerun in this session because `pytest tests/ -x` now covers the test suite directly and `scripts/test.sh` also performs npm packaging work.
- [x] `pytest tests/test_ahe_antigravity_ship.py::test_ahe_ship_sends_plan_contents_to_agy -x`
- [x] `pytest tests/ -x`
- [ ] `ruff check src/`
Details: Not runnable because this repository currently has no `src/` directory.
- [ ] `mypy src/ --strict`
Details: Not runnable because `mypy` is not installed in this environment.

## Change Log

- `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-harness/SKILL.md`, `.codex/skills/ahe-compress/SKILL.md`, `.codex/hooks/ahe-hook.js`, `docs/product.md` - Removed workflow backup-copy guidance and documented summarized-history replacement behavior.
- `tests/test_init_workflow.py`, `tests/test_ahe_hook.py`, `tests/test_compression_workflow.py` - Added contract coverage for no-backup restart behavior and summarized completed-feature compression.
- `feature-list.json`, `progress.md`, `session-handoff.md` - Compressed stale completed history and recorded `feat-043`.
- `bin/ahe`, `README.md`, `docs/product.md`, `package.json`, `tests/test_project_setup.py` - Moved installer behavior and product contract to global Codex home installation.
- `AGENTS.md`, `.codex/skills/ahe-init/SKILL.md`, `.codex/skills/ahe-harness/SKILL.md`, `.codex/skills/ahe-review/SKILL.md`, `.codex/hooks/ahe-hook.js`, `tests/test_init_workflow.py` - Updated startup and internal workflow guidance to read all existing `docs/*.md` files.
- `docs/product.md`, `progress.md`, `session-handoff.md`, `.codex/ahe-shared/templates/*`, `.codex/skills/*`, `.codex/hooks/ahe-hook.js`, `tests/*` - Updated lowercase filename contract for product, progress, and session handoff artifacts.
- `.codex/skills/ahe-ship/*`, `.codex/hooks/ahe-hook.js`, `bin/ahe`, `README.md`, `docs/PRODUCT.md`, `tests/test_ahe_ship_writer.py`, `tests/test_ahe_hook.py`, `tests/test_command_set.py`, `tests/test_project_setup.py` - Added independent Plan Mode export workflow for `.plans/{plan_name}.md`.
- `.codex/hooks/ahe-hook.js`, `.codex/skills/ahe-*`, `.codex/skills/ahe-compress/scripts/check-harness-size.sh`, `docs/product.md`, `feature-list.json`, `tests/test_ahe_hook.py`, `tests/test_spec_workflow.py`, `tests/test_specialized_workflows.py`, `tests/test_compression_workflow.py` - Added staged product-doc routing, active-stage feature derivation, and numeric product-stage compression detection.
- `.codex/skills/ahe-fix/*`, `.codex/hooks/ahe-hook.js`, `bin/ahe`, `README.md`, `docs/PRODUCT.md`, `feature-list.json`, `tests/test_ahe_fix_writer.py`, `tests/test_ahe_hook.py`, `tests/test_command_set.py`, `tests/test_project_setup.py`, `tests/test_chat_command_routing.py` - Added independent fix-plan export workflow for `.plans/{plan_name}.md`.
- `.codex/skills/ahe-new/*`, `.codex/hooks/ahe-hook.js`, `bin/ahe`, `README.md`, `docs/PRODUCT.md`, `tests/*` - Renamed `ahe-init` to `ahe-new` and restructured tests around `tests/test_ahe_new.py`.
- `packages/ahe-antigravity/bin/ahe-antigravity`, `packages/ahe-antigravity/skills/execute/SKILL.md`, `packages/ahe-codex/.codex/skills/ship/SKILL.md`, `packages/ahe-codex/.codex/hooks/ahe-hook.js`, `packages/ahe-codex/bin/ahe-codex`, `packages/ahe-codex/.codex/skills/harness/SKILL.md`, `README.md`, `docs/PRODUCT.md`, `tests/test_ahe_antigravity_execute.py`, and packaged-path test updates - Added the ship-and-execute workflow with verified completion cleanup.
- `packages/ahe-codex/.codex/skills/new/SKILL.md`, `packages/ahe-codex/.codex/skills/harness/SKILL.md`, `packages/ahe-codex/.codex/skills/converse/SKILL.md`, `docs/PRODUCT.md`, `src/templates/agents.md`, `tests/*` - Replaced `.ahe/process_status.json` references with root `status.json` and removed `.ahe` directory references.
- `packages/ahe-codex/.codex/skills/ship/scripts/write_plan.py`, `packages/ahe-codex/.codex/skills/ship/SKILL.md`, and `tests/test_ahe_ship_writer.py` - Removed the Python 3.11-only parser syntax from the writer, aligned the ship skill example with the active environment's `python`, and made the writer test invoke the current interpreter.
- `packages/ahe-antigravity/bin/ahe-antigravity`, `packages/ahe-antigravity/skills/ahe-ship/SKILL.md`, `packages/ahe-codex/.codex/skills/ship/SKILL.md`, `README.md`, `docs/PRODUCT.md`, and `tests/test_ahe_antigravity_ship.py` - Locked `ahe ship` execution to `Gemini 3.1 Pro (High)` in Antigravity and added contract coverage for the `agy --model` call.
- `packages/ahe-codex/.codex/hooks/ahe-hook.js`, `packages/ahe-codex/.codex/skills/compress/SKILL.md`, `packages/ahe-codex/.codex/skills/think/SKILL.md`, `packages/ahe-codex/.codex/skills/harness/SKILL.md`, `packages/ahe-codex/bin/ahe-codex`, `README.md`, `docs/PRODUCT.md`, `tests/test_ahe_hook.py`, `tests/test_compression_workflow.py` - Unified compression wording under `ahe compress` and documented that it checks both harness-size and stale-test detectors.
- `packages/ahe-codex/.codex/hooks/ahe-hook.js`, `packages/ahe-codex/.codex/skills/think/SKILL.md`, `packages/ahe-codex/.codex/skills/fix/SKILL.md`, `README.md`, `docs/PRODUCT.md`, and `tests/test_ahe_hook.py` - Added bidirectional query matching for `ahe` and `ahe fix`, kept fix queries off the thinker route, and documented the updated Codex-side architecture.
- `packages/ahe-codex/bin/ahe-codex`, `tests/test_project_setup.py`, `feature-list.json`, and `progress.md` - Added legacy AHE skill cleanup during install/uninstall and focused regression coverage for global-only skill display.
- `packages/ahe-codex/.codex/skills/ahe/SKILL.md`, `packages/ahe-codex/bin/ahe-codex`, `README.md`, `docs/product.md`, `tests/test_project_setup.py`, and `tests/test_command_set.py` - Added a real top-level global `ahe` skill entry and verified that it installs into `/Users/KC/.codex/skills/ahe`.
- `packages/ahe-codex/.codex/hooks/ahe-hook.js`, `tests/test_ahe_hook.py`, `feature-list.json`, and `progress.md` - Extracted CodeGraph preflight instructions and prepended them to all hook directives (`ahe`, `ahe new`, `ahe ship`, `ahe fix`, `ahe-overview`).
- `packages/ahe-codex/.codex/skills/ahe-harness-checker/SKILL.md` [NEW], `packages/ahe-codex/bin/ahe-codex`, `packages/ahe-codex/.codex/skills/ahe-new/SKILL.md`, `packages/ahe-codex/.codex/skills/ahe-harness/SKILL.md`, `packages/ahe-codex/.codex/skills/ahe-think/SKILL.md`, `packages/ahe-codex/.codex/hooks/ahe-hook.js`, `docs/product.md`, `tests/test_project_setup.py`, `tests/test_command_set.py`, `tests/test_ahe_new.py` - Implemented post-generation harness checker flow and updated setup orchestration sequence and testing.
- `packages/ahe-codex/.codex/skills/ahe-git/SKILL.md` [NEW], `packages/ahe-antigravity/skills/ahe-git/SKILL.md` [NEW], `packages/ahe-codex/bin/ahe-codex`, `packages/ahe-antigravity/bin/ahe-antigravity`, `packages/ahe-codex/.codex/hooks/ahe-hook.js`, `README.md`, `docs/product.md`, `feature-list.json`, `tests/test_ahe_git_skill_contract.py`, `tests/test_ahe_antigravity_git.py`, `tests/test_command_set.py`, `tests/test_project_setup.py`, `tests/test_ahe_hook.py` - Added independent git orchestration workflow and corresponding tests.
- `packages/ahe-codex/.codex/skills/ahe-git/SKILL.md`, `packages/ahe-antigravity/skills/ahe-git/SKILL.md`, `docs/product.md`, `tests/test_ahe_git_skill_contract.py`, `feature-list.json`, `progress.md` - Clarified that dirty repos which are only locally ahead of upstream continue to commit review, while dirty repos that need upstream commits still block.
- `packages/ahe-codex/.codex/skills/ahe-compress/` [DELETED], `packages/ahe-codex/.codex/ahe-shared/config.yaml` [DELETED], `packages/ahe-codex/bin/ahe-codex`, `packages/ahe-codex/.codex/hooks/ahe-hook.js`, `packages/ahe-codex/.codex/skills/ahe-think/SKILL.md`, `packages/ahe-codex/.codex/skills/ahe-harness/SKILL.md`, `README.md`, `docs/product.md`, `tests/test_command_set.py`, `tests/test_project_setup.py`, `tests/test_chat_command_routing.py`, `tests/test_clarification_prompt.py`, `tests/test_ahe_new.py`, `tests/test_ahe_exact.py`, `tests/test_compression_workflow.py` [DELETED], `tests/test_compress_detector.py` [DELETED] - Removed the active AHE compression workflow and its contract/test surface.
- `packages/ahe-codex/bin/ahe-codex`, `packages/ahe-codex/.codex/hooks/ahe-hook.js`, `packages/ahe-codex/.codex/skills/ahe-think/SKILL.md`, `docs/product.md`, `tests/test_project_setup.py`, `tests/test_ahe_hook.py`, `tests/test_ahe_exact.py`, `feature-list.json`, `progress.md`, `session-handoff.md` - Moved harness-manager routing ownership into `ahe-think`, restricted uninstall cleanup to the explicit AHE-managed Codex config block, and added regression coverage for preserving user-owned `ahe-*` agents outside that block.
- `packages/ahe-codex/.codex/skills/ahe-clean/SKILL.md` [NEW], `packages/ahe-codex/bin/ahe-codex`, `packages/ahe-codex/.codex/skills/ahe-harness/SKILL.md`, `packages/ahe-codex/.codex/skills/ahe-think/SKILL.md`, `packages/ahe-codex/.codex/hooks/ahe-hook.js`, `docs/product.md`, `tests/test_command_set.py`, `tests/test_project_setup.py`, `tests/test_ahe_hook.py`, `tests/test_ahe_exact.py`, `tests/test_ahe_clean_contract.py`, `feature-list.json`, `progress.md`, `session-handoff.md` - Added internal `ahe-clean`, made `ahe-think` route tracker compaction for noisy-but-valid harness state, and made `ahe-harness` explicitly own the policy that current-work tracking artifacts may compact unrelated completed history.
- `.github/workflows/publish.yml`, `feature-list.json`, `progress.md`, `session-handoff.md` - Added the npm publish workflow for `v*.*.*` tags, enforced tag/package version parity plus `master` containment, and recorded the corrected remote tag move from `v0.1.1` to `v0.1.7`.
- `package.json`, `packages/ahe-codex/package.json`, `packages/ahe-antigravity/package.json`, `feature-list.json`, `progress.md`, `session-handoff.md` - Bumped the release metadata to `0.1.11`, aligned the internal workspace manifests with the published package version, and recorded the passing local release validation evidence.
- `packages/ahe-codex/.codex/hooks/ahe-hook.js`, `packages/ahe-codex/bin/ahe-codex`, `packages/ahe-codex/.codex/skills/ahe/SKILL.md`, `packages/ahe-codex/.codex/skills/ahe-think/SKILL.md`, `packages/ahe-codex/.codex/skills/ahe-new/SKILL.md`, `packages/ahe-codex/.codex/skills/ahe-overview/SKILL.md`, `README.md`, `docs/product.md`, `tests/test_ahe_hook.py`, `tests/test_ahe_new.py`, `tests/test_command_set.py`, `tests/test_chat_command_routing.py`, `tests/test_project_setup.py`, `feature-list.json`, `progress.md` - Retired standalone `ahe-new` and `ahe-fix` public entrypoints, routed `ahe new` and `ahe fix` through the normal `ahe` continuation surface, kept `ahe-new` internal, and removed `ahe-fix` from the managed install set.
- `packages/ahe-codex/.codex/skills/ahe-fix/SKILL.md` [DELETED], `packages/ahe-codex/.codex/skills/ahe-fix/scripts/write_fix_plan.py` [DELETED], `tests/test_ahe_fix_writer.py` [DELETED], `README.md`, `docs/product.md`, `tests/test_ahe_hook.py`, `tests/test_command_set.py`, `tests/test_project_setup.py`, `feature-list.json`, `progress.md`, `session-handoff.md` - Deleted the remaining shipped `ahe-fix` implementation files and replaced active `ahe fix` mode wording with ordinary `ahe` query wording.
