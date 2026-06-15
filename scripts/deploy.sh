#!/usr/bin/env bash
set -euo pipefail

# awesome_harness_engineering npm deploy script

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(CDPATH= cd -- "${SCRIPT_DIR}/.." && pwd)"

cd "${PACKAGE_ROOT}"

echo "Starting NPM deployment preparation..."

# Check if user is logged into npm
if ! npm whoami > /dev/null 2>&1; then
    echo "You are not logged into npm. Please run 'npm login' first."
    echo "If you don't have an account, sign up at https://www.npmjs.com/"
    exit 1
fi

echo "Logged in as: $(npm whoami)"

# Run pre-publish dry run to check what will be packed
echo "---"
echo "Running dry-run pack to verify contents..."
npm pack --dry-run
echo "---"

# Ask for confirmation
read -p "Does the packed file list look correct? Are you ready to publish to npm? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment aborted."
    exit 0
fi

# Publish the package (this will automatically run the prepublishOnly test script)
echo "Publishing package to npm..."
if npm publish; then
    echo "Successfully published to npm!"
    echo "You can now install the package globally with: npm install -g @ksuchoi216/ahe"
else
    echo "Failed to publish to npm. Check the error messages above."
    exit 1
fi
