#!/usr/bin/env bash
set -euo pipefail

readonly CODEX_HOME="${HOME}/.codex"
readonly SHARED_DIR="${CODEX_HOME}/ahe-shared"
readonly MANAGED_SKILLS=(
  "ahe-init"
  "ahe-agent"
  "ahe-product"
  "ahe-todo"
  "ahe-constraints"
  "ahe-architecture"
  "ahe-update"
  "ahe-clear"
  "ahe-help"
  "ahe-copy"
)

echo "Uninstalling AHE skills from ${CODEX_HOME}..."

for skill_name in "${MANAGED_SKILLS[@]}"; do
  rm -rf "${CODEX_HOME}/skills/${skill_name}"
done

rm -rf "${SHARED_DIR}"

echo "AHE skills uninstalled successfully."
