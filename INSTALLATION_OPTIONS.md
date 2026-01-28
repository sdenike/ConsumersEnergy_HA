# Installation Options - Which Method Should You Choose?

You have **three ways** to install this integration. Here's how to choose:

---

## 🏆 Option 1: Git Repository + HACS (RECOMMENDED)

**Best for:** Everyone, especially if you want updates

### Pros:
- ✅ **One-click installation** through HACS interface
- ✅ **Automatic updates** - get notified when new versions are available
- ✅ **Professional** - standard Home Assistant workflow
- ✅ **Easy sharing** - just share the repository URL
- ✅ **Version control** - can rollback if needed
- ✅ **Community ready** - others can contribute improvements

### Cons:
- ⚠️ Requires GitHub account (free)
- ⚠️ Need to create repository first (5 minutes, one-time)
- ⚠️ Requires HACS installed (if not already)

### Time Required:
- **Setup:** 5 minutes (one-time)
- **Installation:** 2 minutes (through HACS)
- **Updates:** 30 seconds (click button in HACS)

### When to Choose This:
- ✅ You plan to use this long-term
- ✅ You want automatic update notifications
- ✅ You're comfortable with GitHub
- ✅ You might share this with others

### How to Set Up:
1. Run the setup script:
   ```bash
   ./setup_repository.sh
   ```
2. Follow the prompts
3. Create GitHub repository (script will guide you)
4. Push to GitHub
5. Add to HACS as custom repository
6. Install through HACS

**Detailed guide:** See `REPOSITORY_SETUP.md`

---

## 📦 Option 2: Manual Upload via Web UI

**Best for:** Quick testing or if you don't want GitHub

### Pros:
- ✅ No GitHub account needed
- ✅ No command line needed
- ✅ Works through Home Assistant web interface
- ✅ Good for private/personal use

### Cons:
- ⚠️ Manual file uploads (can be tedious)
- ⚠️ No automatic updates
- ⚠️ Must manually re-upload for updates
- ⚠️ Harder to share with others
- ⚠️ No version control

### Time Required:
- **Installation:** 10-15 minutes
- **Updates:** 10-15 minutes (full re-upload)

### When to Choose This:
- ✅ You want to test before committing to Git
- ✅ You don't have/want a GitHub account
- ✅ You only plan to use this on one system
- ✅ You won't need updates

### How to Install:
1. Download `consumers_energy_cost.zip`
2. Use File Editor or Studio Code Server add-on
3. Extract to `/config/custom_components/`
4. Restart Home Assistant
5. Configure integration

**Detailed guide:** See `INSTALL_VIA_WEB_UI.md`

---

## 💾 Option 3: Direct File Copy (Advanced)

**Best for:** Users with direct file access (SSH, Samba)

### Pros:
- ✅ Fastest if you have file access
- ✅ No web UI uploads needed
- ✅ Can use command line tools

### Cons:
- ⚠️ Requires SSH, Samba, or direct file system access
- ⚠️ No automatic updates
- ⚠️ Manual process for updates

### Time Required:
- **Installation:** 2-3 minutes
- **Updates:** 2-3 minutes

### When to Choose This:
- ✅ You have SSH or Samba access
- ✅ You're comfortable with terminal/file copying
- ✅ You want quick installation

### How to Install:
```bash
# Via SSH or terminal
cd /config
unzip consumers_energy_cost.zip
ha core restart
```

**Detailed guide:** See `INSTALL_VIA_WEB_UI.md` (Method 3 or 4)

---

## Comparison Table

| Feature | Git + HACS | Web UI Upload | Direct Copy |
|---------|-----------|---------------|-------------|
| **Installation Time** | 2 min | 10-15 min | 2-3 min |
| **Setup Time** | 5 min (one-time) | 0 min | 0 min |
| **Update Time** | 30 sec | 10-15 min | 2-3 min |
| **Automatic Updates** | ✅ Yes | ❌ No | ❌ No |
| **Requires GitHub** | ✅ Yes | ❌ No | ❌ No |
| **Requires File Access** | ❌ No | ❌ No | ✅ Yes |
| **Version Control** | ✅ Yes | ❌ No | ❌ No |
| **Easy Sharing** | ✅ Yes | ⚠️ Send zip | ⚠️ Send zip |
| **Rollback** | ✅ Easy | ❌ Hard | ❌ Hard |
| **Professional** | ✅ Yes | ❌ No | ❌ No |
| **Community Ready** | ✅ Yes | ❌ No | ❌ No |

---

## Our Recommendation

### For Most Users: **Option 1 (Git + HACS)** 🏆

**Why?**
- Initial setup takes 5 minutes, but you save time on every future update
- You get notified when updates are available
- You can easily rollback if something breaks
- It's the standard way Home Assistant integrations are distributed
- You can share it with others easily

**The 5-minute setup is worth it for:**
- Automatic update notifications
- One-click updates forever
- Professional appearance
- Easy sharing

### For Testing Only: **Option 2 (Web UI Upload)**

**Use this if:**
- You want to test the integration first
- You're not sure you'll use it long-term
- You absolutely don't want to use GitHub

**But consider:** You can always switch to Git later!

### For Advanced Users with Access: **Option 3 (Direct Copy)**

**Use this if:**
- You have SSH or Samba already set up
- You're comfortable with terminal
- You don't need updates

---

## Decision Flow Chart

```
Do you have a GitHub account (or willing to create one)?
│
├─ YES → Do you want automatic updates?
│   │
│   ├─ YES → Use Option 1: Git + HACS ✅ (RECOMMENDED)
│   │
│   └─ NO → Do you have SSH/Samba access?
│       │
│       ├─ YES → Use Option 3: Direct Copy
│       │
│       └─ NO → Use Option 2: Web UI Upload
│
└─ NO → Are you just testing?
    │
    ├─ YES → Use Option 2: Web UI Upload (then switch to Git later)
    │
    └─ NO → Do you have SSH/Samba access?
        │
        ├─ YES → Use Option 3: Direct Copy
        │
        └─ NO → Use Option 2: Web UI Upload
```

---

## Quick Start by Option

### Option 1: Git + HACS
```bash
# 1. Run setup script
./setup_repository.sh

# 2. Create GitHub repo (follow script instructions)

# 3. Push to GitHub
git push -u origin main
git push --tags

# 4. Add to HACS custom repositories

# 5. Install through HACS
```
**Time:** 7 minutes total (5 min setup + 2 min install)

### Option 2: Web UI Upload
```
1. Download consumers_energy_cost.zip
2. Open File Editor in Home Assistant
3. Upload files to /config/custom_components/
4. Restart HA
5. Configure integration
```
**Time:** 10-15 minutes

### Option 3: Direct Copy
```bash
# Via SSH
cd /config
scp user@computer:/path/to/consumers_energy_cost.zip .
unzip consumers_energy_cost.zip
ha core restart
```
**Time:** 2-3 minutes

---

## Frequently Asked Questions

### Can I switch methods later?
**Yes!** You can:
- Start with Web UI Upload, then move to Git later
- Switch from Direct Copy to Git + HACS
- Any combination works

### Do I need to know Git?
**No!** The setup script handles everything. You just need:
1. A GitHub account
2. Run one script
3. Follow the prompts

### What if I don't want my code public?
- GitHub repositories can be **private** (free)
- HACS works with private repositories
- Use a personal access token for HACS

### Which method do you use?
**We recommend Git + HACS** for everyone. It's worth the 5-minute setup.

### Can I use this without HACS?
**Yes!** Options 2 and 3 don't require HACS at all.

---

## Support

Need help deciding or setting up?

- **Git + HACS:** See `REPOSITORY_SETUP.md`
- **Web UI Upload:** See `INSTALL_VIA_WEB_UI.md`
- **General Setup:** See `SETUP_GUIDE.md`
- **Quick Start:** See `QUICK_START.md`

---

## Bottom Line

**For long-term use:** Git + HACS (Option 1) 🏆

**For quick testing:** Web UI Upload (Option 2)

**For advanced users:** Direct Copy (Option 3)

**Most popular choice:** 90% of users choose Git + HACS because automatic updates are worth it!

---

Start with the method you're most comfortable with. You can always change later!
