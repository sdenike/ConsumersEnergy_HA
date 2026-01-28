"""Standalone tests for the rate calculator without Home Assistant dependencies."""
import unittest
from datetime import datetime, time


class RateCalculator:
    """Calculate electricity rates based on time, day, and season."""

    def __init__(self, rate_config: dict) -> None:
        """Initialize the rate calculator."""
        self.rate_config = rate_config

    def get_rate(self, dt: datetime) -> tuple[float, str]:
        """Get the current rate and period name for a given datetime."""
        month = dt.month
        season_config = self._get_season_config(month)

        if season_config is None:
            return (0.0, "Unknown")

        is_weekend = dt.weekday() >= 5

        if is_weekend and "weekend" in season_config:
            day_config = season_config["weekend"]
        elif not is_weekend and "weekday" in season_config:
            day_config = season_config["weekday"]
        else:
            default_rate = season_config.get("default_rate", 0.0)
            default_name = season_config.get("default_name", "Standard")
            return (default_rate, default_name)

        current_time = dt.time()
        periods = day_config.get("periods", [])

        for period in periods:
            start_time = self._parse_time(period["start"])
            end_time = self._parse_time(period["end"])

            if self._time_in_range(current_time, start_time, end_time):
                return (period["rate"], period["name"])

        default_rate = day_config.get("default_rate", 0.0)
        default_name = day_config.get("default_name", "Off-Peak")
        return (default_rate, default_name)

    def _get_season_config(self, month: int) -> dict | None:
        """Get the season configuration for a given month."""
        for season_name, season_config in self.rate_config.items():
            if month in season_config.get("months", []):
                return season_config
        return None

    def _parse_time(self, time_str: str) -> time:
        """Parse a time string in HH:MM format."""
        hour, minute = map(int, time_str.split(":"))
        return time(hour, minute)

    def _time_in_range(self, current: time, start: time, end: time) -> bool:
        """Check if current time is within start and end times."""
        if start <= end:
            return start <= current < end
        else:
            return current >= start or current < end

    def get_season_name(self, dt: datetime) -> str:
        """Get the season name for a given datetime."""
        month = dt.month
        if month in self.rate_config.get("summer", {}).get("months", []):
            return "Summer"
        elif month in self.rate_config.get("winter", {}).get("months", []):
            return "Winter"
        return "Unknown"


# Rate plan configurations
SUMMER_TOU_CONFIG = {
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
}


class TestRateCalculator(unittest.TestCase):
    """Test the RateCalculator class."""

    def test_summer_tou_on_peak_weekday(self):
        """Test Summer TOU rate during on-peak hours on weekday."""
        calculator = RateCalculator(SUMMER_TOU_CONFIG)

        # July 15, 2025 (Tuesday) at 3pm - Summer weekday peak
        dt = datetime(2025, 7, 15, 15, 0, 0)
        rate, period = calculator.get_rate(dt)

        self.assertEqual(rate, 0.23, "Summer on-peak rate should be $0.23/kWh")
        self.assertEqual(period, "On-Peak", "Period should be On-Peak")

    def test_summer_tou_off_peak_weekday(self):
        """Test Summer TOU rate during off-peak hours on weekday."""
        calculator = RateCalculator(SUMMER_TOU_CONFIG)

        # July 15, 2025 (Tuesday) at 10am - Summer weekday off-peak
        dt = datetime(2025, 7, 15, 10, 0, 0)
        rate, period = calculator.get_rate(dt)

        self.assertEqual(rate, 0.178, "Summer off-peak rate should be $0.178/kWh")
        self.assertEqual(period, "Off-Peak", "Period should be Off-Peak")

    def test_summer_tou_weekend(self):
        """Test Summer TOU rate on weekend."""
        calculator = RateCalculator(SUMMER_TOU_CONFIG)

        # July 19, 2025 (Saturday) at 3pm - Summer weekend (always off-peak)
        dt = datetime(2025, 7, 19, 15, 0, 0)
        rate, period = calculator.get_rate(dt)

        self.assertEqual(rate, 0.178, "Summer weekend rate should be $0.178/kWh")
        self.assertEqual(period, "Off-Peak", "Period should be Off-Peak")

    def test_winter_flat_rate(self):
        """Test Winter flat rate."""
        calculator = RateCalculator(SUMMER_TOU_CONFIG)

        # January 15, 2025 (Wednesday) at 3pm - Winter flat rate
        dt = datetime(2025, 1, 15, 15, 0, 0)
        rate, period = calculator.get_rate(dt)

        self.assertEqual(rate, 0.164, "Winter rate should be $0.164/kWh")
        self.assertEqual(period, "Standard", "Period should be Standard")

    def test_peak_hour_boundaries(self):
        """Test rate changes at peak hour boundaries."""
        calculator = RateCalculator(SUMMER_TOU_CONFIG)

        # July 15, 2025 (Tuesday) - Test boundary times
        # 1:59pm - should be off-peak
        dt_before = datetime(2025, 7, 15, 13, 59, 0)
        rate_before, period_before = calculator.get_rate(dt_before)
        self.assertEqual(rate_before, 0.178, "Should be off-peak before 2pm")

        # 2:00pm - should be on-peak
        dt_start = datetime(2025, 7, 15, 14, 0, 0)
        rate_start, period_start = calculator.get_rate(dt_start)
        self.assertEqual(rate_start, 0.23, "Should be on-peak at 2pm")

        # 6:59pm - should still be on-peak
        dt_during = datetime(2025, 7, 15, 18, 59, 0)
        rate_during, period_during = calculator.get_rate(dt_during)
        self.assertEqual(rate_during, 0.23, "Should be on-peak before 7pm")

        # 7:00pm - should be off-peak again
        dt_after = datetime(2025, 7, 15, 19, 0, 0)
        rate_after, period_after = calculator.get_rate(dt_after)
        self.assertEqual(rate_after, 0.178, "Should be off-peak at 7pm")

    def test_season_transitions(self):
        """Test season boundary transitions."""
        calculator = RateCalculator(SUMMER_TOU_CONFIG)

        # May 31 - last day of winter
        dt_may = datetime(2025, 5, 31, 15, 0, 0)
        rate_may, _ = calculator.get_rate(dt_may)
        self.assertEqual(rate_may, 0.164, "May should use winter rate")

        # June 1 - first day of summer, Sunday
        dt_june = datetime(2025, 6, 1, 15, 0, 0)  # Sunday, so off-peak
        rate_june, _ = calculator.get_rate(dt_june)
        self.assertEqual(rate_june, 0.178, "June 1 (Sunday) should use summer off-peak rate")

        # June 2 - first weekday of summer, peak time
        dt_june_weekday = datetime(2025, 6, 2, 15, 0, 0)  # Monday
        rate_june_weekday, _ = calculator.get_rate(dt_june_weekday)
        self.assertEqual(rate_june_weekday, 0.23, "June 2 (Monday) at 3pm should use summer peak rate")

        # September 30 - last day of summer
        dt_sep = datetime(2025, 9, 30, 15, 0, 0)  # Tuesday
        rate_sep, _ = calculator.get_rate(dt_sep)
        self.assertEqual(rate_sep, 0.23, "Sept 30 should use summer peak rate")

        # October 1 - first day of winter
        dt_oct = datetime(2025, 10, 1, 15, 0, 0)
        rate_oct, _ = calculator.get_rate(dt_oct)
        self.assertEqual(rate_oct, 0.164, "October should use winter rate")

    def test_get_season_name(self):
        """Test season name detection."""
        calculator = RateCalculator(SUMMER_TOU_CONFIG)

        # Summer months
        dt_june = datetime(2025, 6, 15, 12, 0, 0)
        self.assertEqual(calculator.get_season_name(dt_june), "Summer")

        dt_july = datetime(2025, 7, 15, 12, 0, 0)
        self.assertEqual(calculator.get_season_name(dt_july), "Summer")

        dt_sept = datetime(2025, 9, 15, 12, 0, 0)
        self.assertEqual(calculator.get_season_name(dt_sept), "Summer")

        # Winter months
        dt_jan = datetime(2025, 1, 15, 12, 0, 0)
        self.assertEqual(calculator.get_season_name(dt_jan), "Winter")

        dt_oct = datetime(2025, 10, 15, 12, 0, 0)
        self.assertEqual(calculator.get_season_name(dt_oct), "Winter")

        dt_may = datetime(2025, 5, 15, 12, 0, 0)
        self.assertEqual(calculator.get_season_name(dt_may), "Winter")


if __name__ == '__main__':
    unittest.main()
