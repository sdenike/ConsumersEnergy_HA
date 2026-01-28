# Install via Home Assistant Web UI

This guide shows how to install the Consumers Energy Cost Tracker integration by uploading files through the Home Assistant web interface.

## Prerequisites

You need **ONE** of these add-ons installed:
- **File Editor** (recommended - easier for beginners)
- **Studio Code Server** (advanced - full IDE)
- **Samba Share** (alternative - use file explorer)

---

## Method 1: Using File Editor Add-on (Recommended)

### Step 1: Install File Editor (if not already installed)

1. Go to Settings > Add-ons > Add-on Store
2. Search for "File Editor"
3. Click "File Editor" by Home Assistant Community Add-ons
4. Click "Install"
5. After installation, toggle "Show in sidebar"
6. Click "Start"

### Step 2: Download the Integration Package

1. Download `consumers_energy_cost.zip` from this repository
2. Save it to your computer

### Step 3: Extract and Upload Files

**Option A: Upload Individual Files (Easier)**

1. In Home Assistant, click "File Editor" in the sidebar
2. Navigate to the root directory (you should see folders like `configuration.yaml`)
3. Create the directory structure:
   - Click the folder icon (top right) > "New folder"
   - Name it `custom_components` (if it doesn't exist)
   - Open `custom_components`
   - Create a new folder named `consumers_energy_cost`

4. Upload the integration files:
   - Open `custom_components/consumers_energy_cost/`
   - Click the upload icon (📤)
   - Upload each file from the zip's `custom_components/consumers_energy_cost/` folder:
     - `__init__.py`
     - `config_flow.py`
     - `const.py`
     - `coordinator.py`
     - `manifest.json`
     - `rate_calculator.py`
     - `sensor.py`
     - `strings.json`

5. Create translations folder:
   - Inside `consumers_energy_cost/`, create folder `translations`
   - Upload `en.json` to the `translations` folder

**Option B: Use Terminal to Extract Zip**

1. Upload `consumers_energy_cost.zip` to the root of your config directory using File Editor
2. In Home Assistant, go to Settings > System > Terminal (or install Terminal add-on)
3. Run these commands:
   ```bash
   cd /config
   unzip -o consumers_energy_cost.zip
   rm consumers_energy_cost.zip
   ```

### Step 4: Verify Installation

1. In File Editor, verify you have this structure:
   ```
   /config/
   ├── custom_components/
   │   └── consumers_energy_cost/
   │       ├── __init__.py
   │       ├── config_flow.py
   │       ├── const.py
   │       ├── coordinator.py
   │       ├── manifest.json
   │       ├── rate_calculator.py
   │       ├── sensor.py
   │       ├── strings.json
   │       └── translations/
   │           └── en.json
   └── configuration.yaml
   ```

2. Check file sizes (should not be 0 bytes)

### Step 5: Restart Home Assistant

1. Go to Developer Tools > YAML
2. Click "Restart" > "Restart Home Assistant"
3. Wait for HA to come back online (1-2 minutes)

### Step 6: Add the Integration

1. Go to Settings > Devices & Services
2. Click "+ Add Integration" (bottom right)
3. Search for "Consumers Energy"
4. Click "Consumers Energy Cost Tracker"
5. Follow the configuration wizard

---

## Method 2: Using Studio Code Server Add-on

### Step 1: Install Studio Code Server (if not installed)

1. Go to Settings > Add-ons > Add-on Store
2. Search for "Studio Code Server"
3. Click "Studio Code Server" by Home Assistant Community Add-ons
4. Click "Install"
5. After installation, toggle "Show in sidebar"
6. Click "Start"
7. Click "Open Web UI"

### Step 2: Upload and Extract

1. In VS Code, open the File Explorer (left sidebar)
2. You should see your `/config` directory
3. Drag and drop `consumers_energy_cost.zip` into the file explorer
4. Right-click the zip file > "Extract Archive"
5. It will extract to the current directory

### Step 3: Verify and Restart

1. Verify the `custom_components/consumers_energy_cost/` folder exists with all files
2. Delete the zip file (right-click > Delete)
3. Restart Home Assistant (Developer Tools > YAML > Restart)

---

## Method 3: Using Samba Share

### Step 1: Install Samba Share (if not installed)

1. Go to Settings > Add-ons > Add-on Store
2. Search for "Samba share"
3. Click "Samba share" by Home Assistant Community Add-ons
4. Click "Install"
5. Click "Start"

### Step 2: Connect to Share

**On Windows:**
1. Open File Explorer
2. In the address bar, type: `\\homeassistant.local` (or your HA IP: `\\192.168.x.x`)
3. Press Enter
4. Enter your Home Assistant credentials if prompted

**On macOS:**
1. In Finder, press Cmd+K
2. Enter: `smb://homeassistant.local` (or your HA IP)
3. Click Connect
4. Enter your Home Assistant credentials

**On Linux:**
1. Open your file manager
2. Connect to: `smb://homeassistant.local`

### Step 3: Extract and Copy Files

1. On your computer, extract `consumers_energy_cost.zip`
2. In the network share, navigate to the `config` folder
3. If `custom_components` folder doesn't exist, create it
4. Copy the entire `custom_components/consumers_energy_cost` folder from the extracted zip
5. Paste it into the `custom_components` folder on the network share

### Step 4: Restart and Configure

1. Restart Home Assistant
2. Add the integration as described above

---

## Method 4: Using SSH/Terminal (Advanced)

If you have SSH access or the Terminal add-on:

```bash
# Navigate to config directory
cd /config

# Download the zip (if hosted online)
# wget https://your-url/consumers_energy_cost.zip

# Or upload via File Editor first, then:
unzip -o consumers_energy_cost.zip

# Verify installation
ls -la custom_components/consumers_energy_cost/

# Clean up
rm consumers_energy_cost.zip

# Restart HA
ha core restart
```

---

## Troubleshooting

### Integration Doesn't Appear

**Cause:** Files not in correct location or HA not restarted

**Solution:**
1. Verify path: `/config/custom_components/consumers_energy_cost/`
2. Check that `manifest.json` exists and is not empty
3. Check logs: Settings > System > Logs (search for "consumers_energy")
4. Restart Home Assistant again

### "Module not found" Error

**Cause:** Files didn't upload correctly or have wrong permissions

**Solution:**
1. Verify all `.py` files are present and not 0 bytes
2. Check file permissions (should be readable)
3. Re-upload files
4. Restart HA

### File Editor Upload Fails

**Cause:** File too large or add-on not configured

**Solution:**
1. Try uploading files one at a time
2. Check File Editor configuration (Settings > Add-ons > File Editor)
3. Increase file size limits if needed
4. Use Method 2 (VS Code) or Method 3 (Samba) instead

### Can't Find custom_components Folder

**Solution:**
1. You're probably in the wrong directory
2. In File Editor, click the folder icon at the top
3. Navigate to the root (where `configuration.yaml` is)
4. Create `custom_components` folder if it doesn't exist

---

## Quick Verification Commands

If you have Terminal access, verify installation:

```bash
# Check if folder exists
ls -la /config/custom_components/consumers_energy_cost/

# Check manifest
cat /config/custom_components/consumers_energy_cost/manifest.json

# Count Python files (should be 5)
ls /config/custom_components/consumers_energy_cost/*.py | wc -l

# Check for syntax errors
python3 -m py_compile /config/custom_components/consumers_energy_cost/*.py
```

Expected output:
```
total XX
-rw-r--r-- 1 root root   4XXX __init__.py
-rw-r--r-- 1 root root   9XXX config_flow.py
-rw-r--r-- 1 root root   5XXX const.py
-rw-r--r-- 1 root root   8XXX coordinator.py
-rw-r--r-- 1 root root    XXX manifest.json
-rw-r--r-- 1 root root   3XXX rate_calculator.py
-rw-r--r-- 1 root root  10XXX sensor.py
-rw-r--r-- 1 root root   1XXX strings.json
drwxr-xr-x 2 root root   XXXX translations
```

---

## After Installation

Once installed successfully:

1. **Configure the integration:**
   - Settings > Devices & Services > Add Integration
   - Search "Consumers Energy Cost Tracker"

2. **Follow the Quick Start:**
   - See `QUICK_START.md` for 10-minute setup

3. **Verify sensors:**
   - Developer Tools > States
   - Search for "consumers_energy"
   - Should see 12 sensors

4. **Add to dashboard:**
   - See `examples/dashboard.yaml` for card configurations

---

## Files Included in Package

```
consumers_energy_cost.zip
├── custom_components/
│   └── consumers_energy_cost/
│       ├── __init__.py              (Integration setup)
│       ├── config_flow.py           (Configuration UI)
│       ├── const.py                 (Constants & rate plans)
│       ├── coordinator.py           (Data coordinator)
│       ├── manifest.json            (Integration metadata)
│       ├── rate_calculator.py       (Rate calculation)
│       ├── sensor.py                (12 sensor entities)
│       ├── strings.json             (UI translations)
│       └── translations/
│           └── en.json              (English translations)
├── examples/
│   └── dashboard.yaml               (Dashboard examples)
├── tests/
│   └── test_*.py                    (Unit tests)
├── README.md                        (Complete documentation)
├── SETUP_GUIDE.md                   (Detailed setup)
├── QUICK_START.md                   (10-minute guide)
├── VERIFICATION_CHECKLIST.md        (Testing checklist)
├── PROJECT_SUMMARY.md               (Technical overview)
├── CHANGELOG.md                     (Version history)
├── LICENSE                          (MIT License)
├── hacs.json                        (HACS metadata)
└── .gitignore                       (Git ignore rules)
```

**Only the `custom_components/consumers_energy_cost/` folder is required for the integration to work.** Other files are documentation and examples.

---

## Need Help?

1. Check Home Assistant logs: Settings > System > Logs
2. Review `SETUP_GUIDE.md` troubleshooting section
3. Verify file structure matches above
4. Try a different upload method
5. Report issues with full error logs

---

**Recommendation:** Use File Editor (Method 1, Option B with Terminal) for the easiest installation. Extract the zip using terminal commands, and you're done in 2 minutes!
