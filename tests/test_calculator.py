"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

This module tests the PrayerTimeCalculator class and calculate_prayer_times
function, which coordinate all calculation modules.

Author: Omar Younis
Date: 23/10/2025 [dd/mm/yyyy]
"""

import unittest
from datetime import datetime
from prayer_times.calculator.calculator import (
    PrayerTimeCalculator,
    calculate_prayer_times
)
from prayer_times.config import UserSettings


class TestPrayerTimeCalculator(unittest.TestCase):
    """
    Tests the PrayerTimeCalculator class.
    """

    def test_calculator_initialization(self):
        """Tests that the calculator initializes with correct attributes."""
        lat = 40.7128
        lng = -74.0060
        elev = 10.0
        settings = UserSettings(method='isna', asr_method='standard')

        calc = PrayerTimeCalculator(lat, lng, elev, settings)

        self.assertEqual(calc.latitude, lat)
        self.assertEqual(calc.longitude, lng)
        self.assertEqual(calc.elevation, elev)
        self.assertEqual(calc.settings, settings)

    def test_calculator_default_settings(self):
        """
        Tests that the calculator uses the correct default settings when no
        settings are provided.
        
        Defaults should be: method='isna', asr_method='standard', hijri_correction=0
        """
        calc = PrayerTimeCalculator(40.0, -74.0, 10.0)

        # Should have a UserSettings object with correct defaults
        self.assertIsInstance(calc.settings, UserSettings)
        self.assertEqual(calc.settings.calculation_method, 'isna')
        self.assertEqual(calc.settings.asr_method, 'standard')
        self.assertEqual(calc.settings.hijri_correction, 0)

    def test_calculate_returns_all_keys(self):
        """Tests that calculate() returns all expected keys in result dictionary."""
        calc = PrayerTimeCalculator(40.7128, -74.0060, 10.0)
        date = datetime(2025, 1, 1)
        result = calc.calculate(date)

        # Checking main keys
        required_keys = ['qibla', 'gregorian_date', 'hijri_date', 'times', 'times_rounded']
        for key in required_keys:
            self.assertIn(key, result)

        # Checking prayer time keys
        prayer_keys = ['fajr', 'sunrise', 'dhuhr', 'asr', 'maghrib', 'isha']
        for key in prayer_keys:
            self.assertIn(key, result['times'])
            self.assertIn(key, result['times_rounded'])

    def test_calculate_new_york_jan1_2025_isna(self):
        """
        Tests full calculation for New York on Jan 1, 2025 with ISNA method.
        Checks Qibla, Hijri date, and all prayer times.
        """
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elev = 10.0

        settings = UserSettings(method='isna', asr_method='standard', hijri_correction=0)
        calc = PrayerTimeCalculator(lat, lng, elev, settings)
        result = calc.calculate(date)

        # Test Qibla direction
        self.assertAlmostEqual(result['qibla'], 58.48, delta=0.01)

        # Test Hijri date (Jumada Al-Thani 29, 1446)
        self.assertEqual(result['hijri_date']['day'], 29)
        self.assertEqual(result['hijri_date']['month'], 6)
        self.assertEqual(result['hijri_date']['year'], 1446)

        # Test Gregorian date
        self.assertEqual(result['gregorian_date'], date)

        # Test prayer times
        times = result['times']

        self.assertEqual(times['fajr'].hour, 2)
        self.assertAlmostEqual(times['fajr'].minute, 59, delta=1)

        self.assertEqual(times['sunrise'].hour, 4)
        self.assertAlmostEqual(times['sunrise'].minute, 20, delta=1)

        self.assertEqual(times['dhuhr'].hour, 9)
        self.assertAlmostEqual(times['dhuhr'].minute, 0, delta=1)

        self.assertEqual(times['asr'].hour, 11)
        self.assertAlmostEqual(times['asr'].minute, 22, delta=1)

        self.assertEqual(times['maghrib'].hour, 13)
        self.assertAlmostEqual(times['maghrib'].minute, 40, delta=1)

        self.assertEqual(times['isha'].hour, 15)
        self.assertAlmostEqual(times['isha'].minute, 1, delta=1)

    def test_prayer_times_chronological_order(self):
        """Tests that all prayer times are in correct order."""
        calc = PrayerTimeCalculator(40.7128, -74.0060, 10.0)
        date = datetime(2025, 1, 1)
        result = calc.calculate(date)

        times = result['times']

        # Checking correct order: Fajr < Sunrise < Dhuhr < Asr < Maghrib < Isha
        self.assertLess(times['fajr'], times['sunrise'])
        self.assertLess(times['sunrise'], times['dhuhr'])
        self.assertLess(times['dhuhr'], times['asr'])
        self.assertLess(times['asr'], times['maghrib'])
        self.assertLess(times['maghrib'], times['isha'])

    def test_mwl_method_new_york_jan1_2025(self):
        """
        Tests MWL calculation method for New York on Jan 1, 2025.
        MWL uses 18° for Fajr and 17° for Isha.
        Expected: Fajr 02:42:44, Isha 15:12:54
        """
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elev = 10.0

        settings = UserSettings(method='mwl', asr_method='standard', hijri_correction=0)
        calc = PrayerTimeCalculator(lat, lng, elev, settings)
        result = calc.calculate(date)

        times = result['times']

        # Tests MWL Fajr time
        self.assertEqual(times['fajr'].hour, 2)
        self.assertAlmostEqual(times['fajr'].minute, 42, delta=1)

        # Tests MWL Isha time
        self.assertEqual(times['isha'].hour, 15)
        self.assertAlmostEqual(times['isha'].minute, 12, delta=1)

        # MWL Fajr should be earlier than ISNA Fajr
        settings_isna = UserSettings(method='isna', asr_method='standard')
        calc_isna = PrayerTimeCalculator(lat, lng, elev, settings_isna)
        result_isna = calc_isna.calculate(date)

        self.assertLess(times['fajr'], result_isna['times']['fajr'])
        self.assertGreater(times['isha'], result_isna['times']['isha'])

    def test_asr_standard_vs_hanafi(self):
        """Tests that Hanafi Asr method gives a later time than standard."""
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elev = 10.0

        # Standard Asr
        settings_std = UserSettings(method='isna', asr_method='standard')
        calc_std = PrayerTimeCalculator(lat, lng, elev, settings_std)
        result_std = calc_std.calculate(date)

        # Hanafi Asr
        settings_hanafi = UserSettings(method='isna', asr_method='hanafi')
        calc_hanafi = PrayerTimeCalculator(lat, lng, elev, settings_hanafi)
        result_hanafi = calc_hanafi.calculate(date)

        # Hanafi should be later
        self.assertGreater(result_hanafi['times']['asr'], result_std['times']['asr'])

        # Difference should be about 37 minutes
        diff_minutes = (result_hanafi['times']['asr'] - result_std['times']['asr']).total_seconds() / 60
        self.assertAlmostEqual(diff_minutes, 37.0, delta=3.0)

    def test_ramadan_isha_timing_uqu_method(self):
        """
        Tests that UQU method adjusts Isha time during Ramadan.
        During Ramadan (Hijri month 9), Isha should be 120 minutes after Maghrib.
        Otherwise, it should be 90 minutes after Maghrib.
        """
        lat = 21.5  # Makkah area
        lng = 39.8
        elev = 300

        settings = UserSettings(method='uqu', asr_method='standard', hijri_correction=0)
        calc = PrayerTimeCalculator(lat, lng, elev, settings)

        # Date that falls in Ramadan 1446
        date_ramadan = datetime(2025, 3, 10)
        result_ramadan = calc.calculate(date_ramadan)

        # Checking it's actually Ramadan
        self.assertEqual(result_ramadan['hijri_date']['month'], 9)

        # Calculating Isha-Maghrib difference
        diff = result_ramadan['times']['isha'] - result_ramadan['times']['maghrib']
        diff_minutes = diff.total_seconds() / 60

        # Should be 120 minutes during Ramadan
        self.assertAlmostEqual(diff_minutes, 120.0, delta=0.5)

    def test_hijri_correction_adds_days(self):
        """
        Tests that hijri_correction parameter correctly adjusts Hijri date.
        
        Jan 1, 2025 with no correction: Jumada Al-Thani 29, 1446
        Jan 1, 2025 with +1 correction: Rajab 1, 1446 (next day, new month)
        """
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elev = 10.0

        # No correction (baseline)
        settings_0 = UserSettings(method='isna', hijri_correction=0)
        calc_0 = PrayerTimeCalculator(lat, lng, elev, settings_0)
        result_0 = calc_0.calculate(date)

        # Checking baseline is month 6, day 29
        self.assertEqual(result_0['hijri_date']['month'], 6)
        self.assertEqual(result_0['hijri_date']['day'], 29)

        # +1 day correction (should wrap to next month)
        settings_plus1 = UserSettings(method='isna', hijri_correction=1)
        calc_plus1 = PrayerTimeCalculator(lat, lng, elev, settings_plus1)
        result_plus1 = calc_plus1.calculate(date)

        # Should be Rajab 1 (month 7, day 1)
        self.assertEqual(result_plus1['hijri_date']['month'], 7)
        self.assertEqual(result_plus1['hijri_date']['day'], 1)
        self.assertEqual(result_plus1['hijri_date']['year'], 1446)

    def test_rounded_times_are_actually_rounded(self):
        """Tests that times_rounded has seconds set to 0."""
        calc = PrayerTimeCalculator(40.7128, -74.0060, 10.0)
        date = datetime(2025, 1, 1)
        result = calc.calculate(date)

        # Rounded times should have 0 seconds
        for prayer in ['fajr', 'sunrise', 'dhuhr', 'asr', 'maghrib', 'isha']:
            rounded_time = result['times_rounded'][prayer]
            self.assertEqual(rounded_time.second, 0,
                           f"{prayer} rounded time has non-zero seconds")

    def test_calculate_uses_current_date_when_none_provided(self):
        """Tests that calculate() uses current date when date=None."""
        calc = PrayerTimeCalculator(40.7128, -74.0060, 10.0)
        result = calc.calculate()

        # Should return results without error
        self.assertIn('times', result)

        # Gregorian date should be today
        today = datetime.now().date()
        result_date = result['gregorian_date'].date()
        self.assertEqual(result_date, today)


class TestCalculatePrayerTimesFunction(unittest.TestCase):
    """
    Tests the calculate_prayer_times convenience function.
    """

    def test_function_returns_same_as_class(self):
        """Tests that the function returns same results as using the class."""
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elev = 10.0
        settings = UserSettings(method='isna', asr_method='standard')

        # Using the class
        calc = PrayerTimeCalculator(lat, lng, elev, settings)
        result_class = calc.calculate(date)

        # Using the function
        result_func = calculate_prayer_times(lat, lng, elev, date, settings)

        # Should be tje same
        self.assertEqual(result_class['qibla'], result_func['qibla'])
        self.assertEqual(result_class['hijri_date'], result_func['hijri_date'])

        # Check all prayer times match
        for prayer in ['fajr', 'sunrise', 'dhuhr', 'asr', 'maghrib', 'isha']:
            self.assertEqual(result_class['times'][prayer], result_func['times'][prayer])


if __name__ == '__main__':
    unittest.main()
