"""Config flow for Consumers Energy Cost Tracker integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector

from .const import (
    CONF_POWER_SENSORS,
    CONF_RATE_CONFIG,
    CONF_RATE_PLAN,
    CONF_USE_PRESET,
    DOMAIN,
    RATE_PLAN_CUSTOM,
    RATE_PLAN_NIGHTTIME_SAVERS,
    RATE_PLAN_SMART_HOURS,
    RATE_PLAN_SUMMER_TOU,
    RATE_PLAN_TEMPLATES,
)

_LOGGER = logging.getLogger(__name__)


class ConsumersEnergyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Consumers Energy Cost Tracker."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._power_sensors: list[str] = []
        self._rate_plan: str | None = None
        self._rate_config: dict | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial step - sensor selection."""
        errors: dict[str, str] = {}

        if user_input is not None:
            power_sensors = user_input.get(CONF_POWER_SENSORS, [])

            if not power_sensors:
                errors[CONF_POWER_SENSORS] = "no_sensors"
            else:
                self._power_sensors = power_sensors
                return await self.async_step_rate_plan()

        # Get all power sensors
        power_sensor_entities = [
            entity_id
            for entity_id in self.hass.states.async_entity_ids(SENSOR_DOMAIN)
            if self.hass.states.get(entity_id).attributes.get("device_class") == "power"
        ]

        data_schema = vol.Schema(
            {
                vol.Required(CONF_POWER_SENSORS): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain=SENSOR_DOMAIN,
                        device_class="power",
                        multiple=True,
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "sensor_count": str(len(power_sensor_entities))
            },
        )

    async def async_step_rate_plan(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle rate plan selection."""
        errors: dict[str, str] = {}

        if user_input is not None:
            use_preset = user_input.get(CONF_USE_PRESET, True)

            if use_preset:
                return await self.async_step_preset_plan()
            else:
                return await self.async_step_custom_plan()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_USE_PRESET, default=True): selector.BooleanSelector(),
            }
        )

        return self.async_show_form(
            step_id="rate_plan",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "preset_count": str(len(RATE_PLAN_TEMPLATES))
            },
        )

    async def async_step_preset_plan(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle preset rate plan selection."""
        errors: dict[str, str] = {}

        if user_input is not None:
            rate_plan = user_input.get(CONF_RATE_PLAN)

            if rate_plan in RATE_PLAN_TEMPLATES:
                self._rate_plan = rate_plan
                self._rate_config = RATE_PLAN_TEMPLATES[rate_plan]["config"]

                return self.async_create_entry(
                    title=RATE_PLAN_TEMPLATES[rate_plan]["name"],
                    data={
                        CONF_POWER_SENSORS: self._power_sensors,
                        CONF_RATE_PLAN: self._rate_plan,
                        CONF_RATE_CONFIG: self._rate_config,
                    },
                )
            else:
                errors[CONF_RATE_PLAN] = "invalid_plan"

        # Create options for rate plans
        rate_plan_options = {
            plan_id: template["name"]
            for plan_id, template in RATE_PLAN_TEMPLATES.items()
        }

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_RATE_PLAN, default=RATE_PLAN_SUMMER_TOU
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(
                                value=plan_id, label=template["name"]
                            )
                            for plan_id, template in RATE_PLAN_TEMPLATES.items()
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="preset_plan",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_custom_plan(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle custom rate plan configuration."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # For simplicity, use a basic custom configuration
            # In production, this would be a multi-step form
            summer_peak_rate = user_input.get("summer_peak_rate", 0.20)
            summer_offpeak_rate = user_input.get("summer_offpeak_rate", 0.15)
            winter_rate = user_input.get("winter_rate", 0.16)

            self._rate_plan = RATE_PLAN_CUSTOM
            self._rate_config = {
                "summer": {
                    "months": [6, 7, 8, 9],
                    "weekday": {
                        "periods": [
                            {
                                "name": "Peak",
                                "start": "14:00",
                                "end": "19:00",
                                "rate": summer_peak_rate,
                            }
                        ],
                        "default_rate": summer_offpeak_rate,
                        "default_name": "Off-Peak",
                    },
                    "weekend": {
                        "default_rate": summer_offpeak_rate,
                        "default_name": "Off-Peak",
                    },
                },
                "winter": {
                    "months": [10, 11, 12, 1, 2, 3, 4, 5],
                    "default_rate": winter_rate,
                    "default_name": "Standard",
                },
            }

            return self.async_create_entry(
                title="Custom Rate Plan",
                data={
                    CONF_POWER_SENSORS: self._power_sensors,
                    CONF_RATE_PLAN: self._rate_plan,
                    CONF_RATE_CONFIG: self._rate_config,
                },
            )

        data_schema = vol.Schema(
            {
                vol.Required("summer_peak_rate", default=0.20): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0.0,
                        max=1.0,
                        step=0.001,
                        mode=selector.NumberSelectorMode.BOX,
                        unit_of_measurement="$/kWh",
                    ),
                ),
                vol.Required(
                    "summer_offpeak_rate", default=0.15
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0.0,
                        max=1.0,
                        step=0.001,
                        mode=selector.NumberSelectorMode.BOX,
                        unit_of_measurement="$/kWh",
                    ),
                ),
                vol.Required("winter_rate", default=0.16): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0.0,
                        max=1.0,
                        step=0.001,
                        mode=selector.NumberSelectorMode.BOX,
                        unit_of_measurement="$/kWh",
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="custom_plan",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> ConsumersEnergyOptionsFlow:
        """Get the options flow for this handler."""
        return ConsumersEnergyOptionsFlow(config_entry)


class ConsumersEnergyOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Consumers Energy Cost Tracker."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            power_sensors = user_input.get(CONF_POWER_SENSORS, [])

            if not power_sensors:
                errors[CONF_POWER_SENSORS] = "no_sensors"
            else:
                # Update config entry data
                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    data={**self.config_entry.data, **user_input},
                )
                # Trigger reload of the integration
                await self.hass.config_entries.async_reload(self.config_entry.entry_id)
                return self.async_create_entry(title="", data={})

        # Get current sensors from config entry
        current_sensors = self.config_entry.data.get(CONF_POWER_SENSORS, [])

        # Ensure current_sensors is a list
        if not isinstance(current_sensors, list):
            current_sensors = []

        # Build the form with current values pre-selected
        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(
                    {
                        vol.Required(CONF_POWER_SENSORS): selector.EntitySelector(
                            selector.EntitySelectorConfig(
                                domain=SENSOR_DOMAIN,
                                device_class="power",
                                multiple=True,
                            ),
                        ),
                    }
                ),
                {CONF_POWER_SENSORS: current_sensors},
            ),
            errors=errors,
            description_placeholders={
                "sensor_count": str(len(current_sensors)),
            },
        )
