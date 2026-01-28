#!/bin/bash

# Consumers Energy Cost Tracker - Git Repository Setup Script
# This script automates the creation of a Git repository and prepares it for GitHub

set -e  # Exit on error

echo "=========================================="
echo "Consumers Energy Cost Tracker"
echo "Git Repository Setup Script"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed"
    echo "Please install Git first: https://git-scm.com/downloads"
    exit 1
fi

# Check if we're already in a git repository
if [ -d .git ]; then
    echo "⚠️  Warning: This directory is already a Git repository"
    read -p "Do you want to continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

# Get user information
echo "📝 Please provide the following information:"
echo ""
read -p "Your GitHub username: " GITHUB_USERNAME
read -p "Repository name [consumers-energy-cost-tracker]: " REPO_NAME
REPO_NAME=${REPO_NAME:-consumers-energy-cost-tracker}

echo ""
echo "📋 Summary:"
echo "   GitHub Username: $GITHUB_USERNAME"
echo "   Repository Name: $REPO_NAME"
echo "   Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
read -p "Is this correct? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted. Please run the script again."
    exit 0
fi

echo ""
echo "🚀 Setting up Git repository..."
echo ""

# Initialize git repository (if not already initialized)
if [ ! -d .git ]; then
    echo "1️⃣  Initializing Git repository..."
    git init
    echo "   ✅ Git repository initialized"
else
    echo "1️⃣  Using existing Git repository..."
fi

# Configure git user if not set
if [ -z "$(git config user.name)" ]; then
    echo "2️⃣  Configuring Git user..."
    read -p "   Your name: " GIT_NAME
    git config user.name "$GIT_NAME"
    read -p "   Your email: " GIT_EMAIL
    git config user.email "$GIT_EMAIL"
    echo "   ✅ Git user configured"
else
    echo "2️⃣  Git user already configured as: $(git config user.name)"
fi

# Add all files
echo "3️⃣  Adding files..."
git add .
echo "   ✅ Files added"

# Create initial commit
echo "4️⃣  Creating initial commit..."
if git diff --cached --quiet; then
    echo "   ⚠️  No changes to commit (already committed)"
else
    git commit -m "Initial release v1.0.0 - Consumers Energy Cost Tracker

Features:
- Multi-sensor power aggregation
- Time-of-use and seasonal pricing
- Three preset Consumers Energy rate plans
- Real-time cost tracking (30-second updates)
- Daily, weekly, monthly, yearly accumulators
- Energy Dashboard integration
- 12 sensor entities
- Complete documentation"
    echo "   ✅ Initial commit created"
fi

# Create version tag
echo "5️⃣  Creating version tag..."
if git tag | grep -q "^v1.0.0$"; then
    echo "   ⚠️  Tag v1.0.0 already exists"
else
    git tag -a v1.0.0 -m "Release version 1.0.0"
    echo "   ✅ Tag v1.0.0 created"
fi

# Check if remote already exists
if git remote | grep -q "^origin$"; then
    echo "6️⃣  Remote 'origin' already exists:"
    echo "   $(git remote get-url origin)"
    read -p "   Do you want to update it? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote remove origin
        git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
        echo "   ✅ Remote 'origin' updated"
    fi
else
    echo "6️⃣  Adding remote repository..."
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo "   ✅ Remote 'origin' added"
fi

echo ""
echo "=========================================="
echo "✅ Git Repository Setup Complete!"
echo "=========================================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Create GitHub repository:"
echo "   • Go to: https://github.com/new"
echo "   • Name: $REPO_NAME"
echo "   • Description: Home Assistant integration for real-time electricity cost tracking"
echo "   • DO NOT initialize with README (we already have one)"
echo "   • Click 'Create repository'"
echo ""
echo "2. Push code to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo "   git push --tags"
echo ""
echo "3. Create GitHub Release:"
echo "   • Go to: https://github.com/$GITHUB_USERNAME/$REPO_NAME/releases/new"
echo "   • Tag: v1.0.0"
echo "   • Title: v1.0.0 - Initial Release"
echo "   • Copy description from CHANGELOG.md"
echo "   • Click 'Publish release'"
echo ""
echo "4. Install via HACS:"
echo "   • Open HACS in Home Assistant"
echo "   • Go to Integrations"
echo "   • Click ⋮ menu > Custom repositories"
echo "   • Add: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "   • Category: Integration"
echo "   • Install the integration"
echo "   • Restart Home Assistant"
echo ""
echo "📚 For detailed instructions, see: REPOSITORY_SETUP.md"
echo ""
echo "🎉 Happy automating!"
echo ""
