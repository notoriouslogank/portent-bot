#!/usr/bin/env bash
set -euo pipefail

# Guard: run only on main
branch=$(git rev-parse --abbrev-ref HEAD)
if [[ "$branch" != "main" && "$branch" != "master" ]]; then
    echo "STOP.  Release only from main/master (you are on: $branch)"; exit 1
fi

# Ensure clean tree
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "STOP.  Uncommited changes present.  Commit or stash first."; exit 1
fi

# Infer bump from conventional commits (feat/fix/BREAKING)
# If nothing matches since last tag, cz exits non-zero; handle gracefully
if ! cz bump --yes; then
    echo "No bump (no new conventional commits). Exiting."
    exit 0
fi

# Grab new version & tag
VERSION=$(cz version --project)
TAG="v${VERSION}"

git push && git push --tags

# Create GH release from CHANGELOG
if command -v gh >/dev/null 2>&1; then
    NOTES=$(awk "\^## \\[?${VERSION}\\]?/{flag=1;next}/^## {flag=0}flag" CHANGELOG.md || true)
    gh release create "$TAG" --title "Portent $VERSION" --notes "${NOTES:-"Release $VERSION}"
else
    echo "Install GitHub CLI to auto-create Release page (optional)"
fi

echo "Released $TAG"
