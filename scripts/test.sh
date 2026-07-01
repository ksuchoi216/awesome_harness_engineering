#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

echo "Starting local npm release validation..."
echo "Current branch: $(git rev-parse --abbrev-ref HEAD)"
echo "---"
echo "Running package tests..."
npm test
echo "---"
echo "Running dry-run pack to verify contents..."
npm pack --dry-run
echo "---"
echo "Local validation passed."
echo "Actual npm publish is handled by GitHub Actions."
