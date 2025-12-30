"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Tests for Reverse Prayer Time Calculator

This module tests the reverse calculation functionality that determines
what angles would produce observed prayer times.

Author: Omar Younis
Date: 30/12/2024 [dd/mm/yyyy]
"""

import unittest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from prayer_times.calculator.reverse_calculator import (
    _reverse_hour_correction,
    reverse_fajr_angle,
    reverse_isha_angle,
    calculate_isha_minutes,
    validate_prayer_time_sequence,
    validate_angle_range,
    ReversePrayerCalculator,
    reverse_calculate_angles
)
from prayer_times.calculator.calculator import calculate_prayer_times
from prayer_times.calculator.times import _hour_correction, midday_time_calc
from prayer_times.config import UserSettings
from prayer_times.core.astronomy import sun_coordinates
from prayer_times.core.calendar import julian_date


class TestReverseHourCorrection(unittest.TestCase):
    """Tests that _reverse_hour_correction is the inverse of _hour_correction."""

    def setUp(self):
        """Set up test data."""
        # Use New York on January 1, 2025
        self.date = datetime(2025, 1, 1, 12, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        self.lat = 40.7128
        jd = julian_date(self.date)
        self.sun_data = sun_coordinates(jd)

    def test_inverse_relationship_small_offset(self):
        """Test that reverse is inverse of forward for small time offset."""
        time_offset = 0.5  # 30 minutes

        # Forward: time_offset -> theta
        theta = 90 + 15  # Example Fajr angle
        calculated_offset = _hour_correction(theta, self.lat, self.sun_data)

        # Reverse: calculated_offset -> theta
        reverse_theta = _reverse_hour_correction(calculated_offset, self.lat, self.sun_data)

        # Should match within floating point precision
        self.assertAlmostEqual(theta, reverse_theta, places=5)

    def test_inverse_relationship_large_offset(self):
        """Test that reverse is inverse of forward for large time offset."""
        # Test with multiple angles
        for angle in [12, 15, 18, 20, 25]:
            theta = 90 + angle
            time_offset = _hour_correction(theta, self.lat, self.sun_data)
            reverse_theta = _reverse_hour_correction(time_offset, self.lat, self.sun_data)
            self.assertAlmostEqual(theta, reverse_theta, places=5,
                                 msg=f"Failed for angle {angle}°")

    def test_invalid_time_offset_negative(self):
        """Test that negative time offset raises error."""
        with self.assertRaises(ValueError):
            _reverse_hour_correction(-1.0, self.lat, self.sun_data)

    def test_invalid_time_offset_too_large(self):
        """Test that time offset > 12 hours raises error."""
        with self.assertRaises(ValueError):
            _reverse_hour_correction(13.0, self.lat, self.sun_data)


class TestReverseFajrAngle(unittest.TestCase):
    """Tests for reverse_fajr_angle function."""

    def setUp(self):
        """Set up test data for New York."""
        self.lat = 40.7128
        self.lng = -74.0060
        self.elev = 10
        self.date = datetime(2025, 1, 1, tzinfo=ZoneInfo("America/New_York"))

        # Calculate forward prayer times with ISNA (15° Fajr)
        settings = UserSettings(method='isna')
        results = calculate_prayer_times(self.lat, self.lng, self.elev, self.date, settings)

        self.sunrise = results['times']['sunrise']
        self.maghrib = results['times']['maghrib']
        self.fajr = results['times']['fajr']

        # Calculate midday and sun data separately
        jd = julian_date(self.date)
        self.sun_data = sun_coordinates(jd)
        self.midday = midday_time_calc(self.date, self.lng, self.sun_data)

    def test_reverse_fajr_isna_method(self):
        """Test that reversing ISNA Fajr time gives ~15° angle."""
        result = reverse_fajr_angle(
            self.fajr, self.midday, self.lat, self.sun_data,
            self.sunrise, self.maghrib
        )

        # Should be close to 15° (ISNA method) - within 0.5°
        self.assertAlmostEqual(result['angle'], 15.0, places=0)
        self.assertEqual(result['method'], 'standard')
        self.assertTrue(result['valid'])

    def test_reverse_fajr_mwl_method(self):
        """Test that reversing MWL Fajr time gives ~18° angle."""
        # Calculate with MWL (18° Fajr)
        settings = UserSettings(method='mwl')
        results = calculate_prayer_times(self.lat, self.lng, self.elev, self.date, settings)
        fajr_mwl = results['times']['fajr']

        result = reverse_fajr_angle(
            fajr_mwl, self.midday, self.lat, self.sun_data,
            self.sunrise, self.maghrib
        )

        # Should be close to 18° (MWL method) - within 0.5°
        self.assertAlmostEqual(result['angle'], 18.0, places=0)

    def test_fajr_after_midday_raises_error(self):
        """Test that Fajr after midday raises ValueError."""
        invalid_fajr = self.midday + timedelta(hours=1)

        with self.assertRaises(ValueError) as context:
            reverse_fajr_angle(
                invalid_fajr, self.midday, self.lat, self.sun_data,
                self.sunrise, self.maghrib
            )

        self.assertIn("not before solar noon", str(context.exception))

    def test_fajr_unusual_angle_warning(self):
        """Test that unusual angles generate warnings."""
        # Create an artificially early Fajr time (would need very large angle)
        very_early_fajr = self.midday - timedelta(hours=8)

        result = reverse_fajr_angle(
            very_early_fajr, self.midday, self.lat, self.sun_data,
            self.sunrise, self.maghrib, check_high_lat=False
        )

        # Should have warnings
        self.assertGreater(len(result['warnings']), 0)
        self.assertFalse(result['valid'])


class TestReverseIshaAngle(unittest.TestCase):
    """Tests for reverse_isha_angle function."""

    def setUp(self):
        """Set up test data for New York."""
        self.lat = 40.7128
        self.lng = -74.0060
        self.elev = 10
        self.date = datetime(2025, 1, 1, tzinfo=ZoneInfo("America/New_York"))

        # Calculate forward prayer times with ISNA (15° Isha)
        settings = UserSettings(method='isna')
        results = calculate_prayer_times(self.lat, self.lng, self.elev, self.date, settings)

        self.sunrise = results['times']['sunrise']
        self.maghrib = results['times']['maghrib']
        self.isha = results['times']['isha']

        # Calculate midday and sun data separately
        jd = julian_date(self.date)
        self.sun_data = sun_coordinates(jd)
        self.midday = midday_time_calc(self.date, self.lng, self.sun_data)

    def test_reverse_isha_isna_method(self):
        """Test that reversing ISNA Isha time gives ~15° angle."""
        result = reverse_isha_angle(
            self.isha, self.midday, self.lat, self.sun_data,
            self.sunrise, self.maghrib
        )

        # Should be close to 15° (ISNA method) - within 0.5°
        self.assertAlmostEqual(result['angle'], 15.0, places=0)
        self.assertEqual(result['method'], 'standard')
        self.assertTrue(result['valid'])

    def test_reverse_isha_mwl_method(self):
        """Test that reversing MWL Isha time gives ~17° angle."""
        # Calculate with MWL (17° Isha)
        settings = UserSettings(method='mwl')
        results = calculate_prayer_times(self.lat, self.lng, self.elev, self.date, settings)
        isha_mwl = results['times']['isha']

        result = reverse_isha_angle(
            isha_mwl, self.midday, self.lat, self.sun_data,
            self.sunrise, self.maghrib
        )

        # Should be close to 17° (MWL method) - within 0.5°
        self.assertAlmostEqual(result['angle'], 17.0, places=0)

    def test_isha_before_maghrib_raises_error(self):
        """Test that Isha before Maghrib raises ValueError."""
        invalid_isha = self.maghrib - timedelta(hours=1)

        with self.assertRaises(ValueError) as context:
            reverse_isha_angle(
                invalid_isha, self.midday, self.lat, self.sun_data,
                self.sunrise, self.maghrib
            )

        self.assertIn("not after Maghrib", str(context.exception))


class TestCalculateIshaMinutes(unittest.TestCase):
    """Tests for calculate_isha_minutes function."""

    def test_90_minutes(self):
        """Test 90 minutes after Maghrib (UQU standard)."""
        maghrib = datetime(2025, 1, 1, 17, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        isha = maghrib + timedelta(minutes=90)

        minutes = calculate_isha_minutes(isha, maghrib)

        self.assertEqual(minutes, 90.0)

    def test_120_minutes(self):
        """Test 120 minutes after Maghrib (UQU Ramadan)."""
        maghrib = datetime(2025, 1, 1, 17, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        isha = maghrib + timedelta(minutes=120)

        minutes = calculate_isha_minutes(isha, maghrib)

        self.assertEqual(minutes, 120.0)

    def test_fractional_minutes(self):
        """Test fractional minutes."""
        maghrib = datetime(2025, 1, 1, 17, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        isha = maghrib + timedelta(minutes=85, seconds=30)

        minutes = calculate_isha_minutes(isha, maghrib)

        self.assertAlmostEqual(minutes, 85.5, places=1)

    def test_isha_before_maghrib_raises_error(self):
        """Test that Isha before Maghrib raises ValueError."""
        maghrib = datetime(2025, 1, 1, 17, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        isha = maghrib - timedelta(minutes=30)

        with self.assertRaises(ValueError):
            calculate_isha_minutes(isha, maghrib)


class TestValidationFunctions(unittest.TestCase):
    """Tests for validation helper functions."""

    def test_validate_prayer_time_sequence_valid(self):
        """Test that valid sequence passes."""
        fajr = datetime(2025, 1, 1, 5, 30, tzinfo=ZoneInfo("America/New_York"))
        sunrise = datetime(2025, 1, 1, 7, 20, tzinfo=ZoneInfo("America/New_York"))
        maghrib = datetime(2025, 1, 1, 16, 45, tzinfo=ZoneInfo("America/New_York"))
        isha = datetime(2025, 1, 1, 18, 15, tzinfo=ZoneInfo("America/New_York"))

        # Should not raise
        validate_prayer_time_sequence(fajr, sunrise, maghrib, isha)

    def test_validate_prayer_time_sequence_invalid(self):
        """Test that invalid sequence raises ValueError."""
        fajr = datetime(2025, 1, 1, 8, 30, tzinfo=ZoneInfo("America/New_York"))  # After sunrise!
        sunrise = datetime(2025, 1, 1, 7, 20, tzinfo=ZoneInfo("America/New_York"))
        maghrib = datetime(2025, 1, 1, 16, 45, tzinfo=ZoneInfo("America/New_York"))
        isha = datetime(2025, 1, 1, 18, 15, tzinfo=ZoneInfo("America/New_York"))

        with self.assertRaises(ValueError):
            validate_prayer_time_sequence(fajr, sunrise, maghrib, isha)

    def test_validate_angle_range_valid(self):
        """Test that valid angle returns no warnings."""
        warnings = validate_angle_range(15.0, "Fajr")
        self.assertEqual(len(warnings), 0)

    def test_validate_angle_range_invalid(self):
        """Test that invalid angle returns warnings."""
        warnings = validate_angle_range(35.0, "Fajr")
        self.assertGreater(len(warnings), 0)


class TestReversePrayerCalculator(unittest.TestCase):
    """Tests for ReversePrayerCalculator class."""

    def setUp(self):
        """Set up test data."""
        self.lat = 40.7128
        self.lng = -74.0060
        self.elev = 10
        self.date = datetime(2025, 1, 1, tzinfo=ZoneInfo("America/New_York"))

    def test_reverse_calculator_initialization(self):
        """Test that calculator initializes correctly."""
        calc = ReversePrayerCalculator(self.lat, self.lng, self.elev)

        self.assertEqual(calc.latitude, self.lat)
        self.assertEqual(calc.longitude, self.lng)
        self.assertEqual(calc.elevation, self.elev)

    def test_reverse_calculate_isna(self):
        """Test full reverse calculation with ISNA times."""
        # First, calculate forward with ISNA
        settings = UserSettings(method='isna')
        forward_results = calculate_prayer_times(
            self.lat, self.lng, self.elev, self.date, settings
        )

        # Extract observed times
        fajr_time = forward_results['times']['fajr']
        maghrib_time = forward_results['times']['maghrib']
        isha_time = forward_results['times']['isha']

        # Now reverse calculate
        calc = ReversePrayerCalculator(self.lat, self.lng, self.elev)
        results = calc.reverse_calculate(self.date, fajr_time, maghrib_time, isha_time)

        # Should get back ~15° for both (within 0.5°)
        self.assertAlmostEqual(results['fajr_angle'], 15.0, places=0)
        self.assertAlmostEqual(results['isha_angle'], 15.0, places=0)
        self.assertTrue(results['valid'])

    def test_reverse_calculate_with_invalid_sequence(self):
        """Test that invalid time sequence raises error."""
        fajr_time = datetime(2025, 1, 1, 8, 0, tzinfo=ZoneInfo("America/New_York"))
        maghrib_time = datetime(2025, 1, 1, 16, 45, tzinfo=ZoneInfo("America/New_York"))
        isha_time = datetime(2025, 1, 1, 18, 15, tzinfo=ZoneInfo("America/New_York"))

        calc = ReversePrayerCalculator(self.lat, self.lng, self.elev)

        with self.assertRaises(ValueError):
            calc.reverse_calculate(self.date, fajr_time, maghrib_time, isha_time)

    def test_reverse_calculate_returns_all_fields(self):
        """Test that reverse_calculate returns all expected fields."""
        settings = UserSettings(method='isna')
        forward_results = calculate_prayer_times(
            self.lat, self.lng, self.elev, self.date, settings
        )

        fajr_time = forward_results['times']['fajr']
        maghrib_time = forward_results['times']['maghrib']
        isha_time = forward_results['times']['isha']

        calc = ReversePrayerCalculator(self.lat, self.lng, self.elev)
        results = calc.reverse_calculate(self.date, fajr_time, maghrib_time, isha_time)

        # Check all expected keys exist
        expected_keys = [
            'fajr_angle', 'fajr_method', 'isha_angle', 'isha_method',
            'isha_minutes', 'midday', 'sunrise', 'astronomical_data',
            'warnings', 'high_latitude', 'valid'
        ]
        for key in expected_keys:
            self.assertIn(key, results, f"Missing key: {key}")


class TestRoundTrip(unittest.TestCase):
    """
    Critical tests: Forward → Reverse → Forward should produce same results.
    This is the gold standard for verifying correctness.
    """

    def test_round_trip_isna_new_york(self):
        """Test round trip with ISNA method in New York."""
        lat, lng, elev = 40.7128, -74.0060, 10
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo("America/New_York"))

        # Step 1: Forward calculation with ISNA
        settings_isna = UserSettings(method='isna')
        forward1 = calculate_prayer_times(lat, lng, elev, date, settings_isna)

        # Step 2: Reverse calculate to get angles
        calc = ReversePrayerCalculator(lat, lng, elev)
        reverse_results = calc.reverse_calculate(
            date,
            forward1['times']['fajr'],
            forward1['times']['maghrib'],
            forward1['times']['isha']
        )

        # Step 3: Forward calculate again with extracted angles
        settings_custom = UserSettings(
            method='isna',  # Base method
            fajr_angle=reverse_results['fajr_angle'],
            isha_angle=reverse_results['isha_angle']
        )
        forward2 = calculate_prayer_times(lat, lng, elev, date, settings_custom)

        # Step 4: Compare times (should match within 2 minutes)
        # Note: Allow 2 minutes tolerance due to rounding in time calculations
        fajr_diff = abs((forward1['times']['fajr'] - forward2['times']['fajr']).total_seconds())
        isha_diff = abs((forward1['times']['isha'] - forward2['times']['isha']).total_seconds())

        self.assertLessEqual(fajr_diff, 120, "Fajr times differ by more than 2 minutes")
        self.assertLessEqual(isha_diff, 120, "Isha times differ by more than 2 minutes")

    def test_round_trip_mwl_new_york(self):
        """Test round trip with MWL method in New York."""
        lat, lng, elev = 40.7128, -74.0060, 10
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo("America/New_York"))

        # Forward with MWL
        settings_mwl = UserSettings(method='mwl')
        forward1 = calculate_prayer_times(lat, lng, elev, date, settings_mwl)

        # Reverse
        calc = ReversePrayerCalculator(lat, lng, elev)
        reverse_results = calc.reverse_calculate(
            date,
            forward1['times']['fajr'],
            forward1['times']['maghrib'],
            forward1['times']['isha']
        )

        # Forward again with extracted angles
        settings_custom = UserSettings(
            method='mwl',
            fajr_angle=reverse_results['fajr_angle'],
            isha_angle=reverse_results['isha_angle']
        )
        forward2 = calculate_prayer_times(lat, lng, elev, date, settings_custom)

        # Compare (within 2 minutes tolerance)
        fajr_diff = abs((forward1['times']['fajr'] - forward2['times']['fajr']).total_seconds())
        isha_diff = abs((forward1['times']['isha'] - forward2['times']['isha']).total_seconds())

        self.assertLessEqual(fajr_diff, 120)
        self.assertLessEqual(isha_diff, 120)

    def test_round_trip_different_location(self):
        """Test round trip with different location (Dubai)."""
        lat, lng, elev = 25.2048, 55.2708, 10  # Dubai
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo("Asia/Dubai"))

        # Forward with ISNA
        settings = UserSettings(method='isna')
        forward1 = calculate_prayer_times(lat, lng, elev, date, settings)

        # Reverse
        calc = ReversePrayerCalculator(lat, lng, elev)
        reverse_results = calc.reverse_calculate(
            date,
            forward1['times']['fajr'],
            forward1['times']['maghrib'],
            forward1['times']['isha']
        )

        # Forward again
        settings_custom = UserSettings(
            method='isna',
            fajr_angle=reverse_results['fajr_angle'],
            isha_angle=reverse_results['isha_angle']
        )
        forward2 = calculate_prayer_times(lat, lng, elev, date, settings_custom)

        # Compare (within 2 minutes tolerance)
        fajr_diff = abs((forward1['times']['fajr'] - forward2['times']['fajr']).total_seconds())
        isha_diff = abs((forward1['times']['isha'] - forward2['times']['isha']).total_seconds())

        self.assertLessEqual(fajr_diff, 120)
        self.assertLessEqual(isha_diff, 120)


class TestConvenienceFunction(unittest.TestCase):
    """Tests for the convenience function."""

    def test_reverse_calculate_angles_function(self):
        """Test convenience function works."""
        lat, lng, elev = 40.7128, -74.0060, 10
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo("America/New_York"))

        # Get times from forward calculation
        settings = UserSettings(method='isna')
        forward = calculate_prayer_times(lat, lng, elev, date, settings)

        # Use convenience function
        results = reverse_calculate_angles(
            lat, lng, elev, date,
            forward['times']['fajr'],
            forward['times']['maghrib'],
            forward['times']['isha']
        )

        # Should get reasonable angles (within 0.5°)
        self.assertAlmostEqual(results['fajr_angle'], 15.0, places=0)
        self.assertAlmostEqual(results['isha_angle'], 15.0, places=0)


if __name__ == '__main__':
    unittest.main()
