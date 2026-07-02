#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

echo "Starting local npm release validation..."
echo "Current branch: $(git rev-parse --abbrev-ref HEAD)"

PACKAGE_NAME=$(node -p "require('./package.json').name")
PACKAGE_VERSION=$(node -p "require('./package.json').version")

echo "---"
echo "Checking if ${PACKAGE_NAME}@${PACKAGE_VERSION} already exists on npm..."
if npm view "${PACKAGE_NAME}@${PACKAGE_VERSION}" version >/dev/null 2>&1; then
    echo "Error: Version ${PACKAGE_VERSION} of ${PACKAGE_NAME} already exists on npm registry!"
    echo "Please bump the version in package.json before proceeding."
    exit 1
fi
echo "Version ${PACKAGE_VERSION} is available."
echo "---"
echo "Running package tests..."
npm test
echo "---"
echo "Running dry-run pack to verify contents..."
npm pack --dry-run
echo "---"
echo "Local validation passed."
echo "Actual npm publish is handled by GitHub Actions."
