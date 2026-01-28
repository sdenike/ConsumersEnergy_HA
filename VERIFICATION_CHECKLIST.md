# Verification Checklist

Use this checklist to verify your Consumers Energy Cost Tracker installation is working correctly.

## Installation Verification

- [ ] Integration folder copied to `config/custom_components/consumers_energy_cost/`
- [ ] Home Assistant restarted successfully
- [ ] No errors in Home Assistant logs related to "consumers_energy"
- [ ] Integration appears in Settings > Devices & Services > Add Integration

## Configuration Verification

- [ ] Successfully completed sensor selection step
- [ ] Successfully selected or configured rate plan
- [ ] Integration entry created in Devices & Services
- [ ] All 12 sensors created and visible

## Sensor Data Verification

Check each sensor has valid data (not "Unknown" or "Unavailable"):

### Real-time Sensors
- [ ] `sensor.consumers_energy_total_power` shows current watts
- [ ] `sensor.consumers_energy_current_rate` shows rate (e.g., 0.178)
- [ ] `sensor.consumers_energy_cost_rate` shows $/hour value
- [ ] `sensor.consumers_energy_rate_period` shows period name (e.g., "Summer Off-Peak")

### Accumulator Sensors
- [ ] `sensor.consumers_energy_energy_today` shows kWh value (starts at 0.0)
- [ ] `sensor.consumers_energy_cost_today` shows dollar value (starts at 0.0)
- [ ] `sensor.consumers_energy_energy_week` shows kWh value
- [ ] `sensor.consumers_energy_cost_week` shows dollar value
- [ ] `sensor.consumers_energy_energy_month` shows kWh value
- [ ] `sensor.consumers_energy_cost_month` shows dollar value
- [ ] `sensor.consumers_energy_energy_year` shows kWh value
- [ ] `sensor.consumers_energy_cost_year` shows dollar value

## Rate Calculation Verification

### For Summer Time-of-Use (Rate 1001):

**If tested in Summer (June-September):**
- [ ] Before 2pm on weekday: Rate Period shows "Summer Off-Peak", rate is $0.178/kWh
- [ ] 2pm-7pm on weekday: Rate Period shows "Summer On-Peak", rate is $0.23/kWh
- [ ] After 7pm on weekday: Rate Period shows "Summer Off-Peak", rate is $0.178/kWh
- [ ] Weekend (any time): Rate Period shows "Summer Off-Peak", rate is $0.178/kWh

**If tested in Winter (October-May):**
- [ ] Any time, any day: Rate Period shows "Winter Standard", rate is $0.164/kWh

### Rate Transition Test
- [ ] Wait for rate transition time (e.g., 2pm or 7pm on weekday)
- [ ] Verify rate period sensor changes immediately
- [ ] Verify current rate sensor updates to new rate
- [ ] Verify cost rate sensor adjusts based on new rate

## Power Aggregation Verification

If you configured multiple power sensors:

1. Note individual sensor values:
   - Sensor 1: _____ W
   - Sensor 2: _____ W
   - Sensor 3: _____ W
   - (add more as needed)

2. Check total power sensor:
   - [ ] Total power equals sum of individual sensors (±5W tolerance)

## Period Accumulator Verification

### Daily Reset (Test at midnight):
- [ ] Before midnight: Note `energy_today` value: _____ kWh
- [ ] After midnight: Verify `energy_today` resets to 0.0
- [ ] After midnight: Verify `cost_today` resets to 0.0

### Weekly Reset (Test on Monday 00:00):
- [ ] Before Monday: Note `energy_week` value: _____ kWh
- [ ] After Monday 00:00: Verify `energy_week` resets to 0.0
- [ ] After Monday 00:00: Verify `cost_week` resets to 0.0

### Monthly Reset (Test on 1st of month):
- [ ] Before 1st: Note `energy_month` value: _____ kWh
- [ ] After 1st 00:00: Verify `energy_month` resets to 0.0
- [ ] After 1st 00:00: Verify `cost_month` resets to 0.0

## Energy Calculation Verification

Perform a manual calculation to verify accuracy:

1. Record power at start: _____ W at _____:_____ (time)
2. Wait exactly 1 hour
3. Record power at end: _____ W at _____:_____ (time)
4. Calculate expected energy:
   ```
   Average power = (start_power + end_power) / 2
   Energy (kWh) = average_power / 1000 * 1 hour = _____ kWh
   ```
5. Check sensor value:
   - [ ] `energy_today` increased by approximately expected energy (±5% tolerance)

## Cost Calculation Verification

Using the same 1-hour test:

1. Note current rate during test: _____ $/kWh
2. Calculate expected cost:
   ```
   Cost = energy_kWh * rate = _____ * _____ = $_____
   ```
3. Check sensor value:
   - [ ] `cost_today` increased by approximately expected cost (±5% tolerance)

## Dashboard Integration Verification

- [ ] Created basic entities card with sensors
- [ ] Card displays correctly on dashboard
- [ ] Values update every 30-60 seconds
- [ ] No "Unknown" or "Unavailable" states after 2 minutes

### Optional (if using ApexCharts):
- [ ] Installed ApexCharts card via HACS
- [ ] Created power/cost chart from examples
- [ ] Chart displays data correctly
- [ ] Chart updates in real-time

## Energy Dashboard Verification

- [ ] Go to Settings > Dashboards > Energy
- [ ] Add `sensor.consumers_energy_energy_today` as consumption source
- [ ] Wait 1-2 hours for data to accumulate
- [ ] Verify Energy Dashboard shows consumption graph
- [ ] Verify cost data appears alongside energy data

## Persistence Verification

- [ ] Note current sensor values before restart:
  - Total power: _____ W
  - Energy today: _____ kWh
  - Cost today: $_____
- [ ] Restart Home Assistant
- [ ] After restart, verify accumulators maintain values (not reset to 0)
- [ ] After restart, verify real-time sensors resume updating

## Error Handling Verification

### Test sensor unavailability:
- [ ] Disable one power sensor temporarily
- [ ] Verify integration continues working with remaining sensors
- [ ] Verify log shows warning about unavailable sensor (not error)
- [ ] Re-enable sensor and verify it's included again

### Test all sensors unavailable:
- [ ] Disable all power sensors temporarily
- [ ] Verify integration handles gracefully (no crashes)
- [ ] Verify appropriate log messages
- [ ] Re-enable sensors and verify recovery

## Performance Verification

- [ ] Check Home Assistant logs for errors related to integration
- [ ] Verify CPU usage is reasonable (<5% sustained)
- [ ] Verify database size doesn't grow excessively
- [ ] Verify 30-second update interval is maintained

## Accuracy Verification (24-Hour Test)

After 24 hours of operation:

1. **Compare with utility data** (if available):
   - Integration energy today: _____ kWh
   - Utility smart meter data: _____ kWh
   - Difference: _____ % (should be <5%)

2. **Compare with bill estimate**:
   - Integration cost today: $_____
   - Manual calculation from bill rates: $_____
   - Difference: _____ % (should be <1%)

3. **Verify rate transitions**:
   - [ ] Log shows appropriate rate changes at 2pm and 7pm (if applicable)
   - [ ] Cost accumulation pauses/resumes correctly
   - [ ] No duplicate rate transitions

## Configuration Update Verification

### Test sensor update via Options:
- [ ] Go to integration Configure option
- [ ] Add or remove a power sensor
- [ ] Verify integration reloads successfully
- [ ] Verify new sensor configuration is active
- [ ] Verify accumulators continue from previous values (not reset)

## Final Checklist

- [ ] All sensors updating regularly
- [ ] Rates change at correct times
- [ ] Accumulators increment correctly
- [ ] Dashboard displays properly
- [ ] Energy Dashboard integration works
- [ ] Restarts preserve data
- [ ] No errors in logs
- [ ] Accuracy within acceptable tolerance

## Notes

Use this space to document any issues or observations:

```
Issue:
Solution:

Issue:
Solution:

```

---

**Installation Date:** _____________

**Home Assistant Version:** _____________

**Integration Version:** 1.0.0

**Rate Plan Selected:** _____________

**Number of Power Sensors:** _____

**Verification Status:** ⬜ Pass / ⬜ Fail

**Verified By:** _____________
