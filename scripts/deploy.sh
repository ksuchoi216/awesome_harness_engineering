#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

echo "Starting NPM deployment preparation..."

if ! npm whoami > /dev/null 2>&1; then
    echo "You are not logged into npm. Please run 'npm login' first."
    echo "If you don't have an account, sign up at https://www.npmjs.com/"
    exit 1
fi

echo "Logged in as: $(npm whoami)"

ORIGINAL_BRANCH=$(git rev-parse --abbrev-ref HEAD)
SWITCHED_BRANCH=0

if [ "$ORIGINAL_BRANCH" != "master" ]; then
    echo "---"
    echo "WARNING: You are currently on branch '$ORIGINAL_BRANCH'."
    echo "Standard practice is to publish stable npm releases from the 'master' branch."
    read -p "Do you want to switch to 'master' for publishing, and then return to '$ORIGINAL_BRANCH'? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
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

cleanup() {
    if [ "$SWITCHED_BRANCH" -eq 1 ]; then
        echo "---"
        echo "Returning to original branch: $ORIGINAL_BRANCH"
        git checkout "$ORIGINAL_BRANCH"
    fi
}
trap cleanup EXIT

echo "---"
echo "Running dry-run pack to verify contents..."
npm pack --dry-run
echo "---"

read -p "Does the packed file list look correct? Are you ready to publish to npm? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment aborted."
    exit 0
fi

echo "Publishing package to npm..."
if npm publish; then
    echo "Successfully published to npm!"
    echo "You can now install the package globally with: npm install -g @ksuchoi216/ahe"
else
    echo "Failed to publish to npm. Check the error messages above."
    exit 1
fi
