---
name: ahe
description: Continue existing harness work and route exact `ahe`, `ahe <query>`, and `<query> ahe` requests through the AHE agent network.
---

# AHE

`ahe` is the top-level user-facing Codex skill for continuing existing AHE
work in the current workspace.

## Command Contract

- Exact `ahe` means continue existing harness work.
- `ahe <query>` and `<query> ahe` mean continue AHE work with the user's
  explicit query.
- `ahe` must route through `ahe-think` as the central decision layer.
- `ahe` must not replace the dedicated `ahe-new`, `ahe-fix`, or `ahe-ship`
  workflows when the user's prompt matches those command contracts.

## Routing

- Call `ahe-think` first.
- Let `ahe-think` choose `ahe-review`, `ahe-converse`, `ahe-harness`, or
  `ahe-solve`.
- Keep `docs/product.md` as overview context and `feature-list.json` as the
  derived tracker.
- Actualize the final product through `docs/product{number}.md` stages in
  numeric order when staged product docs exist.

## Scope

- Use this skill for ongoing harness work, product updates, and explicit AHE
  requests such as `ahe compress`.
- Do not use this skill for standalone fix-plan export or ship-plan export.
