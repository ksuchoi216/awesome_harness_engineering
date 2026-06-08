#!/usr/bin/env bash
set -euo pipefail

echo "Installing AHE skill locally..."
npx --yes --package=file:. ahe install "$@"
