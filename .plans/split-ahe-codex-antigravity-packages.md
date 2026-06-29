# Split AHE Code into `packages/ahe-codex` and `packages/ahe-antigravity`

## Handoff Summary
Restructure AHE to mirror the `oh-my-openagent` package layout pattern at the code level while keeping a single published npm package. Move Codex-specific code and assets into `packages/ahe-codex`, add Antigravity-specific code and assets in `packages/ahe-antigravity`, and keep the root package as the umbrella CLI and publish surface.

## Source Plan
### Summary
Split AHE code into `packages/ahe-codex` and `packages/ahe-antigravity`.

### Public Interface
- Keep one published npm package: `@ksuchoi216/ahe`
- Introduce internal package folders:
  - `packages/ahe-codex`
  - `packages/ahe-antigravity`
- Keep the root CLI as the public entrypoint.
- Preserve Codex global install behavior.
- Add Antigravity install behavior targeting the documented Antigravity skill locations.

### Implementation Changes
- Convert the repo to a workspace-style layout with `packages/*`.
- Move current Codex assets and install logic into `packages/ahe-codex`.
- Add Antigravity skill source and install logic into `packages/ahe-antigravity`.
- Refactor `bin/ahe` into a dispatcher that delegates to package-owned install logic.
- Keep root packaging metadata responsible for shipping both internal package assets in one npm artifact.
- Avoid speculative shared abstractions; extract only clearly duplicated helpers after the split is in place.

## Execution Context
- The current repo is still a single-package layout with one root [package.json](/Users/KC/Codes/awesome_harness_engineering/package.json) and a monolithic shell installer in [bin/ahe](/Users/KC/Codes/awesome_harness_engineering/bin/ahe).
- Current Codex assets live at the repo root under `.codex/skills`, `.codex/hooks`, and `.codex/ahe-shared`.
- The repo already contains a local `oh-my-openagent` checkout with separate `packages/omo-codex` and `packages/omo-opencode`, which is the structural reference for this split.
- The user explicitly does **not** want two published npm packages; the split is for folder/code separation only.
- Antigravity skill install targets were confirmed from the referenced docs:
  - workspace-local: `<workspace-root>/.agents/skills/<skill-folder>/`
  - global: `~/.gemini/config/skills/<skill-folder>/`
- The intended Antigravity-side workflow is that Codex writes plans into `.plans/`, and Antigravity executes those plans.

## Assumptions
- Root package name remains `@ksuchoi216/ahe`.
- `packages/ahe-codex` and `packages/ahe-antigravity` are internal workspace packages, not separately published npm packages.
- Existing user-facing Codex commands should remain stable unless a new install target selector is needed.
- The Antigravity execution skill remains a downstream consumer of Codex-authored `.plans/*.md` files.

## Constraints
- Do not redesign AHE into a multi-publish-package repo.
- Keep changes scoped to package layout, installer routing, and platform-specific asset ownership.
- Preserve current Codex behavior while introducing the Antigravity package path.
- Follow the repo’s existing harness conventions and leave template contents unchanged unless the split directly requires it.

## Verification Plan
- Confirm workspace/package wiring from the root package metadata.
- Verify root packaging still includes both Codex and Antigravity assets in the published artifact.
- Re-run Codex install/uninstall/doctor regression checks after the refactor.
- Validate Antigravity install output targets the documented skill locations.
- Confirm the root CLI can dispatch correctly to Codex and Antigravity install flows.
- Update README and product docs to describe the one-package, two-internal-packages structure.

## Risks and Open Questions
- Moving root-owned `.codex` assets into `packages/ahe-codex` may require careful updates to publish metadata and path assumptions in installer scripts and tests.
- The current installer is shell-based and path-coupled to the root layout, so the split may reveal hidden assumptions in `bin/ahe`.
- Antigravity-side behavior is newer and less integrated than Codex-side behavior, so install-path and packaging regressions are more likely there.
- If shared logic emerges between Codex and Antigravity installers, extract it only after duplication becomes concrete.

## Instructions for Next Agent
- Treat this as a structural refactor with contract preservation for the root npm package.
- Start by establishing the new package folders and moving Codex-owned assets behind a stable internal boundary.
- Keep the root CLI thin and delegate platform-specific work to package-local code.
- Use `oh-my-openagent` as the packaging/layout reference, not as a requirement to copy its full toolchain.
- Preserve the Codex plan-export flow and prepare the Antigravity side to consume `.plans/*.md` as execution artifacts.
