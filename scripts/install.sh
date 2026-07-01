#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

echo "Uninstalling awesome_harness_engineering Codex skills..."
./bin/ahe uninstall || true

echo "Installing awesome_harness_engineering globally..."
sudo npm install -g .

echo "Installing Codex and Antigravity skills..."
./bin/ahe install --force

echo "Installation complete!"
