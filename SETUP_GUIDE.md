# Setup Guide - Consumers Energy Cost Tracker

This guide walks you through setting up the Consumers Energy Cost Tracker integration from scratch.

## Prerequisites

- Home Assistant 2024.1.0 or newer
- At least one power sensor (watts) already configured in Home Assistant
  - Examples: Shelly Plug, TP-Link Kasa, Aqara Smart Plug, Emporia Vue, Sense Energy Monitor
- Your Consumers Energy rate plan information (or use the presets)

## Installation Methods

### Method 1: Manual Installation

1. **Download the integration**
   - Clone or download this repository
   - Copy the entire `custom_components/consumers_energy_cost` folder

2. **Install to Home Assistant**
   ```bash
   # Navigate to your Home Assistant config directory
   cd /path/to/homeassistant/config

   # Create custom_components if it doesn't exist
   mkdir -p custom_components

   # Copy the integration
   cp -r /path/to/download/custom_components/consumers_energy_cost custom_components/
   ```

3. **Restart Home Assistant**
   - Go to Developer Tools > YAML > Restart
   - Or restart via command line: `ha core restart`

4. **Verify installation**
   - Check logs for any errors: Settings > System > Logs
   - Search for "consumers_energy" in the logs

### Method 2: HACS Installation (Future)

Once published to HACS:

1. Open HACS in Home Assistant
2. Click Integrations
3. Click the + button
4. Search for "Consumers Energy Cost Tracker"
5. Click Install
6. Restart Home Assistant

## Configuration Steps

### Step 1: Find Your Power Sensors

Before configuring, identify which power sensors you want to track:

1. Go to Developer Tools > States
2. Filter by "power" in the entity search
3. Look for entities with:
   - `device_class: power`
   - Units in watts (W)
   - State showing numeric values

Example power sensor entity IDs:
- `sensor.living_room_plug_power`
- `sensor.ac_unit_power`
- `sensor.whole_home_power`
- `sensor.office_outlets_power`

Write down the entity IDs you want to track.

### Step 2: Add the Integration

1. Go to Settings > Devices & Services
2. Click "+ Add Integration" (bottom right)
3. Search for "Consumers Energy"
4. Click "Consumers Energy Cost Tracker"

### Step 3: Select Power Sensors

1. A dialog will appear showing "Select Power Sensors"
2. Click the dropdown and select all power sensors you want to monitor
   - You can select 1 to many sensors
   - All selected sensors will be summed together
3. Click "Submit"

**Tip**: Start with just 1-2 sensors to test, then add more later via Options.

### Step 4: Choose Rate Plan Type

1. You'll see "Rate Plan Type" dialog
2. Toggle "Use Preset Rate Plan":
   - **ON**: Use one of the 3 Consumers Energy presets
   - **OFF**: Configure custom rates
3. Click "Submit"

### Step 5A: Select Preset Rate Plan

If you chose preset:

1. Select your rate plan from the dropdown:
   - **Summer Time-of-Use (Rate 1001)**: Most common residential plan
   - **Smart Hours (Rate 1040)**: Advanced TOU (requires rate updates)
   - **Nighttime Savers (Rate 1050)**: Three-tier overnight discount

2. Click "Submit"

**How to find your rate plan**:
- Check your Consumers Energy bill (usually noted near usage details)
- Log into your Consumers Energy account online
- Call Consumers Energy: 1-800-477-5050

### Step 5B: Configure Custom Rates

If you chose custom:

1. Enter your rates:
   - **Summer Peak Rate**: Rate during peak hours (Jun-Sep, weekdays 2-7pm)
   - **Summer Off-Peak Rate**: Rate during off-peak times in summer
   - **Winter Rate**: Flat rate for Oct-May
2. Click "Submit"

### Step 6: Verify Installation

1. Go to Settings > Devices & Services
2. You should see "Consumers Energy Cost Tracker" in the list
3. Click on it to see all 12 sensors created

## Testing Your Setup

### Verify Sensor Data

1. Go to Developer Tools > States
2. Search for "consumers_energy"
3. Check that sensors show valid data:

```
sensor.consumers_energy_total_power: 1234.5 W
sensor.consumers_energy_current_rate: 0.178 $/kWh
sensor.consumers_energy_rate_period: Summer Off-Peak
sensor.consumers_energy_energy_today: 5.2 kWh
sensor.consumers_energy_cost_today: 0.93 USD
```

### Test Rate Changes

If using Summer Time-of-Use:

1. Check the Rate Period sensor before 2pm
   - Should show "Summer Off-Peak" (summer) or "Standard" (winter)
2. Check again after 2pm on a weekday in summer
   - Should show "Summer On-Peak"
3. Check again after 7pm
   - Should show "Summer Off-Peak"

### Verify Power Aggregation

If you selected multiple power sensors:

1. Note the individual power sensor values
2. Check `sensor.consumers_energy_total_power`
3. It should equal the sum of all selected sensors

Example:
```
sensor.ac_power: 1500 W
sensor.heater_power: 800 W
sensor.consumers_energy_total_power: 2300 W ✓
```

## Adding to Dashboard

### Quick Test Card

1. Go to your dashboard
2. Click Edit Dashboard (top right)
3. Click "+ Add Card"
4. Choose "Entities" card
5. Add these entities:
   - `sensor.consumers_energy_total_power`
   - `sensor.consumers_energy_current_rate`
   - `sensor.consumers_energy_cost_today`
6. Click "Save"

### Full Dashboard

See `examples/dashboard.yaml` for complete dashboard configurations including:
- Power gauges
- ApexCharts graphs
- Period summaries
- Rate visualizations

## Energy Dashboard Integration

### Enable Energy Dashboard

1. Go to Settings > Dashboards > Energy
2. Click "Add Consumption"
3. Select `sensor.consumers_energy_energy_today`
4. Configure:
   - **Name**: "Monitored Circuits" (or similar)
   - **Entity**: `sensor.consumers_energy_energy_today`
5. Click "Save"

The cost sensor will automatically be linked.

### View Energy Data

1. Go to Settings > Dashboards > Energy
2. Select time period (Day, Week, Month, Year)
3. View energy consumption and costs

**Note**: Energy Dashboard requires a few hours of data before showing graphs.

## Updating Configuration

### Update Power Sensors

To add/remove power sensors without losing data:

1. Go to Settings > Devices & Services
2. Find "Consumers Energy Cost Tracker"
3. Click "Configure"
4. Update the sensor selection
5. Click "Submit"

The integration will reload with the new sensors.

### Change Rate Plan

To change rate plans:

**Warning**: This will reset all period accumulators (today, week, month, year).

1. Go to Settings > Devices & Services
2. Find "Consumers Energy Cost Tracker"
3. Click the three dots menu > "Delete"
4. Confirm deletion
5. Follow the setup steps again with the new rate plan

## Troubleshooting

### Issue: Sensors show "Unavailable"

**Cause**: Power sensors are not reporting data or integration cannot find them.

**Solution**:
1. Check that power sensors are online and reporting
2. Go to Developer Tools > States and verify sensor entity IDs
3. Check Home Assistant logs for errors
4. Reconfigure integration with correct entity IDs

### Issue: Costs seem too high/low

**Cause**: Wrong rate plan or incorrect rates.

**Solution**:
1. Verify your rate plan on your utility bill
2. Check that the Rate Period sensor shows correct periods
3. Compare `current_rate` sensor with your expected rate at that time
4. Reconfigure if needed

### Issue: Energy Dashboard not showing data

**Cause**: Not enough data accumulated yet.

**Solution**:
1. Wait at least 1-2 hours for data to accumulate
2. Verify energy sensors are incrementing: Watch `sensor.consumers_energy_energy_today`
3. Check that sensor has correct `device_class: energy` and `state_class: total`
4. Restart Home Assistant if needed

### Issue: Rate doesn't change at 2pm/7pm

**Cause**: Rate plan configuration or timezone issue.

**Solution**:
1. Verify Home Assistant timezone: Settings > System > General
2. Check Rate Period sensor at 1:59pm and 2:01pm
3. Check logs for rate calculation errors
4. Verify rate plan has correct peak hours (14:00-19:00)

### Issue: Daily total resets mid-day

**Cause**: Timezone misconfiguration or Home Assistant restart.

**Solution**:
1. Verify timezone settings match your local time
2. Check that "midnight" in HA matches your local midnight
3. Daily reset is expected at midnight (not a bug)

## Advanced Configuration

### Tracking Specific Circuits

You can create multiple instances to track different areas:

**Example 1: HVAC only**
- Select only HVAC-related power sensors
- Name: "HVAC Energy Cost"

**Example 2: Entertainment Center**
- Select TV, gaming console, stereo power sensors
- Name: "Entertainment Cost"

This lets you see cost breakdowns by area.

### Custom Rate Schedules

For complex rate schedules not covered by presets:

1. Choose "Custom Rate Plan"
2. Enter base rates
3. After setup, the rate configuration is stored in `config/.storage/core.config_entries`
4. Advanced users can manually edit the rate_config JSON structure

### Automations Based on Cost

Create automations using cost sensors:

```yaml
automation:
  - alias: "Alert when daily cost exceeds budget"
    trigger:
      - platform: numeric_state
        entity_id: sensor.consumers_energy_cost_today
        above: 5.00
    action:
      - service: notify.mobile_app
        data:
          message: "Daily energy cost exceeded $5.00"
```

```yaml
automation:
  - alias: "Notify when entering peak rate period"
    trigger:
      - platform: state
        entity_id: sensor.consumers_energy_rate_period
        to: "Summer On-Peak"
    action:
      - service: notify.mobile_app
        data:
          message: "Peak rate period started - reduce usage to save money"
```

## Getting Help

If you encounter issues not covered here:

1. Check the logs: Settings > System > Logs
2. Search for existing issues on GitHub
3. Create a new issue with:
   - Home Assistant version
   - Integration version
   - Log excerpts
   - Steps to reproduce

## Next Steps

After successful setup:

1. Monitor for 24 hours to verify accuracy
2. Compare daily cost with previous utility bill data
3. Set up dashboard visualizations
4. Create automations to reduce peak usage
5. Integrate with Energy Dashboard for long-term tracking

Enjoy real-time energy cost tracking!
