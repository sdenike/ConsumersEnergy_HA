"""Data update coordinator for Consumers Energy Cost Tracker."""
from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import DOMAIN, UPDATE_INTERVAL_SECONDS
from .rate_calculator import RateCalculator

_LOGGER = logging.getLogger(__name__)


class EnergyDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator to manage energy data updates."""

    def __init__(
        self,
        hass: HomeAssistant,
        power_sensors: list[str],
        rate_config: dict,
    ) -> None:
        """Initialize the coordinator.

        Args:
            hass: Home Assistant instance
            power_sensors: List of power sensor entity IDs
            rate_config: Rate configuration dictionary
        """
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )
        self.power_sensors = power_sensors
        self.rate_calculator = RateCalculator(rate_config)

        # Previous state for energy calculation
        self._previous_power: float | None = None
        self._previous_timestamp: datetime | None = None

        # Period accumulators
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

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from power sensors and calculate costs.

        Returns:
            Dictionary with current state data
        """
        try:
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

            # Calculate current cost rate ($/hour)
            cost_rate = (total_power / 1000.0 * current_rate) if total_power else 0.0

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
