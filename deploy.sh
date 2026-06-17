#!/usr/bin/env bash
set -euo pipefail

# awesome_harness_engineering npm deploy script

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

echo "Starting NPM deployment preparation..."

# Check if user is logged into npm
if ! npm whoami > /dev/null 2>&1; then
    echo "You are not logged into npm. Please run 'npm login' first."
    echo "If you don't have an account, sign up at https://www.npmjs.com/"
    exit 1
fi

echo "Logged in as: $(npm whoami)"

# Check current git branch
ORIGINAL_BRANCH=$(git rev-parse --abbrev-ref HEAD)
SWITCHED_BRANCH=0

if [ "$ORIGINAL_BRANCH" != "master" ]; then
    echo "---"
    echo "⚠️  WARNING: You are currently on branch '$ORIGINAL_BRANCH'."
    echo "Standard practice is to publish stable npm releases from the 'master' branch."
    read -p "Do you want to switch to 'master' for publishing, and then return to '$ORIGINAL_BRANCH'? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Ensure working tree is clean before switching
        if ! git diff-index --quiet HEAD --; then
            echo "Error: Your working tree is not clean. Please commit or stash your changes first."
            exit 1
        fi
        git checkout master
        SWITCHED_BRANCH=1
        echo "Switched to 'master' for deployment."
    else
        read -p "Are you sure you want to publish directly from '$ORIGINAL_BRANCH'? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Deployment aborted."
            exit 0
        fi
    fi
fi

# Set a trap to ensure we always return to the original branch if we switched
cleanup() {
    if [ "$SWITCHED_BRANCH" -eq 1 ]; then
        echo "---"
        echo "Returning to original branch: $ORIGINAL_BRANCH"
        git checkout "$ORIGINAL_BRANCH"
    fi
}
trap cleanup EXIT

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
