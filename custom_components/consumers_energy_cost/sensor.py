"""Sensor platform for Consumers Energy Cost Tracker."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_INSTANCE_NAME,
    DOMAIN,
    SENSOR_COST_MONTH,
    SENSOR_COST_RATE,
    SENSOR_COST_TODAY,
    SENSOR_COST_WEEK,
    SENSOR_COST_YEAR,
    SENSOR_CURRENT_RATE,
    SENSOR_ENERGY_MONTH,
    SENSOR_ENERGY_TODAY,
    SENSOR_ENERGY_WEEK,
    SENSOR_ENERGY_YEAR,
    SENSOR_RATE_PERIOD,
    SENSOR_TOTAL_POWER,
)
from .coordinator import EnergyDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Consumers Energy Cost sensors from a config entry."""
    coordinator: EnergyDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = [
        TotalPowerSensor(coordinator, config_entry),
        CurrentRateSensor(coordinator, config_entry),
        CostRateSensor(coordinator, config_entry),
        RatePeriodSensor(coordinator, config_entry),
        EnergyTodaySensor(coordinator, config_entry),
        CostTodaySensor(coordinator, config_entry),
        EnergyWeekSensor(coordinator, config_entry),
        CostWeekSensor(coordinator, config_entry),
        EnergyMonthSensor(coordinator, config_entry),
        CostMonthSensor(coordinator, config_entry),
        EnergyYearSensor(coordinator, config_entry),
        CostYearSensor(coordinator, config_entry),
    ]

    async_add_entities(entities)


class ConsumersEnergySensorBase(CoordinatorEntity, SensorEntity):
    """Base class for Consumers Energy Cost sensors."""

    def __init__(
        self,
        coordinator: EnergyDataUpdateCoordinator,
        config_entry: ConfigEntry,
        sensor_type: str,
        name: str,
    ) -> None:
        """Initialize the sensor.

        Args:
            coordinator: Data update coordinator
            config_entry: Config entry
            sensor_type: Sensor type identifier
            name: Sensor name
        """
        super().__init__(coordinator)
        instance_name = config_entry.data.get(CONF_INSTANCE_NAME, "Consumers Energy")
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_type}"
        self._attr_name = f"{instance_name} {name}"
        self._attr_has_entity_name = False

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            "source_sensors": self.coordinator.power_sensors,
            "last_update": self.coordinator.data.get("last_update"),
        }


class TotalPowerSensor(ConsumersEnergySensorBase):
    """Sensor for total power consumption."""

    def __init__(
        self, coordinator: EnergyDataUpdateCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, SENSOR_TOTAL_POWER, "Total Power")
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("total_power")


class CurrentRateSensor(ConsumersEnergySensorBase):
    """Sensor for current electricity rate."""

    def __init__(
        self, coordinator: EnergyDataUpdateCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator, config_entry, SENSOR_CURRENT_RATE, "Current Rate"
        )
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "$/kWh"
        self._attr_icon = "mdi:currency-usd"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("current_rate")


class CostRateSensor(ConsumersEnergySensorBase):
    """Sensor for current cost rate ($/hour)."""

    def __init__(
        self, coordinator: EnergyDataUpdateCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, SENSOR_COST_RATE, "Cost Rate")
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "$/h"
        self._attr_icon = "mdi:currency-usd"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("cost_rate")


class RatePeriodSensor(ConsumersEnergySensorBase):
    """Sensor for current rate period name."""

    def __init__(
        self, coordinator: EnergyDataUpdateCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator, config_entry, SENSOR_RATE_PERIOD, "Rate Period"
        )
        self._attr_icon = "mdi:clock-outline"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("rate_period")


class EnergyTodaySensor(ConsumersEnergySensorBase):
    """Sensor for energy consumed today."""

    def __init__(
        self, coordinator: EnergyDataUpdateCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, SENSOR_ENERGY_TODAY, "Energy Today")
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("energy_today")


class CostTodaySensor(ConsumersEnergySensorBase):
    """Sensor for cost today."""

    def __init__(
        self, coordinator: EnergyDataUpdateCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, SENSOR_COST_TODAY, "Cost Today")
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "USD"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("cost_today")


class EnergyWeekSensor(ConsumersEnergySensorBase):
    """Sensor for energy consumed this week."""

    def __init__(
        self, coordinator: EnergyDataUpdateCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, SENSOR_ENERGY_WEEK, "Energy Week")
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("energy_week")


class CostWeekSensor(ConsumersEnergySensorBase):
    """Sensor for cost this week."""

    def __init__(
        self, coordinator: EnergyDataUpdateCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, SENSOR_COST_WEEK, "Cost Week")
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "USD"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("cost_week")


class EnergyMonthSensor(ConsumersEnergySensorBase):
    """Sensor for energy consumed this month."""

    def __init__(
        self, coordinator: EnergyDataUpdateCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, SENSOR_ENERGY_MONTH, "Energy Month")
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("energy_month")


class CostMonthSensor(ConsumersEnergySensorBase):
    """Sensor for cost this month."""

    def __init__(
        self, coordinator: EnergyDataUpdateCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, SENSOR_COST_MONTH, "Cost Month")
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "USD"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("cost_month")


class EnergyYearSensor(ConsumersEnergySensorBase):
    """Sensor for energy consumed this year."""

    def __init__(
        self, coordinator: EnergyDataUpdateCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, SENSOR_ENERGY_YEAR, "Energy Year")
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("energy_year")


class CostYearSensor(ConsumersEnergySensorBase):
    """Sensor for cost this year."""

    def __init__(
        self, coordinator: EnergyDataUpdateCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, SENSOR_COST_YEAR, "Cost Year")
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = "USD"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("cost_year")
