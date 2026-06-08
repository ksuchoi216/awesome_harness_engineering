#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR=".codex/skills/ahe"

if [ -d "${TARGET_DIR}" ]; then
  echo "Uninstalling AHE skill..."
  rm -rf "${TARGET_DIR}"
  echo "AHE skill uninstalled successfully."
else
  echo "AHE skill is not installed (directory ${TARGET_DIR} not found)."
fi
