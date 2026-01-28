"""Constants for the Consumers Energy Cost Tracker integration."""
from typing import Final

DOMAIN: Final = "consumers_energy_cost"

# Configuration keys
CONF_POWER_SENSORS: Final = "power_sensors"
CONF_RATE_PLAN: Final = "rate_plan"
CONF_RATE_CONFIG: Final = "rate_config"
CONF_USE_PRESET: Final = "use_preset"

# Rate plan presets
RATE_PLAN_SUMMER_TOU: Final = "summer_tou_1001"
RATE_PLAN_SMART_HOURS: Final = "smart_hours_1040"
RATE_PLAN_NIGHTTIME_SAVERS: Final = "nighttime_savers_1050"
RATE_PLAN_CUSTOM: Final = "custom"

# Update interval
UPDATE_INTERVAL_SECONDS: Final = 30

# Sensor entity IDs
SENSOR_TOTAL_POWER: Final = "total_power"
SENSOR_CURRENT_RATE: Final = "current_rate"
SENSOR_COST_RATE: Final = "cost_rate"
SENSOR_RATE_PERIOD: Final = "rate_period"
SENSOR_ENERGY_TODAY: Final = "energy_today"
SENSOR_COST_TODAY: Final = "cost_today"
SENSOR_ENERGY_WEEK: Final = "energy_week"
SENSOR_COST_WEEK: Final = "cost_week"
SENSOR_ENERGY_MONTH: Final = "energy_month"
SENSOR_COST_MONTH: Final = "cost_month"
SENSOR_ENERGY_YEAR: Final = "energy_year"
SENSOR_COST_YEAR: Final = "cost_year"

# Rate plan templates for Consumers Energy
RATE_PLAN_TEMPLATES = {
    RATE_PLAN_SUMMER_TOU: {
        "name": "Summer Time-of-Use (Rate 1001)",
        "description": "Summer peak pricing weekdays 2-7pm, flat rate non-summer",
        "config": {
            "summer": {
                "months": [6, 7, 8, 9],
                "weekday": {
                    "periods": [
                        {
                            "name": "On-Peak",
                            "start": "14:00",
                            "end": "19:00",
                            "rate": 0.23,
                        }
                    ],
                    "default_rate": 0.178,
                    "default_name": "Off-Peak",
                },
                "weekend": {
                    "default_rate": 0.178,
                    "default_name": "Off-Peak",
                },
            },
            "winter": {
                "months": [10, 11, 12, 1, 2, 3, 4, 5],
                "default_rate": 0.164,
                "default_name": "Standard",
            },
        },
    },
    RATE_PLAN_SMART_HOURS: {
        "name": "Smart Hours (Rate 1040)",
        "description": "Peak pricing weekdays 2-7pm year-round (requires manual rate entry)",
        "config": {
            "summer": {
                "months": [6, 7, 8, 9],
                "weekday": {
                    "periods": [
                        {
                            "name": "Peak",
                            "start": "14:00",
                            "end": "19:00",
                            "rate": 0.20,  # Placeholder - user must update
                        }
                    ],
                    "default_rate": 0.15,  # Placeholder - user must update
                    "default_name": "Off-Peak",
                },
                "weekend": {
                    "default_rate": 0.15,
                    "default_name": "Off-Peak",
                },
            },
            "winter": {
                "months": [10, 11, 12, 1, 2, 3, 4, 5],
                "weekday": {
                    "periods": [
                        {
                            "name": "Peak",
                            "start": "14:00",
                            "end": "19:00",
                            "rate": 0.20,  # Placeholder - user must update
                        }
                    ],
                    "default_rate": 0.15,  # Placeholder - user must update
                    "default_name": "Off-Peak",
                },
                "weekend": {
                    "default_rate": 0.15,
                    "default_name": "Off-Peak",
                },
            },
        },
    },
    RATE_PLAN_NIGHTTIME_SAVERS: {
        "name": "Nighttime Savers (Rate 1050)",
        "description": "Three-tier pricing: super off-peak overnight, off-peak daytime, peak afternoon",
        "config": {
            "summer": {
                "months": [6, 7, 8, 9],
                "weekday": {
                    "periods": [
                        {
                            "name": "Super Off-Peak",
                            "start": "00:00",
                            "end": "06:00",
                            "rate": 0.133,
                        },
                        {
                            "name": "On-Peak",
                            "start": "14:00",
                            "end": "19:00",
                            "rate": 0.212,
                        },
                        {
                            "name": "Super Off-Peak",
                            "start": "23:00",
                            "end": "23:59",
                            "rate": 0.133,
                        },
                    ],
                    "default_rate": 0.173,
                    "default_name": "Off-Peak",
                },
                "weekend": {
                    "default_rate": 0.133,
                    "default_name": "Super Off-Peak",
                },
            },
            "winter": {
                "months": [10, 11, 12, 1, 2, 3, 4, 5],
                "weekday": {
                    "periods": [
                        {
                            "name": "Super Off-Peak",
                            "start": "00:00",
                            "end": "06:00",
                            "rate": 0.141,
                        },
                        {
                            "name": "On-Peak",
                            "start": "14:00",
                            "end": "19:00",
                            "rate": 0.169,
                        },
                        {
                            "name": "Super Off-Peak",
                            "start": "23:00",
                            "end": "23:59",
                            "rate": 0.141,
                        },
                    ],
                    "default_rate": 0.168,
                    "default_name": "Off-Peak",
                },
                "weekend": {
                    "default_rate": 0.141,
                    "default_name": "Super Off-Peak",
                },
            },
        },
    },
}
