#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

echo "Starting local npm release validation..."
echo "Current branch: $(git rev-parse --abbrev-ref HEAD)"

PACKAGE_NAME=$(node -p "require('./package.json').name")
PACKAGE_VERSION=$(node -p "require('./package.json').version")

echo "Checking package version alignment..."
CODEX_VERSION=$(node -p "require('./packages/ahe-codex/package.json').version")
ANTIGRAVITY_VERSION=$(node -p "require('./packages/ahe-antigravity/package.json').version")

if [ "${PACKAGE_VERSION}" != "${CODEX_VERSION}" ]; then
    echo "Error: Root package version (${PACKAGE_VERSION}) does not match @ahe/codex version (${CODEX_VERSION})!" >&2
    exit 1
fi

if [ "${PACKAGE_VERSION}" != "${ANTIGRAVITY_VERSION}" ]; then
    echo "Error: Root package version (${PACKAGE_VERSION}) does not match @ahe/antigravity version (${ANTIGRAVITY_VERSION})!" >&2
    exit 1
fi
echo "Package version alignment verified successfully (${PACKAGE_VERSION})."


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
if command -v docker >/dev/null 2>&1; then
    echo "🐳 Docker detected. Running tests in an isolated CI-like container to prevent environment mismatch..."
    docker run --rm -v "$PWD:/app" -w /app python:3.11-slim bash -c "
        apt-get update -qq && apt-get install -y -qq nodejs npm && \\
        pip install -q pytest && \\
        npm test
    " || {
        echo "❌ Tests failed in CI-like container environment!"
        exit 1
    }
else
    echo "⚠️ Docker not found. Running tests locally (Warning: this might not catch CI-specific environment issues)..."
    npm test
fi
echo "---"
echo "Running dry-run pack to verify contents..."
npm pack --dry-run
echo "---"
echo "Local validation passed."
echo "Actual npm publish is handled by GitHub Actions."
