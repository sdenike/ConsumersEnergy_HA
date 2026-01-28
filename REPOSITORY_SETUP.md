# Setting Up as a Git Repository for HACS

This guide shows how to publish this integration as a GitHub repository and install it via HACS (Home Assistant Community Store).

## Why Use Git + HACS?

- ✅ One-click installation through HACS
- ✅ Automatic update notifications
- ✅ No manual file uploads needed
- ✅ Version control and change tracking
- ✅ Easy to share with community
- ✅ Standard Home Assistant workflow

---

## Part 1: Create GitHub Repository

### Step 1: Initialize Git Repository

In your terminal (in this directory):

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial release v1.0.0 - Consumers Energy Cost Tracker"

# Create a tag for the release
git tag -a v1.0.0 -m "Release version 1.0.0"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository settings:
   - **Name:** `consumers-energy-cost-tracker` (or your preferred name)
   - **Description:** "Home Assistant integration for real-time electricity cost tracking with Consumers Energy rate plans"
   - **Public** or **Private** (HACS works with both)
   - **DO NOT** check "Initialize with README" (we already have one)
3. Click "Create repository"

### Step 3: Push to GitHub

GitHub will show you commands. Run them:

```bash
# Add remote origin (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/consumers-energy-cost-tracker.git

# Push code and tags
git branch -M main
git push -u origin main
git push --tags
```

### Step 4: Create GitHub Release

1. Go to your repository on GitHub
2. Click "Releases" (right sidebar)
3. Click "Create a new release"
4. Fill in:
   - **Tag:** Select `v1.0.0` (the tag we created)
   - **Release title:** `v1.0.0 - Initial Release`
   - **Description:** Copy from `CHANGELOG.md` or write:
     ```markdown
     ## First Release

     Complete Home Assistant integration for Consumers Energy cost tracking.

     ### Features
     - Multi-sensor power aggregation
     - Time-of-use and seasonal pricing
     - Three preset Consumers Energy rate plans
     - Real-time cost tracking (30-second updates)
     - Daily, weekly, monthly, yearly accumulators
     - Energy Dashboard integration
     - 12 sensor entities

     ### Installation
     Install via HACS by adding this repository as a custom repository.

     See README.md for full documentation.
     ```
5. Click "Publish release"

---

## Part 2: Install via HACS

### For You (Repository Owner)

#### Step 1: Install HACS (if not installed)

1. If you don't have HACS:
   - Visit https://hacs.xyz/docs/setup/download
   - Follow installation instructions
   - Restart Home Assistant
   - Complete HACS setup wizard

#### Step 2: Add Custom Repository to HACS

1. In Home Assistant, click "HACS" in the sidebar
2. Click "Integrations"
3. Click the three dots menu (⋮) in the top right
4. Select "Custom repositories"
5. Add your repository:
   - **Repository:** `https://github.com/YOUR_USERNAME/consumers-energy-cost-tracker`
   - **Category:** Integration
6. Click "Add"

#### Step 3: Install the Integration

1. Click the "+ Explore & Download Repositories" button
2. Search for "Consumers Energy"
3. Click "Consumers Energy Cost Tracker"
4. Click "Download"
5. Select version (v1.0.0)
6. Click "Download"
7. Restart Home Assistant

#### Step 4: Configure

1. Go to Settings > Devices & Services
2. Click "+ Add Integration"
3. Search "Consumers Energy Cost Tracker"
4. Follow the configuration wizard

---

## Part 3: Making it Official (Optional)

### Submit to HACS Default Repository

To make your integration available to everyone without custom repository setup:

1. **Meet HACS Requirements:**
   - ✅ Repository is public
   - ✅ Has proper README.md
   - ✅ Has hacs.json
   - ✅ Has LICENSE file
   - ✅ Has releases with proper versioning
   - ✅ Code follows Home Assistant standards

2. **Submit for Review:**
   - Go to https://github.com/hacs/default
   - Click "Issues" > "New Issue"
   - Select "Add repository to HACS"
   - Fill in the template with your repository URL
   - Submit and wait for review

3. **Once Approved:**
   - Your integration appears in HACS default list
   - Users can install without adding custom repository
   - Wider community reach

---

## Part 4: Repository Best Practices

### Recommended Repository Structure

```
consumers-energy-cost-tracker/
├── .github/
│   └── workflows/              (Optional: CI/CD)
├── custom_components/
│   └── consumers_energy_cost/  (Your integration)
├── examples/
│   └── dashboard.yaml
├── tests/
│   └── test_*.py
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
├── SETUP_GUIDE.md
├── hacs.json
└── info.md                     (Optional: HACS info page)
```

### Add an info.md for HACS (Optional)

Create `info.md` in the root:

```markdown
# Consumers Energy Cost Tracker

Real-time electricity cost tracking with time-of-use and seasonal pricing.

## Features
- Aggregate multiple power sensors
- Time-of-use and seasonal pricing
- Three preset Consumers Energy rate plans
- Real-time cost tracking (30-second updates)
- Daily, weekly, monthly, yearly tracking
- Energy Dashboard integration

## Installation

1. Install via HACS
2. Restart Home Assistant
3. Add integration: Settings > Devices & Services > Add Integration
4. Search "Consumers Energy Cost Tracker"
5. Follow setup wizard

## Documentation

Full documentation available in the [README](https://github.com/YOUR_USERNAME/consumers-energy-cost-tracker/blob/main/README.md).

## Support

Report issues on [GitHub](https://github.com/YOUR_USERNAME/consumers-energy-cost-tracker/issues).
```

### Update hacs.json

Already created, but verify it has:

```json
{
  "name": "Consumers Energy Cost Tracker",
  "render_readme": true,
  "domains": ["sensor"],
  "homeassistant": "2024.1.0"
}
```

---

## Part 5: Future Updates

### When You Make Changes

```bash
# Make your code changes
# Then commit them
git add .
git commit -m "Fix: Your fix description"
git push

# Create new release
git tag -a v1.0.1 -m "Release version 1.0.1"
git push --tags

# Create GitHub release
# Go to GitHub > Releases > Create new release
# Select v1.0.1 tag and publish
```

### Users Get Updates

1. HACS will notify them: "Update available"
2. They click "Update"
3. HACS downloads new version
4. They restart Home Assistant
5. Done!

---

## Part 6: Alternative - Private Repository

If you want to keep it private:

### Step 1: Make Repository Private

1. Go to repository Settings
2. Scroll to "Danger Zone"
3. Click "Change visibility" > "Make private"

### Step 2: Create Personal Access Token

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Click "Generate new token (classic)"
3. Name it "HACS Token"
4. Select scopes: `repo` (all)
5. Generate and copy the token

### Step 3: Add to HACS with Token

In HACS custom repository field:
```
https://YOUR_TOKEN@github.com/YOUR_USERNAME/consumers-energy-cost-tracker
```

Users you want to share with need:
- Your repository URL
- A personal access token with read access to your repo

---

## Comparison: Manual Upload vs Git Repository

| Feature | Manual Upload | Git + HACS |
|---------|--------------|------------|
| Installation Time | 10-15 min | 2 min |
| Updates | Manual re-upload | One click |
| Version Control | None | Full history |
| Rollback | Difficult | Easy |
| Sharing | Send zip file | Share repo URL |
| Update Notifications | None | Automatic |
| Community Contributions | Difficult | Pull requests |
| Professional | ❌ | ✅ |

---

## Quick Start for Git Repository Setup

**TL;DR - Complete setup in 5 minutes:**

```bash
# In your project directory
git init
git add .
git commit -m "Initial release v1.0.0"
git tag -a v1.0.0 -m "Release v1.0.0"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/consumers-energy-cost-tracker.git
git branch -M main
git push -u origin main
git push --tags

# Create GitHub release v1.0.0

# In HACS:
# Add custom repository > YOUR_REPO_URL > Integration
# Install > Restart HA > Configure
```

---

## Recommended Approach

**For personal use:** Git repository + HACS custom repository

**For public release:** Git repository + HACS custom repository, then submit to HACS default

**Not recommended:** Manual upload (unless absolutely necessary)

---

## Need Help?

**Git Issues:**
- GitHub Help: https://docs.github.com
- Git Documentation: https://git-scm.com/doc

**HACS Issues:**
- HACS Documentation: https://hacs.xyz
- HACS Discord: https://discord.gg/apgchf8

**Integration Issues:**
- Create issue on your GitHub repository
- Include Home Assistant logs
- Describe expected vs actual behavior

---

## Checklist for Repository Publication

- [ ] Git repository initialized
- [ ] All files committed
- [ ] Version tag created (v1.0.0)
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Tags pushed to GitHub
- [ ] GitHub release created
- [ ] README.md reviewed and accurate
- [ ] hacs.json present and valid
- [ ] LICENSE file included
- [ ] CHANGELOG.md up to date
- [ ] Tested installation via HACS
- [ ] Integration configures successfully
- [ ] All sensors working
- [ ] Documentation links correct

Once this checklist is complete, your integration is ready for the community! 🎉
