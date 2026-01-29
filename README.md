# Consumers Energy Cost Tracker

A custom Home Assistant integration to track real-time energy costs with time-of-use and seasonal pricing support for Consumers Energy customers (and others with similar rate structures).

## Features

- **Sensor Aggregation**: Combine multiple power sensors (watts) into total power monitoring
- **Energy Calculation**: Accurate kWh calculation using trapezoidal integration
- **Time-of-Use Pricing**: Automatic rate switching based on time of day
- **Seasonal Pricing**: Different rates for summer (Jun-Sep) and winter (Oct-May) periods
- **Real-time Cost Tracking**: See your current cost per hour
- **Period Accumulators**: Track energy and costs for today, this week, this month, and this year
- **Preset Rate Plans**: Three Consumers Energy rate plan templates included
- **Custom Rate Configuration**: Configure your own rate structure
- **Energy Dashboard Integration**: Full compatibility with Home Assistant's Energy Dashboard

## Preset Rate Plans

### 1. Summer Time-of-Use (Rate 1001)
- **Summer (June-September)**:
  - On-Peak: $0.23/kWh (weekdays 2-7pm)
  - Off-Peak: $0.178/kWh (all other times)
- **Winter (October-May)**: Flat rate $0.164/kWh

### 2. Smart Hours (Rate 1040)
- Peak pricing weekdays 2-7pm year-round
- Off-peak all other times
- Requires manual rate entry (only differentials published by Consumers Energy)

### 3. Nighttime Savers (Rate 1050)
- **Summer**:
  - Super Off-Peak: $0.133/kWh (12am-6am, 11pm-12am)
  - Off-Peak: $0.173/kWh (6am-2pm, 7pm-11pm)
  - On-Peak: $0.212/kWh (2pm-7pm)
- **Winter**:
  - Super Off-Peak: $0.141/kWh (12am-6am, 11pm-12am)
  - Off-Peak: $0.168/kWh (6am-2pm, 7pm-11pm)
  - On-Peak: $0.169/kWh (2pm-7pm)
- **Weekends**: All super off-peak pricing

## Installation

### Manual Installation

1. Copy the `custom_components/consumers_energy_cost` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant
3. Go to Settings > Devices & Services > Add Integration
4. Search for "Consumers Energy Cost Tracker"

### HACS Installation (Recommended when published)

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click the three dots menu and select "Custom repositories"
4. Add this repository URL with category "Integration"
5. Click "Install" on the Consumers Energy Cost Tracker card
6. Restart Home Assistant

## Configuration

### Step 1: Select Power Sensors

1. Go to Settings > Devices & Services > Add Integration
2. Search for "Consumers Energy Cost Tracker"
3. Select all power sensors you want to monitor
   - These should be sensors with `device_class: power` and units in watts (W)
   - Examples: Smart plugs, individual circuit monitors, whole-home energy monitors

### Step 2: Choose Rate Plan

Choose whether to use a preset rate plan or configure custom rates.

#### Option A: Preset Rate Plan
Select your Consumers Energy rate plan from the dropdown:
- Summer Time-of-Use (Rate 1001) - Most common residential plan
- Smart Hours (Rate 1040) - Advanced TOU plan
- Nighttime Savers (Rate 1050) - Three-tier overnight discount plan

#### Option B: Custom Rate Plan
Enter your own rates:
- Summer Peak Rate (Jun-Sep, weekdays 2-7pm)
- Summer Off-Peak Rate (all other summer times)
- Winter Rate (Oct-May, flat rate)

### Step 3: Complete Setup

The integration will create 12 sensors:

**Power & Rate Sensors:**
- `sensor.consumers_energy_total_power` - Current total power (W)
- `sensor.consumers_energy_current_rate` - Current electricity rate ($/kWh)
- `sensor.consumers_energy_cost_rate` - Current cost rate ($/hour)
- `sensor.consumers_energy_rate_period` - Current rate period (e.g., "Summer On-Peak")

**Daily Tracking:**
- `sensor.consumers_energy_energy_today` - Energy consumed today (kWh)
- `sensor.consumers_energy_cost_today` - Cost today ($)

**Weekly Tracking:**
- `sensor.consumers_energy_energy_week` - Energy this week (kWh)
- `sensor.consumers_energy_cost_week` - Cost this week ($)

**Monthly Tracking:**
- `sensor.consumers_energy_energy_month` - Energy this month (kWh)
- `sensor.consumers_energy_cost_month` - Cost this month ($)

**Yearly Tracking:**
- `sensor.consumers_energy_energy_year` - Energy this year (kWh)
- `sensor.consumers_energy_cost_year` - Cost this year ($)

## Dashboard Examples

### Basic Power and Cost Card

```yaml
type: entities
title: Energy Cost Tracker
entities:
  - entity: sensor.consumers_energy_total_power
    name: Current Power
  - entity: sensor.consumers_energy_current_rate
    name: Current Rate
  - entity: sensor.consumers_energy_cost_rate
    name: Cost Per Hour
  - entity: sensor.consumers_energy_rate_period
    name: Rate Period
  - type: divider
  - entity: sensor.consumers_energy_cost_today
    name: Cost Today
  - entity: sensor.consumers_energy_cost_week
    name: Cost This Week
  - entity: sensor.consumers_energy_cost_month
    name: Cost This Month
```

### ApexCharts Example - Power & Cost Over Time

Install the [ApexCharts card](https://github.com/RomRider/apexcharts-card) via HACS, then add:

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Power Usage & Cost Today
  show_states: true
graph_span: 24h
span:
  start: day
series:
  - entity: sensor.consumers_energy_total_power
    name: Power
    stroke_width: 2
    type: line
    yaxis_id: power
    color: '#2196F3'
  - entity: sensor.consumers_energy_cost_today
    name: Cost Today
    stroke_width: 2
    type: line
    yaxis_id: cost
    color: '#4CAF50'
yaxis:
  - id: power
    opposite: false
    decimals: 0
    apex_config:
      title:
        text: Power (W)
  - id: cost
    opposite: true
    decimals: 2
    apex_config:
      title:
        text: Cost ($)
```

### ApexCharts Example - Rate Period Visualization

```yaml
type: custom:apexcharts-card
header:
  show: true
  title: Electricity Rate Periods
graph_span: 24h
span:
  start: day
series:
  - entity: sensor.consumers_energy_current_rate
    name: Rate
    stroke_width: 3
    type: line
    color: '#FF9800'
yaxis:
  - decimals: 3
    apex_config:
      title:
        text: Rate ($/kWh)
```

### Gauge Card - Current Power

```yaml
type: gauge
entity: sensor.consumers_energy_total_power
name: Current Power Usage
unit: W
min: 0
max: 5000
needle: true
segments:
  - from: 0
    color: '#4CAF50'
  - from: 1500
    color: '#FF9800'
  - from: 3000
    color: '#F44336'
```

### Statistics Card - Monthly Comparison

```yaml
type: statistic
entity: sensor.consumers_energy_cost_month
period:
  calendar:
    period: month
stat_type: change
name: Monthly Cost Trend
```

## Energy Dashboard Integration

The integration automatically integrates with Home Assistant's Energy Dashboard:

1. Go to Settings > Dashboards > Energy
2. Click "Add Consumption"
3. Select `sensor.consumers_energy_energy_today` or any of the energy sensors
4. The cost sensors will automatically be associated with their energy counterparts

## Technical Details

### Energy Calculation Method

The integration uses **trapezoidal integration** for accurate energy calculation:

```
energy_kwh = ((previous_power_w + current_power_w) / 2) * time_hours / 1000
```

This method accounts for power variations between readings, providing higher accuracy than assuming constant power.

### Update Frequency

Sensors update every 30 seconds by default. This provides:
- Real-time responsiveness in the UI
- Accurate cost tracking during rate transitions
- Smooth graphs and visualizations

### Period Reset Logic

Accumulators automatically reset at period boundaries:
- **Daily**: Midnight local time
- **Weekly**: Monday 00:00:00 local time
- **Monthly**: 1st of month 00:00:00 local time
- **Yearly**: January 1st 00:00:00 local time

### Data Persistence

- Short-term data stored in coordinator state (survives updates)
- Long-term data stored in Home Assistant database (survives restarts)
- Period accumulators reset at boundaries but maintain running totals

## Troubleshooting

### Sensors show "Unknown" or "Unavailable"

1. Check that your power sensors are reporting valid numeric values
2. Verify sensor entity IDs are correct in integration config
3. Check Home Assistant logs for errors: Settings > System > Logs

### Cost calculations seem incorrect

1. Verify your rate plan is correct for your utility account
2. Check that rate period changes at expected times (use Rate Period sensor)
3. Compare daily totals with your utility's online usage data
4. Ensure power sensors are measuring the circuits you expect

### Period totals don't match expectations

1. Period accumulators only track data while Home Assistant is running
2. If HA was offline, energy during that time won't be counted
3. Consider using the Energy Dashboard for long-term statistics (doesn't reset)

### Energy Dashboard not showing data

1. Ensure energy sensors have correct `device_class: energy` and `state_class: total`
2. Wait a few hours for data to accumulate
3. Check that sensors are actually updating (watch for state changes)

## Advanced Configuration

### Modifying Rate Plans

To update rates without losing historical data:

1. Go to Settings > Devices & Services
2. Find "Consumers Energy Cost Tracker"
3. Click "Configure"
4. Update power sensors (this won't affect rate configuration)

To change rate plans:
1. Remove the integration
2. Re-add with new rate configuration
3. Historical data will be lost, but new tracking begins immediately

### Multiple Rate Configurations

You can install the integration multiple times to track different rate scenarios:
1. Use different power sensor sets for each instance
2. Compare costs across different rate plans
3. Track specific circuits separately from whole-home

## Support

For issues, feature requests, or questions:
- GitHub Issues: [Report a bug or request a feature](https://github.com/sdenike/ConsumersEnergy_HA/issues)
<!-- - Home Assistant Community: [Post in the forums] -->

## Credits

Developed for Consumers Energy customers and Home Assistant enthusiasts who want accurate, real-time energy cost tracking.

## License

This integration is provided as-is for personal use. Consumers Energy rate data is sourced from public rate schedules and may change. Always verify rates with your utility.

---

**Disclaimer**: This is an unofficial integration and is not affiliated with or endorsed by Consumers Energy. Rate information is provided for convenience and may not reflect current rates. Always verify costs with your utility bill.
