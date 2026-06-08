#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(CDPATH= cd -- "${SCRIPT_DIR}/.." && pwd)"
readonly CODEX_HOME="${HOME}/.codex"

echo "Installing AHE skill into ${CODEX_HOME}..."
(
  cd "${HOME}"
  npx --yes --package="${REPO_ROOT}" ahe install "$@"
)
