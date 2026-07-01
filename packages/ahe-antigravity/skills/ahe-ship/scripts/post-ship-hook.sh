#!/usr/bin/env bash
set -euo pipefail

PLAN_PATH="$1"

if [ -f "${PLAN_PATH}" ]; then
  echo "Running AHE Ship post-execution hook..."
  rm -f "${PLAN_PATH}"
  echo "Cleaned up plan file: ${PLAN_PATH}"
else
  echo "Warning: Plan file not found at ${PLAN_PATH}"
fi
