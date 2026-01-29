"""Data update coordinator for Consumers Energy Cost Tracker."""
from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import DOMAIN, UPDATE_INTERVAL_SECONDS
from .rate_calculator import RateCalculator

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION = 1
STORAGE_KEY = "consumers_energy_cost_state"


class EnergyDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator to manage energy data updates."""

    def __init__(
        self,
        hass: HomeAssistant,
        power_sensors: list[str],
        rate_config: dict,
        entry_id: str,
    ) -> None:
        """Initialize the coordinator.

        Args:
            hass: Home Assistant instance
            power_sensors: List of power sensor entity IDs
            rate_config: Rate configuration dictionary
            entry_id: Config entry ID for unique storage
        """
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )
        self.power_sensors = power_sensors
        self.rate_calculator = RateCalculator(rate_config)
        self._entry_id = entry_id

        # Create persistent storage
        self._store = Store(
            hass,
            STORAGE_VERSION,
            f"{STORAGE_KEY}_{entry_id}",
        )

        # Previous state for energy calculation
        self._previous_power: float | None = None
        self._previous_timestamp: datetime | None = None

        # Period accumulators - will be initialized from storage or defaults
        self._daily_energy = 0.0
        self._daily_cost = 0.0
        self._daily_start = dt_util.start_of_local_day()

        self._weekly_energy = 0.0
        self._weekly_cost = 0.0
        self._weekly_start = self._get_week_start()

        self._monthly_energy = 0.0
        self._monthly_cost = 0.0
        self._monthly_start = dt_util.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )

        self._yearly_energy = 0.0
        self._yearly_cost = 0.0
        self._yearly_start = dt_util.now().replace(
            month=1, day=1, hour=0, minute=0, second=0, microsecond=0
        )

        # Hourly tracking (rolling 1-hour window)
        self._hourly_energy = 0.0
        self._hourly_cost = 0.0
        self._hourly_start = dt_util.now().replace(minute=0, second=0, microsecond=0)

        # Previous month tracking
        self._previous_month_energy = 0.0
        self._previous_month_cost = 0.0

        # State restoration flag
        self._state_restored = False

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from power sensors and calculate costs.

        Returns:
            Dictionary with current state data
        """
        try:
            # Restore state on first update
            if not self._state_restored:
                await self._restore_state()
                self._state_restored = True

            current_time = dt_util.now()

            # Get total power from all sensors
            total_power = await self._get_total_power()

            # Get current rate
            current_rate, period_name = self.rate_calculator.get_rate(current_time)
            season_name = self.rate_calculator.get_season_name(current_time)

            # Calculate energy delta using trapezoidal integration
            energy_delta = 0.0
            cost_delta = 0.0

            if (
                self._previous_power is not None
                and self._previous_timestamp is not None
                and total_power is not None
            ):
                time_hours = (
                    current_time - self._previous_timestamp
                ).total_seconds() / 3600.0

                # Trapezoidal integration: (P1 + P2) / 2 * dt
                energy_delta = (
                    (self._previous_power + total_power) / 2 * time_hours / 1000.0
                )

                # Calculate cost for this delta
                # Use the rate at the time of energy consumption
                cost_delta = energy_delta * current_rate

            # Update previous state
            if total_power is not None:
                self._previous_power = total_power
                self._previous_timestamp = current_time

            # Check for period boundaries and reset if needed
            self._check_period_boundaries(current_time)

            # Update accumulators
            self._daily_energy += energy_delta
            self._daily_cost += cost_delta

            self._weekly_energy += energy_delta
            self._weekly_cost += cost_delta

            self._monthly_energy += energy_delta
            self._monthly_cost += cost_delta

            self._yearly_energy += energy_delta
            self._yearly_cost += cost_delta

            self._hourly_energy += energy_delta
            self._hourly_cost += cost_delta

            # Calculate current cost rate ($/hour)
            cost_rate = (total_power / 1000.0 * current_rate) if total_power else 0.0

            # Save state for persistence across restarts
            await self._save_state()

            return {
                "total_power": total_power,
                "current_rate": current_rate,
                "cost_rate": cost_rate,
                "rate_period": f"{season_name} {period_name}",
                "energy_today": self._daily_energy,
                "cost_today": self._daily_cost,
                "energy_week": self._weekly_energy,
                "cost_week": self._weekly_cost,
                "energy_month": self._monthly_energy,
                "cost_month": self._monthly_cost,
                "energy_year": self._yearly_energy,
                "cost_year": self._yearly_cost,
                "energy_hour": self._hourly_energy,
                "cost_hour": self._hourly_cost,
                "energy_previous_month": self._previous_month_energy,
                "cost_previous_month": self._previous_month_cost,
                "last_update": current_time.isoformat(),
            }

        except Exception as err:
            _LOGGER.error("Error updating energy data: %s", err)
            raise UpdateFailed(f"Error updating energy data: {err}") from err

    async def _get_total_power(self) -> float | None:
        """Get total power from all configured sensors.

        Returns:
            Total power in watts, or None if all sensors unavailable
        """
        total = 0.0
        valid_sensors = 0

        for entity_id in self.power_sensors:
            state = self.hass.states.get(entity_id)

            if state is None:
                _LOGGER.debug("Power sensor %s not found (may still be loading)", entity_id)
                continue

            if state.state in ("unavailable", "unknown"):
                _LOGGER.debug("Power sensor %s is %s", entity_id, state.state)
                continue

            try:
                power = float(state.state)
                total += power
                valid_sensors += 1
            except (ValueError, TypeError) as err:
                _LOGGER.warning(
                    "Could not convert state of %s to float: %s", entity_id, err
                )
                continue

        if valid_sensors == 0:
            _LOGGER.debug("No valid power sensors available yet (may still be loading)")
            return None

        return total

    def _check_period_boundaries(self, current_time: datetime) -> None:
        """Check if any period boundaries have been crossed and reset accumulators.

        Args:
            current_time: Current datetime
        """
        # Check hourly boundary (rolling 1-hour window)
        hour_ago = current_time - timedelta(hours=1)
        if current_time.replace(minute=0, second=0, microsecond=0) > self._hourly_start.replace(minute=0, second=0, microsecond=0):
            _LOGGER.debug(
                "Hourly period reset - Energy: %.3f kWh, Cost: $%.2f",
                self._hourly_energy,
                self._hourly_cost,
            )
            self._hourly_energy = 0.0
            self._hourly_cost = 0.0
            self._hourly_start = current_time.replace(minute=0, second=0, microsecond=0)

        # Check daily boundary
        day_start = dt_util.start_of_local_day()
        if day_start > self._daily_start:
            _LOGGER.info(
                "Daily period reset - Energy: %.3f kWh, Cost: $%.2f",
                self._daily_energy,
                self._daily_cost,
            )
            self._daily_energy = 0.0
            self._daily_cost = 0.0
            self._daily_start = day_start

        # Check weekly boundary
        week_start = self._get_week_start()
        if week_start > self._weekly_start:
            _LOGGER.info(
                "Weekly period reset - Energy: %.3f kWh, Cost: $%.2f",
                self._weekly_energy,
                self._weekly_cost,
            )
            self._weekly_energy = 0.0
            self._weekly_cost = 0.0
            self._weekly_start = week_start

        # Check monthly boundary
        month_start = current_time.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        if month_start > self._monthly_start:
            _LOGGER.info(
                "Monthly period reset - Energy: %.3f kWh, Cost: $%.2f",
                self._monthly_energy,
                self._monthly_cost,
            )
            # Store previous month's data before resetting
            self._previous_month_energy = self._monthly_energy
            self._previous_month_cost = self._monthly_cost

            self._monthly_energy = 0.0
            self._monthly_cost = 0.0
            self._monthly_start = month_start

        # Check yearly boundary
        year_start = current_time.replace(
            month=1, day=1, hour=0, minute=0, second=0, microsecond=0
        )
        if year_start > self._yearly_start:
            _LOGGER.info(
                "Yearly period reset - Energy: %.3f kWh, Cost: $%.2f",
                self._yearly_energy,
                self._yearly_cost,
            )
            self._yearly_energy = 0.0
            self._yearly_cost = 0.0
            self._yearly_start = year_start

    def _get_week_start(self) -> datetime:
        """Get the start of the current week (Monday 00:00:00).

        Returns:
            Datetime of week start
        """
        now = dt_util.now()
        days_since_monday = now.weekday()
        week_start = now - timedelta(days=days_since_monday)
        return week_start.replace(hour=0, minute=0, second=0, microsecond=0)

    async def _save_state(self) -> None:
        """Save current accumulator state to persistent storage."""
        try:
            state_data = {
                "daily_energy": self._daily_energy,
                "daily_cost": self._daily_cost,
                "daily_start": self._daily_start.isoformat(),
                "weekly_energy": self._weekly_energy,
                "weekly_cost": self._weekly_cost,
                "weekly_start": self._weekly_start.isoformat(),
                "monthly_energy": self._monthly_energy,
                "monthly_cost": self._monthly_cost,
                "monthly_start": self._monthly_start.isoformat(),
                "yearly_energy": self._yearly_energy,
                "yearly_cost": self._yearly_cost,
                "yearly_start": self._yearly_start.isoformat(),
                "hourly_energy": self._hourly_energy,
                "hourly_cost": self._hourly_cost,
                "hourly_start": self._hourly_start.isoformat(),
                "previous_month_energy": self._previous_month_energy,
                "previous_month_cost": self._previous_month_cost,
                "previous_power": self._previous_power,
                "previous_timestamp": self._previous_timestamp.isoformat() if self._previous_timestamp else None,
            }
            await self._store.async_save(state_data)
        except Exception as err:
            _LOGGER.error("Error saving state: %s", err)

    async def _restore_state(self) -> None:
        """Restore accumulator state from persistent storage."""
        try:
            state_data = await self._store.async_load()

            if state_data is None:
                _LOGGER.info("No saved state found, starting fresh")
                return

            current_time = dt_util.now()

            # Restore daily state if still valid
            daily_start = dt_util.parse_datetime(state_data.get("daily_start", ""))
            if daily_start and dt_util.start_of_local_day() == daily_start.replace(tzinfo=dt_util.DEFAULT_TIME_ZONE):
                self._daily_energy = state_data.get("daily_energy", 0.0)
                self._daily_cost = state_data.get("daily_cost", 0.0)
                self._daily_start = daily_start
                _LOGGER.info("Restored daily state: %.3f kWh, $%.2f", self._daily_energy, self._daily_cost)
            else:
                _LOGGER.info("Daily period expired, starting fresh")

            # Restore weekly state if still valid
            weekly_start = dt_util.parse_datetime(state_data.get("weekly_start", ""))
            if weekly_start and self._get_week_start() == weekly_start.replace(tzinfo=dt_util.DEFAULT_TIME_ZONE):
                self._weekly_energy = state_data.get("weekly_energy", 0.0)
                self._weekly_cost = state_data.get("weekly_cost", 0.0)
                self._weekly_start = weekly_start
                _LOGGER.info("Restored weekly state: %.3f kWh, $%.2f", self._weekly_energy, self._weekly_cost)
            else:
                _LOGGER.info("Weekly period expired, starting fresh")

            # Restore monthly state if still valid
            monthly_start = dt_util.parse_datetime(state_data.get("monthly_start", ""))
            current_month_start = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if monthly_start and current_month_start == monthly_start.replace(tzinfo=dt_util.DEFAULT_TIME_ZONE):
                self._monthly_energy = state_data.get("monthly_energy", 0.0)
                self._monthly_cost = state_data.get("monthly_cost", 0.0)
                self._monthly_start = monthly_start
                _LOGGER.info("Restored monthly state: %.3f kWh, $%.2f", self._monthly_energy, self._monthly_cost)
            else:
                _LOGGER.info("Monthly period expired, starting fresh")

            # Restore yearly state if still valid
            yearly_start = dt_util.parse_datetime(state_data.get("yearly_start", ""))
            current_year_start = current_time.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            if yearly_start and current_year_start == yearly_start.replace(tzinfo=dt_util.DEFAULT_TIME_ZONE):
                self._yearly_energy = state_data.get("yearly_energy", 0.0)
                self._yearly_cost = state_data.get("yearly_cost", 0.0)
                self._yearly_start = yearly_start
                _LOGGER.info("Restored yearly state: %.3f kWh, $%.2f", self._yearly_energy, self._yearly_cost)
            else:
                _LOGGER.info("Yearly period expired, starting fresh")

            # Restore hourly state if still valid
            hourly_start = dt_util.parse_datetime(state_data.get("hourly_start", ""))
            current_hour_start = current_time.replace(minute=0, second=0, microsecond=0)
            if hourly_start and current_hour_start == hourly_start.replace(tzinfo=dt_util.DEFAULT_TIME_ZONE):
                self._hourly_energy = state_data.get("hourly_energy", 0.0)
                self._hourly_cost = state_data.get("hourly_cost", 0.0)
                self._hourly_start = hourly_start
                _LOGGER.debug("Restored hourly state: %.3f kWh, $%.2f", self._hourly_energy, self._hourly_cost)
            else:
                _LOGGER.debug("Hourly period expired, starting fresh")

            # Always restore previous month
            self._previous_month_energy = state_data.get("previous_month_energy", 0.0)
            self._previous_month_cost = state_data.get("previous_month_cost", 0.0)
            if self._previous_month_energy > 0 or self._previous_month_cost > 0:
                _LOGGER.info("Restored previous month: %.3f kWh, $%.2f", self._previous_month_energy, self._previous_month_cost)

            # Restore previous power reading for energy calculation
            self._previous_power = state_data.get("previous_power")
            previous_timestamp_str = state_data.get("previous_timestamp")
            if previous_timestamp_str:
                self._previous_timestamp = dt_util.parse_datetime(previous_timestamp_str)

        except Exception as err:
            _LOGGER.error("Error restoring state: %s", err)
