"""Tests for the rate calculator."""
import unittest
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from custom_components.consumers_energy_cost.rate_calculator import RateCalculator
from custom_components.consumers_energy_cost.const import RATE_PLAN_TEMPLATES, RATE_PLAN_SUMMER_TOU, RATE_PLAN_NIGHTTIME_SAVERS


class TestRateCalculator(unittest.TestCase):
    """Test the RateCalculator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.summer_tou_config = RATE_PLAN_TEMPLATES[RATE_PLAN_SUMMER_TOU]["config"]
        self.nighttime_savers_config = RATE_PLAN_TEMPLATES[RATE_PLAN_NIGHTTIME_SAVERS]["config"]

    def test_summer_tou_on_peak_weekday(self):
        """Test Summer TOU rate during on-peak hours on weekday."""
        calculator = RateCalculator(self.summer_tou_config)

        # July 15, 2025 (Tuesday) at 3pm - Summer weekday peak
        dt = datetime(2025, 7, 15, 15, 0, 0)
        rate, period = calculator.get_rate(dt)

        self.assertEqual(rate, 0.23, "Summer on-peak rate should be $0.23/kWh")
        self.assertEqual(period, "On-Peak", "Period should be On-Peak")

    def test_summer_tou_off_peak_weekday(self):
        """Test Summer TOU rate during off-peak hours on weekday."""
        calculator = RateCalculator(self.summer_tou_config)

        # July 15, 2025 (Tuesday) at 10am - Summer weekday off-peak
        dt = datetime(2025, 7, 15, 10, 0, 0)
        rate, period = calculator.get_rate(dt)

        self.assertEqual(rate, 0.178, "Summer off-peak rate should be $0.178/kWh")
        self.assertEqual(period, "Off-Peak", "Period should be Off-Peak")

    def test_summer_tou_weekend(self):
        """Test Summer TOU rate on weekend."""
        calculator = RateCalculator(self.summer_tou_config)

        # July 19, 2025 (Saturday) at 3pm - Summer weekend (always off-peak)
        dt = datetime(2025, 7, 19, 15, 0, 0)
        rate, period = calculator.get_rate(dt)

        self.assertEqual(rate, 0.178, "Summer weekend rate should be $0.178/kWh")
        self.assertEqual(period, "Off-Peak", "Period should be Off-Peak")

    def test_winter_flat_rate(self):
        """Test Winter flat rate."""
        calculator = RateCalculator(self.summer_tou_config)

        # January 15, 2025 (Wednesday) at 3pm - Winter flat rate
        dt = datetime(2025, 1, 15, 15, 0, 0)
        rate, period = calculator.get_rate(dt)

        self.assertEqual(rate, 0.164, "Winter rate should be $0.164/kWh")
        self.assertEqual(period, "Standard", "Period should be Standard")

    def test_peak_hour_boundaries(self):
        """Test rate changes at peak hour boundaries."""
        calculator = RateCalculator(self.summer_tou_config)

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
        calculator = RateCalculator(self.summer_tou_config)

        # May 31 - last day of winter
        dt_may = datetime(2025, 5, 31, 15, 0, 0)
        rate_may, _ = calculator.get_rate(dt_may)
        self.assertEqual(rate_may, 0.164, "May should use winter rate")

        # June 1 - first day of summer, weekday peak time
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

    def test_nighttime_savers_three_tier(self):
        """Test Nighttime Savers three-tier pricing."""
        calculator = RateCalculator(self.nighttime_savers_config)

        # Summer weekday - test all three tiers
        # Super off-peak: 2am
        dt_super = datetime(2025, 7, 15, 2, 0, 0)  # Tuesday
        rate_super, period_super = calculator.get_rate(dt_super)
        self.assertEqual(rate_super, 0.133, "Should be super off-peak rate")
        self.assertEqual(period_super, "Super Off-Peak")

        # Off-peak: 10am
        dt_off = datetime(2025, 7, 15, 10, 0, 0)
        rate_off, period_off = calculator.get_rate(dt_off)
        self.assertEqual(rate_off, 0.173, "Should be off-peak rate")
        self.assertEqual(period_off, "Off-Peak")

        # On-peak: 3pm
        dt_on = datetime(2025, 7, 15, 15, 0, 0)
        rate_on, period_on = calculator.get_rate(dt_on)
        self.assertEqual(rate_on, 0.212, "Should be on-peak rate")
        self.assertEqual(period_on, "On-Peak")

        # Off-peak again: 8pm
        dt_off2 = datetime(2025, 7, 15, 20, 0, 0)
        rate_off2, period_off2 = calculator.get_rate(dt_off2)
        self.assertEqual(rate_off2, 0.173, "Should be off-peak rate")

        # Super off-peak: 11:30pm
        dt_super2 = datetime(2025, 7, 15, 23, 30, 0)
        rate_super2, period_super2 = calculator.get_rate(dt_super2)
        self.assertEqual(rate_super2, 0.133, "Should be super off-peak rate")

    def test_nighttime_savers_weekend(self):
        """Test Nighttime Savers weekend (all super off-peak)."""
        calculator = RateCalculator(self.nighttime_savers_config)

        # Saturday at 3pm (normally peak) - should be super off-peak
        dt_weekend = datetime(2025, 7, 19, 15, 0, 0)  # Saturday
        rate_weekend, period_weekend = calculator.get_rate(dt_weekend)

        self.assertEqual(rate_weekend, 0.133, "Weekend should be super off-peak rate")
        self.assertEqual(period_weekend, "Super Off-Peak")

    def test_get_season_name(self):
        """Test season name detection."""
        calculator = RateCalculator(self.summer_tou_config)

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
