# Quick Start Guide

Get up and running with Consumers Energy Cost Tracker in 10 minutes.

## Prerequisites

- Home Assistant 2024.1.0 or newer
- At least one power sensor (watts) - examples:
  - Shelly Plug
  - TP-Link Kasa Smart Plug
  - Emporia Vue Energy Monitor
  - Sense Energy Monitor

## 5-Minute Installation

### Step 1: Install Integration (2 minutes)

```bash
# SSH into your Home Assistant server
cd /config

# Copy the integration
cp -r /path/to/custom_components/consumers_energy_cost custom_components/

# Restart Home Assistant
ha core restart
```

**OR** use File Editor in Home Assistant:
1. Go to Settings > Add-ons > File Editor
2. Upload `custom_components/consumers_energy_cost` folder to `/config/custom_components/`
3. Restart Home Assistant

### Step 2: Configure Integration (3 minutes)

1. **Add Integration:**
   - Go to Settings > Devices & Services
   - Click "+ Add Integration"
   - Search "Consumers Energy"
   - Click "Consumers Energy Cost Tracker"

2. **Select Power Sensors:**
   - Click the dropdown
   - Select all power sensors you want to track
   - Click "Submit"

3. **Choose Rate Plan:**
   - Toggle "Use Preset Rate Plan" = ON
   - Click "Submit"

4. **Select Your Rate Plan:**
   - Choose "Summer Time-of-Use (Rate 1001)" (most common)
   - Click "Submit"

✅ Done! Integration is now running.

### Step 3: Verify (1 minute)

1. Go to Developer Tools > States
2. Search for "consumers_energy"
3. Verify you see 12 sensors with valid data

## 5-Minute Dashboard Setup

### Basic Card (1 minute)

1. Go to your dashboard
2. Click Edit Dashboard
3. Click "+ Add Card"
4. Select "Entities"
5. Add these entities:
   - `sensor.consumers_energy_total_power`
   - `sensor.consumers_energy_current_rate`
   - `sensor.consumers_energy_cost_today`
6. Click "Save"

### Power Gauge (2 minutes)

1. Click "+ Add Card"
2. Select "Gauge"
3. Configure:
   - Entity: `sensor.consumers_energy_total_power`
   - Name: "Current Power"
   - Unit: W
   - Min: 0
   - Max: 5000 (adjust for your home)
4. Add segments:
   - 0-1500: Green
   - 1500-3000: Yellow
   - 3000-5000: Red
5. Click "Save"

### Cost Card (2 minutes)

1. Click "+ Add Card"
2. Select "Sensor"
3. Configure:
   - Entity: `sensor.consumers_energy_cost_today`
   - Graph: Line
4. Click "Save"

## What You Should See

### Real-time Sensors

```
Total Power: 1,234 W
Current Rate: 0.178 $/kWh
Cost Rate: 0.22 $/h
Rate Period: Summer Off-Peak
```

### Daily Tracking

```
Energy Today: 15.3 kWh
Cost Today: $2.73
```

### Rate Changes

- **Weekday 2pm:** Changes to "Summer On-Peak" ($0.23/kWh)
- **Weekday 7pm:** Changes back to "Summer Off-Peak" ($0.178/kWh)
- **Weekends:** Always "Summer Off-Peak"
- **Winter (Oct-May):** Always "Winter Standard" ($0.164/kWh)

## First 24 Hours

### Watch for These

1. **Rate Transitions** (if in summer):
   - Around 2pm on weekdays, rate should change to On-Peak
   - Around 7pm, should change back to Off-Peak
   - Check the Rate Period sensor

2. **Midnight Reset**:
   - At midnight, "Energy Today" and "Cost Today" reset to 0.0
   - This is expected behavior

3. **Accuracy Check**:
   - Compare "Cost Today" with your utility's online portal
   - Should be within 5% if rate plan is correct

## Quick Troubleshooting

### Sensors Show "Unknown"
- Wait 1-2 minutes for first update
- Check power sensors are reporting valid data
- Check Home Assistant logs: Settings > System > Logs

### Rate Seems Wrong
- Verify your rate plan on your utility bill
- Check Rate Period sensor shows correct period
- Most residential customers use "Summer Time-of-Use (Rate 1001)"

### Cost Seems Too High/Low
- Verify rate plan matches your utility account
- Check Total Power sensor matches your actual usage
- Compare Current Rate with expected rate for current time

## Next Steps

### After 24 Hours
1. Compare daily cost with utility bill estimate
2. Verify rate changes happened at correct times
3. Check midnight reset worked correctly

### Improve Your Dashboard
- See `examples/dashboard.yaml` for advanced cards
- Install ApexCharts card for graphs
- Add to Energy Dashboard

### Learn More
- `README.md` - Complete documentation
- `SETUP_GUIDE.md` - Detailed setup instructions
- `VERIFICATION_CHECKLIST.md` - Full testing procedures

## Rate Plan Quick Reference

### Summer Time-of-Use (Rate 1001) - Most Common
- **Summer (Jun-Sep):**
  - Weekdays 2-7pm: $0.23/kWh (On-Peak)
  - All other times: $0.178/kWh (Off-Peak)
- **Winter (Oct-May):** $0.164/kWh (flat rate)

### Smart Hours (Rate 1040)
- Peak weekdays 2-7pm year-round
- Requires manual rate entry (only differentials published)

### Nighttime Savers (Rate 1050)
- Three tiers: Super Off-Peak (overnight), Off-Peak (daytime), Peak (afternoon)
- Weekends all Super Off-Peak
- Best for night owls and EV owners

**Don't know your rate plan?**
- Check your Consumers Energy bill
- Call Consumers Energy: 1-800-477-5050
- Log into your account at ConsumersEnergy.com

## Getting Help

**Integration not working?**
1. Check Home Assistant logs first
2. Review `SETUP_GUIDE.md` troubleshooting section
3. Verify rate plan is correct
4. Report issues on GitHub

**Need different rate structure?**
- Use "Custom Rate Plan" option during setup
- Or reconfigure integration with different preset

---

**You're all set!** The integration is now tracking your energy costs in real-time. Check back in 24 hours to verify accuracy.
