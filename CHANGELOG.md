# Changelog

All notable changes to the Consumers Energy Cost Tracker integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-28

### Added
- Initial release of Consumers Energy Cost Tracker integration
- Support for multiple power sensor aggregation
- Trapezoidal integration for accurate energy (kWh) calculation
- Real-time cost calculation with 30-second update interval
- Time-of-use and seasonal pricing support
- Three preset Consumers Energy rate plans:
  - Summer Time-of-Use (Rate 1001)
  - Smart Hours (Rate 1040)
  - Nighttime Savers (Rate 1050)
- Custom rate plan configuration
- Period accumulators for daily, weekly, monthly, and yearly tracking
- 12 sensor entities:
  - Total power (W)
  - Current rate ($/kWh)
  - Cost rate ($/hour)
  - Rate period name
  - Energy and cost for today, week, month, year
- Config flow with multi-step UI setup
- Options flow for updating power sensors
- Weekday/weekend rate differentiation
- Automatic period boundary resets (midnight, week start, month start, year start)
- Energy Dashboard integration with proper device_class and state_class
- Comprehensive documentation and setup guide
- Example dashboard configurations using ApexCharts
- Unit tests for rate calculator
- HACS compatibility

### Technical Details
- Uses DataUpdateCoordinator pattern for efficient polling
- Implements RateCalculator for season and TOU logic
- Power sensor unavailability handling
- Timezone-aware period resets
- Source sensor tracking in extra state attributes

### Documentation
- Complete README with installation and configuration instructions
- Detailed SETUP_GUIDE with troubleshooting
- Example dashboard configurations (entities, ApexCharts, gauges)
- Rate plan comparison table
- Testing and verification procedures

## [Unreleased]

### Planned Features
- Statistics system integration for long-term data storage
- Custom Lovelace card (TypeScript/LitElement)
- Advanced rate schedule configuration (more than 3 time periods)
- Holiday rate support
- Utility bill comparison report
- CSV export functionality
- Automation helpers (peak rate notifications)
- Multi-currency support
- Rate plan import/export
- Integration with other utility providers

### Known Issues
- Statistics manager not yet implemented (planned for v1.1.0)
- Custom rate configuration is simplified (limited to 3 basic fields)
- Options flow only allows sensor updates, not rate plan changes
- No validation of rate plan accuracy against utility rates

### Future Enhancements
- Add more Consumers Energy rate plans as they become available
- Support for demand charges ($/kW)
- Real-time utility bill estimation
- Cost projections and trend analysis
- Integration with solar/battery systems
- Smart device scheduling based on rate periods
