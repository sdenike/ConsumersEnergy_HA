# Quick Reference Card

## Installation (Choose One)

### 🏆 Git + HACS (Recommended)
```bash
./setup_repository.sh  # Run script, follow prompts
# Then add to HACS and install
```
**Time:** 7 minutes | **Updates:** Automatic

### 📦 Manual Upload
```
1. Download consumers_energy_cost.zip
2. Upload via File Editor to /config/custom_components/
3. Restart HA
```
**Time:** 15 minutes | **Updates:** Manual

## Configuration

```
Settings > Devices & Services > Add Integration
Search: "Consumers Energy Cost Tracker"
→ Select power sensors
→ Choose rate plan (Summer Time-of-Use for most users)
→ Done!
```

## 12 Sensors Created

| Sensor | Shows |
|--------|-------|
| `total_power` | Current watts |
| `current_rate` | $/kWh now |
| `cost_rate` | $/hour now |
| `rate_period` | Period name |
| `energy_today` | kWh today |
| `cost_today` | $ today |
| `energy_week` | kWh week |
| `cost_week` | $ week |
| `energy_month` | kWh month |
| `cost_month` | $ month |
| `energy_year` | kWh year |
| `cost_year` | $ year |

## Rate Plans

**Summer Time-of-Use (Rate 1001)** - Most common
- Summer on-peak: $0.23/kWh (weekdays 2-7pm)
- Summer off-peak: $0.178/kWh
- Winter: $0.164/kWh

**Smart Hours (Rate 1040)** - Advanced TOU

**Nighttime Savers (Rate 1050)** - Three-tier

## Dashboard Quick Add

```yaml
type: entities
entities:
  - sensor.consumers_energy_total_power
  - sensor.consumers_energy_current_rate
  - sensor.consumers_energy_cost_today
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Integration not found | Check logs, verify path, restart |
| Sensors "Unknown" | Wait 2 min for first update |
| Wrong costs | Verify rate plan on bill |
| Rate doesn't change | Check timezone, verify weekday |

## File Guide

| Need | Read |
|------|------|
| Start | START_HERE.md |
| Compare methods | INSTALLATION_OPTIONS.md |
| Install via HACS | REPOSITORY_SETUP.md |
| Install manually | INSTALL_VIA_WEB_UI.md |
| Quick setup | QUICK_START.md |
| Detailed help | SETUP_GUIDE.md |
| Dashboard | examples/dashboard.yaml |
| Testing | VERIFICATION_CHECKLIST.md |

## Quick Commands

```bash
# Setup Git repo
./setup_repository.sh

# Check installation
ls /config/custom_components/consumers_energy_cost/

# View logs
# Settings > System > Logs, search "consumers_energy"

# Restart HA
# Developer Tools > YAML > Restart
```

## Support

- Logs: Settings > System > Logs
- Verify: VERIFICATION_CHECKLIST.md
- Help: SETUP_GUIDE.md troubleshooting

## Quick Start Path

1. Read START_HERE.md (5 min)
2. Install via chosen method (7-15 min)
3. Configure integration (5 min)
4. Add dashboard cards (5 min)
5. Monitor 24 hours
6. Verify accuracy

**Total:** 20-30 minutes to full operation

---

**Version:** 1.0.0 | **Files:** 23 | **Status:** ✅ Ready
