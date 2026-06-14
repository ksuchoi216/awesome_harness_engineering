#!/usr/bin/env bash
set -euo pipefail

readonly CODEX_HOME="${HOME}/.codex"
readonly SHARED_DIR="${CODEX_HOME}/ahe-shared"
readonly HOOKS_DIR="${CODEX_HOME}/hooks"
readonly MANAGED_SKILLS=(
  "ahe-init"
  "ahe-conversation"
  "ahe-spec"
  "ahe-update"
  "ahe-clear"
  "ahe-help"
)

echo "Uninstalling AHE skills from ${CODEX_HOME}..."

for skill_name in "${MANAGED_SKILLS[@]}"; do
  rm -rf "${CODEX_HOME}/skills/${skill_name}"
done

rm -rf "${SHARED_DIR}"
rm -rf "${HOOKS_DIR}"

echo "AHE skills uninstalled successfully."
