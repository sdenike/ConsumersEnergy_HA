"""Rate calculator for time-of-use and seasonal pricing."""
from datetime import datetime, time
import logging

_LOGGER = logging.getLogger(__name__)


class RateCalculator:
    """Calculate electricity rates based on time, day, and season."""

    def __init__(self, rate_config: dict) -> None:
        """Initialize the rate calculator.

        Args:
            rate_config: Rate configuration dictionary with summer/winter seasons
        """
        self.rate_config = rate_config

    def get_rate(self, dt: datetime) -> tuple[float, str]:
        """Get the current rate and period name for a given datetime.

        Args:
            dt: The datetime to calculate rate for

        Returns:
            Tuple of (rate_per_kwh, period_name)
        """
        # Determine season
        month = dt.month
        season_config = self._get_season_config(month)

        if season_config is None:
            _LOGGER.error("No season config found for month %s", month)
            return (0.0, "Unknown")

        # Determine if weekday or weekend
        is_weekend = dt.weekday() >= 5  # Saturday = 5, Sunday = 6

        # Get day type config
        if is_weekend and "weekend" in season_config:
            day_config = season_config["weekend"]
        elif not is_weekend and "weekday" in season_config:
            day_config = season_config["weekday"]
        else:
            # Fallback to default rate
            default_rate = season_config.get("default_rate", 0.0)
            default_name = season_config.get("default_name", "Standard")
            return (default_rate, default_name)

        # Check if current time falls within any defined periods
        current_time = dt.time()
        periods = day_config.get("periods", [])

        for period in periods:
            start_time = self._parse_time(period["start"])
            end_time = self._parse_time(period["end"])

            if self._time_in_range(current_time, start_time, end_time):
                return (period["rate"], period["name"])

        # No period matched, use default rate
        default_rate = day_config.get("default_rate", 0.0)
        default_name = day_config.get("default_name", "Off-Peak")
        return (default_rate, default_name)

    def _get_season_config(self, month: int) -> dict | None:
        """Get the season configuration for a given month.

        Args:
            month: Month number (1-12)

        Returns:
            Season configuration dict or None
        """
        for season_name, season_config in self.rate_config.items():
            if month in season_config.get("months", []):
                return season_config
        return None

    def _parse_time(self, time_str: str) -> time:
        """Parse a time string in HH:MM format.

        Args:
            time_str: Time string like "14:00"

        Returns:
            time object
        """
        hour, minute = map(int, time_str.split(":"))
        return time(hour, minute)

    def _time_in_range(self, current: time, start: time, end: time) -> bool:
        """Check if current time is within start and end times.

        Args:
            current: Current time
            start: Start time of period
            end: End time of period

        Returns:
            True if current is within the range
        """
        if start <= end:
            # Normal range (e.g., 14:00 to 19:00)
            return start <= current < end
        else:
            # Range crosses midnight (e.g., 23:00 to 01:00)
            return current >= start or current < end

    def get_season_name(self, dt: datetime) -> str:
        """Get the season name for a given datetime.

        Args:
            dt: The datetime to check

        Returns:
            Season name ("summer" or "winter")
        """
        month = dt.month
        if month in self.rate_config.get("summer", {}).get("months", []):
            return "Summer"
        elif month in self.rate_config.get("winter", {}).get("months", []):
            return "Winter"
        return "Unknown"
