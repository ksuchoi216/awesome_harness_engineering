#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

echo "Installing awesome_harness_engineering globally..."
sudo npm install -g .

echo "Installation complete!"
echo "You can now run 'ahe install' to install the Codex skills."
