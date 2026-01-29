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
    CONF_INSTANCE_NAME,
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
        self._instance_name: str = ""
        self._power_sensors: list[str] = []
        self._rate_plan: str | None = None
        self._rate_config: dict | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial step - instance name and sensor selection."""
        errors: dict[str, str] = {}

        if user_input is not None:
            instance_name = user_input.get(CONF_INSTANCE_NAME, "").strip()
            power_sensors = user_input.get(CONF_POWER_SENSORS, [])

            if not instance_name:
                errors[CONF_INSTANCE_NAME] = "no_name"
            elif not power_sensors:
                errors[CONF_POWER_SENSORS] = "no_sensors"
            else:
                self._instance_name = instance_name
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
                vol.Required(CONF_INSTANCE_NAME, default="All Sensors"): selector.TextSelector(
                    selector.TextSelectorConfig(
                        type=selector.TextSelectorType.TEXT,
                    ),
                ),
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
                    title=self._instance_name,
                    data={
                        CONF_INSTANCE_NAME: self._instance_name,
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
                title=self._instance_name,
                data={
                    CONF_INSTANCE_NAME: self._instance_name,
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
        return ConsumersEnergyOptionsFlow()


class ConsumersEnergyOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Consumers Energy Cost Tracker."""

    def __init__(self) -> None:
        """Initialize the options flow."""
        self._update_type: str | None = None

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Manage the options - choose what to update."""
        if user_input is not None:
            self._update_type = user_input.get("update_type")

            if self._update_type == "sensors":
                return await self.async_step_update_sensors()
            elif self._update_type == "rates":
                return await self.async_step_update_rates()

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required("update_type"): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=[
                                selector.SelectOptionDict(
                                    value="sensors",
                                    label="Update Power Sensors"
                                ),
                                selector.SelectOptionDict(
                                    value="rates",
                                    label="Update Rate Plan / Custom Rates"
                                ),
                            ],
                            mode=selector.SelectSelectorMode.LIST,
                        ),
                    ),
                }
            ),
        )

    async def async_step_update_sensors(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Update power sensors."""
        errors: dict[str, str] = {}

        if user_input is not None:
            power_sensors = user_input.get(CONF_POWER_SENSORS, [])

            if not power_sensors:
                errors[CONF_POWER_SENSORS] = "no_sensors"
            else:
                # Update config entry data
                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    data={**self.config_entry.data, CONF_POWER_SENSORS: power_sensors},
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
            step_id="update_sensors",
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

    async def async_step_update_rates(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Update rate plan."""
        errors: dict[str, str] = {}

        if user_input is not None:
            rate_plan = user_input.get(CONF_RATE_PLAN)

            if rate_plan == RATE_PLAN_CUSTOM:
                # Go to custom rate entry
                return await self.async_step_custom_rates()
            elif rate_plan in RATE_PLAN_TEMPLATES:
                # Update with preset rates
                rate_config = RATE_PLAN_TEMPLATES[rate_plan]["config"]

                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    data={
                        **self.config_entry.data,
                        CONF_RATE_PLAN: rate_plan,
                        CONF_RATE_CONFIG: rate_config,
                    },
                )
                await self.hass.config_entries.async_reload(self.config_entry.entry_id)
                return self.async_create_entry(title="", data={})
            else:
                errors[CONF_RATE_PLAN] = "invalid_plan"

        # Get current rate plan
        current_rate_plan = self.config_entry.data.get(CONF_RATE_PLAN, RATE_PLAN_SUMMER_TOU)

        return self.async_show_form(
            step_id="update_rates",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(
                    {
                        vol.Required(CONF_RATE_PLAN): selector.SelectSelector(
                            selector.SelectSelectorConfig(
                                options=[
                                    selector.SelectOptionDict(
                                        value=plan_id, label=template["name"]
                                    )
                                    for plan_id, template in RATE_PLAN_TEMPLATES.items()
                                ] + [
                                    selector.SelectOptionDict(
                                        value=RATE_PLAN_CUSTOM, label="Custom Rates"
                                    )
                                ],
                                mode=selector.SelectSelectorMode.DROPDOWN,
                            ),
                        ),
                    }
                ),
                {CONF_RATE_PLAN: current_rate_plan},
            ),
            errors=errors,
        )

    async def async_step_custom_rates(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Update custom rates."""
        if user_input is not None:
            summer_peak_rate = user_input.get("summer_peak_rate", 0.20)
            summer_offpeak_rate = user_input.get("summer_offpeak_rate", 0.15)
            winter_rate = user_input.get("winter_rate", 0.16)

            rate_config = {
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

            self.hass.config_entries.async_update_entry(
                self.config_entry,
                data={
                    **self.config_entry.data,
                    CONF_RATE_PLAN: RATE_PLAN_CUSTOM,
                    CONF_RATE_CONFIG: rate_config,
                },
            )
            await self.hass.config_entries.async_reload(self.config_entry.entry_id)
            return self.async_create_entry(title="", data={})

        # Get current custom rates if they exist
        current_config = self.config_entry.data.get(CONF_RATE_CONFIG, {})
        summer_config = current_config.get("summer", {})
        winter_config = current_config.get("winter", {})

        # Extract current values
        current_summer_peak = 0.20
        current_summer_offpeak = 0.15
        current_winter = 0.16

        if "weekday" in summer_config:
            weekday = summer_config["weekday"]
            if "periods" in weekday and len(weekday["periods"]) > 0:
                current_summer_peak = weekday["periods"][0].get("rate", 0.20)
            current_summer_offpeak = weekday.get("default_rate", 0.15)

        if "default_rate" in winter_config:
            current_winter = winter_config["default_rate"]

        return self.async_show_form(
            step_id="custom_rates",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(
                    {
                        vol.Required("summer_peak_rate"): selector.NumberSelector(
                            selector.NumberSelectorConfig(
                                min=0.0,
                                max=1.0,
                                step=0.001,
                                mode=selector.NumberSelectorMode.BOX,
                                unit_of_measurement="$/kWh",
                            ),
                        ),
                        vol.Required("summer_offpeak_rate"): selector.NumberSelector(
                            selector.NumberSelectorConfig(
                                min=0.0,
                                max=1.0,
                                step=0.001,
                                mode=selector.NumberSelectorMode.BOX,
                                unit_of_measurement="$/kWh",
                            ),
                        ),
                        vol.Required("winter_rate"): selector.NumberSelector(
                            selector.NumberSelectorConfig(
                                min=0.0,
                                max=1.0,
                                step=0.001,
                                mode=selector.NumberSelectorMode.BOX,
                                unit_of_measurement="$/kWh",
                            ),
                        ),
                    }
                ),
                {
                    "summer_peak_rate": current_summer_peak,
                    "summer_offpeak_rate": current_summer_offpeak,
                    "winter_rate": current_winter,
                },
            ),
        )
