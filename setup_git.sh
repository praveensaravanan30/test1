#!/bin/bash
# Script to configure git and complete the commit

set -e

cd "$(dirname "$0")"

echo "🔧 Configuring git for this repository..."

# Configure git user (you can change these values)
git config user.email "praveen@example.com"
git config user.name "Praveen"

echo "✅ Git configured!"
echo ""
echo "Current git config:"
git config --list | grep user
echo ""

# Check if there are uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Uncommitted changes found:"
    git status --short
    echo ""
    read -p "Would you like to commit these changes now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📦 Staging and committing changes..."
        git add -A
        git commit -m "Fix baseline: Use incomplete skeleton for patch compatibility"
        echo "✅ Changes committed!"
        echo ""
        read -p "Would you like to push to origin? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            CURRENT_BRANCH=$(git branch --show-current)
            echo "🚀 Pushing to origin/$CURRENT_BRANCH..."
            git push origin "$CURRENT_BRANCH"
            echo "✅ Pushed successfully!"
        fi
    fi
else
    echo "✅ No uncommitted changes found."
fi

