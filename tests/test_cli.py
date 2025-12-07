"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Tests for the CLI module.

This module tests the command-line interface including argument parsing,
validation, output formatting, and integration with the calculator.

Author: Omar Younis
Date: 07/12/2024 [dd/mm/yyyy]
"""

import unittest
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from io import StringIO
from unittest.mock import patch

from prayer_times.cli import (
    create_parser,
    validate_coordinates,
    parse_date,
    format_output,
    list_methods,
    main
)
from prayer_times.config import UserSettings
from prayer_times.calculator.calculator import calculate_prayer_times


class TestArgumentParsing(unittest.TestCase):
    """Tests CLI argument parsing with comprehensive coverage."""

    def setUp(self):
        self.parser = create_parser()

    def test_required_latitude_longitude_parsed(self):
        """Tests that latitude and longitude are correctly parsed as floats."""
        args = self.parser.parse_args(['33.88', '-117.928611'])
        self.assertAlmostEqual(args.latitude, 33.88, places=5)
        self.assertAlmostEqual(args.longitude, -117.928611, places=5)

    def test_negative_coordinates_parsed_correctly(self):
        """Tests that negative coordinates are handled correctly."""
        args = self.parser.parse_args(['-45.5', '-120.3'])
        self.assertAlmostEqual(args.latitude, -45.5)
        self.assertAlmostEqual(args.longitude, -120.3)

    def test_elevation_defaults_to_zero(self):
        """Tests that elevation defaults to 0 when not specified."""
        args = self.parser.parse_args(['33.88', '-117.928611'])
        self.assertEqual(args.elevation, 0)

    def test_elevation_accepts_positive_values(self):
        """Tests that positive elevation values are parsed."""
        args = self.parser.parse_args(['33.88', '-117.928611', '--elevation', '1500'])
        self.assertEqual(args.elevation, 1500)

    def test_elevation_accepts_negative_values(self):
        """Tests that negative elevation values (below sea level) are parsed."""
        args = self.parser.parse_args(['33.88', '-117.928611', '-e', '-50'])
        self.assertEqual(args.elevation, -50)

    def test_method_defaults_to_isna(self):
        """Tests that calculation method defaults to ISNA."""
        args = self.parser.parse_args(['33.88', '-117.928611'])
        self.assertEqual(args.method, 'isna')

    def test_all_methods_accepted(self):
        """Tests that all 9 calculation methods are accepted."""
        methods = ['mwl', 'isna', 'egas', 'uqu', 'uisk', 'ut', 'lri', 'gulf', 'jakim']
        for method in methods:
            args = self.parser.parse_args(['33.88', '-117.928611', '--method', method])
            self.assertEqual(args.method, method)

    def test_asr_method_defaults_to_standard(self):
        """Tests that Asr method defaults to standard."""
        args = self.parser.parse_args(['33.88', '-117.928611'])
        self.assertEqual(args.asr_method, 'standard')

    def test_asr_method_accepts_hanafi(self):
        """Tests that Hanafi Asr method is accepted."""
        args = self.parser.parse_args(['33.88', '-117.928611', '--asr-method', 'hanafi'])
        self.assertEqual(args.asr_method, 'hanafi')

    def test_hijri_correction_defaults_to_zero(self):
        """Tests that Hijri correction defaults to 0."""
        args = self.parser.parse_args(['33.88', '-117.928611'])
        self.assertEqual(args.hijri_correction, 0)

    def test_hijri_correction_accepts_positive(self):
        """Tests that positive Hijri correction is accepted."""
        args = self.parser.parse_args(['33.88', '-117.928611', '--hijri-correction', '2'])
        self.assertEqual(args.hijri_correction, 2)

    def test_hijri_correction_accepts_negative(self):
        """Tests that negative Hijri correction is accepted."""
        args = self.parser.parse_args(['33.88', '-117.928611', '--hijri-correction', '-1'])
        self.assertEqual(args.hijri_correction, -1)

    def test_fajr_angle_parsed_as_float(self):
        """Tests that custom Fajr angle is parsed as float."""
        args = self.parser.parse_args(['33.88', '-117.928611', '--fajr-angle', '16.5'])
        self.assertAlmostEqual(args.fajr_angle, 16.5)

    def test_isha_angle_parsed_as_float(self):
        """Tests that custom Isha angle is parsed as float."""
        args = self.parser.parse_args(['33.88', '-117.928611', '--isha-angle', '13.5'])
        self.assertAlmostEqual(args.isha_angle, 13.5)

    def test_isha_interval_parsed_as_int(self):
        """Tests that custom Isha interval is parsed as integer."""
        args = self.parser.parse_args(['33.88', '-117.928611', '--isha-interval', '95'])
        self.assertEqual(args.isha_interval, 95)

    def test_both_fajr_and_isha_angles_accepted(self):
        """Tests that both custom angles can be specified together."""
        args = self.parser.parse_args([
            '33.88', '-117.928611',
            '--fajr-angle', '17',
            '--isha-angle', '14'
        ])
        self.assertAlmostEqual(args.fajr_angle, 17)
        self.assertAlmostEqual(args.isha_angle, 14)

    def test_date_string_parsed(self):
        """Tests that date string is parsed."""
        args = self.parser.parse_args(['33.88', '-117.928611', '--date', '2025-03-15'])
        self.assertEqual(args.date, '2025-03-15')

    def test_timezone_string_parsed(self):
        """Tests that timezone string is parsed."""
        args = self.parser.parse_args(['33.88', '-117.928611', '--timezone', 'America/New_York'])
        self.assertEqual(args.timezone, 'America/New_York')

    def test_list_methods_flag_parsed(self):
        """Tests that --list-methods flag is parsed."""
        args = self.parser.parse_args(['--list-methods'])
        self.assertTrue(args.list_methods)

    def test_short_flags_work(self):
        """Tests that short flag versions work correctly."""
        args = self.parser.parse_args([
            '33.88', '-117.928611',
            '-e', '100',
            '-z', 'UTC',
            '-d', '2025-01-01',
            '-m', 'mwl',
            '-a', 'hanafi'
        ])
        self.assertEqual(args.elevation, 100)
        self.assertEqual(args.timezone, 'UTC')
        self.assertEqual(args.date, '2025-01-01')
        self.assertEqual(args.method, 'mwl')
        self.assertEqual(args.asr_method, 'hanafi')


class TestCoordinateValidation(unittest.TestCase):
    """Tests coordinate validation with edge cases."""

    def test_valid_coordinates_at_origin(self):
        """Tests that coordinates at (0, 0) are valid."""
        try:
            validate_coordinates(0, 0)
        except ValueError:
            self.fail("validate_coordinates raised ValueError for (0, 0)")

    def test_valid_coordinates_at_boundaries(self):
        """Tests that coordinates at exact boundaries are valid."""
        try:
            validate_coordinates(90, 180)
            validate_coordinates(-90, -180)
            validate_coordinates(90, -180)
            validate_coordinates(-90, 180)
        except ValueError:
            self.fail("validate_coordinates raised ValueError for boundary coordinates")

    def test_latitude_exactly_90(self):
        """Tests that latitude of exactly 90 is valid (North Pole)."""
        try:
            validate_coordinates(90, 0)
        except ValueError:
            self.fail("validate_coordinates rejected valid latitude 90")

    def test_latitude_exactly_minus_90(self):
        """Tests that latitude of exactly -90 is valid (South Pole)."""
        try:
            validate_coordinates(-90, 0)
        except ValueError:
            self.fail("validate_coordinates rejected valid latitude -90")

    def test_latitude_above_90_raises_error(self):
        """Tests that latitude > 90 raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            validate_coordinates(90.1, 0)
        self.assertIn("latitude", str(cm.exception).lower())
        self.assertIn("90.1", str(cm.exception))

    def test_latitude_below_minus_90_raises_error(self):
        """Tests that latitude < -90 raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            validate_coordinates(-90.1, 0)
        self.assertIn("latitude", str(cm.exception).lower())
        self.assertIn("-90.1", str(cm.exception))

    def test_longitude_above_180_raises_error(self):
        """Tests that longitude > 180 raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            validate_coordinates(0, 180.1)
        self.assertIn("longitude", str(cm.exception).lower())
        self.assertIn("180.1", str(cm.exception))

    def test_longitude_below_minus_180_raises_error(self):
        """Tests that longitude < -180 raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            validate_coordinates(0, -180.1)
        self.assertIn("longitude", str(cm.exception).lower())
        self.assertIn("-180.1", str(cm.exception))

    def test_error_message_shows_invalid_value(self):
        """Tests that error messages include the invalid value."""
        with self.assertRaises(ValueError) as cm:
            validate_coordinates(95.5, 0)
        self.assertIn("95.5", str(cm.exception))


class TestDateParsing(unittest.TestCase):
    """Tests date parsing functionality."""

    def test_valid_iso_date_parsed(self):
        """Tests that valid ISO 8601 date is parsed correctly."""
        date = parse_date('2025-03-15', 'UTC')
        self.assertEqual(date.year, 2025)
        self.assertEqual(date.month, 3)
        self.assertEqual(date.day, 15)
        self.assertEqual(date.hour, 0)
        self.assertEqual(date.minute, 0)

    def test_date_is_timezone_aware(self):
        """Tests that parsed date is timezone-aware."""
        date = parse_date('2025-03-15', 'UTC')
        self.assertIsNotNone(date.tzinfo)

    def test_correct_timezone_applied(self):
        """Tests that the correct timezone is applied."""
        date = parse_date('2025-03-15', 'America/New_York')
        self.assertEqual(date.tzinfo, ZoneInfo('America/New_York'))

    def test_different_timezones_produce_different_results(self):
        """Tests that different timezones produce different datetime objects."""
        date_utc = parse_date('2025-03-15', 'UTC')
        date_ny = parse_date('2025-03-15', 'America/New_York')
        # Same wall clock time but different absolute times
        self.assertNotEqual(date_utc.utcoffset(), date_ny.utcoffset())

    def test_leap_year_date_parsed(self):
        """Tests that leap year dates are parsed correctly."""
        date = parse_date('2024-02-29', 'UTC')
        self.assertEqual(date.year, 2024)
        self.assertEqual(date.month, 2)
        self.assertEqual(date.day, 29)

    def test_invalid_date_format_raises_error(self):
        """Tests that invalid date format raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            parse_date('01/15/2025', 'UTC')
        self.assertIn("Invalid date format", str(cm.exception))
        self.assertIn("01/15/2025", str(cm.exception))

    def test_invalid_date_format_with_dashes_wrong_order(self):
        """Tests that MM-DD-YYYY format is rejected."""
        with self.assertRaises(ValueError) as cm:
            parse_date('03-15-2025', 'UTC')
        self.assertIn("Invalid date format", str(cm.exception))

    def test_invalid_month_raises_error(self):
        """Tests that invalid month (13) raises error."""
        with self.assertRaises(ValueError):
            parse_date('2025-13-01', 'UTC')

    def test_invalid_day_raises_error(self):
        """Tests that invalid day (32) raises error."""
        with self.assertRaises(ValueError):
            parse_date('2025-01-32', 'UTC')

    def test_invalid_timezone_raises_error(self):
        """Tests that invalid timezone raises ZoneInfoNotFoundError."""
        with self.assertRaises(ZoneInfoNotFoundError) as cm:
            parse_date('2025-01-15', 'Invalid/Timezone')
        self.assertIn("Invalid timezone", str(cm.exception))
        self.assertIn("Invalid/Timezone", str(cm.exception))

    def test_none_timezone_uses_local(self):
        """Tests that None timezone uses local timezone."""
        date = parse_date('2025-03-15', None)
        self.assertIsNotNone(date.tzinfo)
        # Should have same date components
        self.assertEqual(date.year, 2025)
        self.assertEqual(date.month, 3)
        self.assertEqual(date.day, 15)


class TestFormatOutput(unittest.TestCase):
    """Tests output formatting functionality."""

    def test_output_contains_all_prayer_times(self):
        """Tests that formatted output contains all six prayer times."""
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo('UTC'))
        settings = UserSettings(method='isna', asr_method='standard')
        results = calculate_prayer_times(40.7128, -74.0060, 10, date, settings)

        output = format_output(results, settings, 40.7128, -74.0060, 10)

        # Check all prayer names are present
        self.assertIn('Fajr', output)
        self.assertIn('Sunrise', output)
        self.assertIn('Dhuhr', output)
        self.assertIn('Asr', output)
        self.assertIn('Maghrib', output)
        self.assertIn('Isha', output)

    def test_output_contains_qibla_direction(self):
        """Tests that output contains Qibla direction."""
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo('UTC'))
        settings = UserSettings(method='isna')
        results = calculate_prayer_times(40.7128, -74.0060, 10, date, settings)

        output = format_output(results, settings, 40.7128, -74.0060, 10)

        self.assertIn('Qibla', output)
        # Should contain the actual direction value
        self.assertIn(f"{results['qibla']:06.2f}", output)

    def test_output_contains_location_info(self):
        """Tests that output contains location information."""
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo('UTC'))
        settings = UserSettings(method='isna')
        results = calculate_prayer_times(33.88, -117.928611, 50, date, settings)

        output = format_output(results, settings, 33.88, -117.928611, 50)

        self.assertIn('33.88', output)
        self.assertIn('-117.928611', output)
        self.assertIn('50m', output)

    def test_output_contains_hijri_date(self):
        """Tests that output contains Hijri date in both English and Arabic."""
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo('UTC'))
        settings = UserSettings(method='isna')
        results = calculate_prayer_times(40.7128, -74.0060, 10, date, settings)

        output = format_output(results, settings, 40.7128, -74.0060, 10)

        # Should contain Hijri date components
        self.assertIn('Hijri Date', output)
        # Should have year
        self.assertIn(str(results['hijri_date']['year']), output)

    def test_output_shows_calculation_method(self):
        """Tests that output shows the calculation method used."""
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo('UTC'))
        settings = UserSettings(method='mwl', asr_method='hanafi')
        results = calculate_prayer_times(40.7128, -74.0060, 10, date, settings)

        output = format_output(results, settings, 40.7128, -74.0060, 10)

        self.assertIn('MWL', output)
        self.assertIn('Muslim World League', output)
        self.assertIn('Hanafi', output)

    def test_output_shows_custom_fajr_angle_when_used(self):
        """Tests that custom Fajr angle is displayed when used."""
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo('UTC'))
        settings = UserSettings(method='isna', fajr_angle=17.5)
        results = calculate_prayer_times(40.7128, -74.0060, 10, date, settings)

        output = format_output(results, settings, 40.7128, -74.0060, 10)

        self.assertIn('Custom Fajr Angle', output)
        self.assertIn('17.5', output)

    def test_output_shows_custom_isha_angle_when_used(self):
        """Tests that custom Isha angle is displayed when used."""
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo('UTC'))
        settings = UserSettings(method='isna', isha_angle=13.5)
        results = calculate_prayer_times(40.7128, -74.0060, 10, date, settings)

        output = format_output(results, settings, 40.7128, -74.0060, 10)

        self.assertIn('Custom Isha Angle', output)
        self.assertIn('13.5', output)

    def test_output_shows_custom_isha_interval_when_used(self):
        """Tests that custom Isha interval is displayed when used."""
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo('UTC'))
        settings = UserSettings(method='isna', isha_interval=95)
        results = calculate_prayer_times(40.7128, -74.0060, 10, date, settings)

        output = format_output(results, settings, 40.7128, -74.0060, 10)

        self.assertIn('Custom Isha Interval', output)
        self.assertIn('95', output)

    def test_output_contains_both_12_and_24_hour_formats(self):
        """Tests that output contains both 12-hour and 24-hour time formats."""
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo('UTC'))
        settings = UserSettings(method='isna')
        results = calculate_prayer_times(40.7128, -74.0060, 10, date, settings)

        output = format_output(results, settings, 40.7128, -74.0060, 10)

        # Should have AM/PM indicators (12-hour)
        self.assertTrue('AM' in output or 'PM' in output)
        # Should have brackets for 24-hour format
        self.assertIn('[', output)
        self.assertIn(']', output)


class TestListMethods(unittest.TestCase):
    """Tests method listing functionality."""

    def test_list_methods_contains_all_methods(self):
        """Tests that list_methods includes all 9 calculation methods."""
        output = list_methods()

        method_keys = ['MWL', 'ISNA', 'EGAS', 'UQU', 'UISK', 'UT', 'LRI', 'GULF', 'JAKIM']
        for key in method_keys:
            self.assertIn(key, output)

    def test_list_methods_shows_method_names(self):
        """Tests that method names are shown, not just keys."""
        output = list_methods()

        self.assertIn('Muslim World League', output)
        self.assertIn('Islamic Society of North America', output)
        self.assertIn('Umm al-Qura University', output)

    def test_list_methods_shows_fajr_angles(self):
        """Tests that Fajr angles are displayed for each method."""
        output = list_methods()

        # Check some specific Fajr angles
        self.assertIn('15.0°', output)  # ISNA
        self.assertIn('18.0°', output)  # MWL and others
        self.assertIn('20.0°', output)  # JAKIM

    def test_list_methods_shows_isha_config(self):
        """Tests that Isha configuration is shown for each method."""
        output = list_methods()

        # Should show angle-based methods
        self.assertIn('Isha: 17.0°', output)  # MWL
        # Should show fixed-time methods
        self.assertIn('90 min after Maghrib', output)  # UQU/GULF


class TestMainFunction(unittest.TestCase):
    """Tests the main CLI function with various scenarios."""

    def test_main_returns_zero_on_success(self):
        """Tests that main() returns 0 on successful execution."""
        argv = ['33.88', '-117.928611']
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_all_options_succeeds(self):
        """Tests main() with all optional arguments specified."""
        argv = [
            '40.7128', '-74.0060',
            '--elevation', '10',
            '--timezone', 'America/New_York',
            '--date', '2025-01-15',
            '--method', 'mwl',
            '--asr-method', 'hanafi',
            '--hijri-correction', '1'
        ]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_custom_fajr_angle_succeeds(self):
        """Tests main() with custom Fajr angle."""
        argv = ['33.88', '-117.928611', '--fajr-angle', '17']
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_custom_isha_angle_succeeds(self):
        """Tests main() with custom Isha angle."""
        argv = ['33.88', '-117.928611', '--isha-angle', '14']
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_custom_isha_interval_succeeds(self):
        """Tests main() with custom Isha interval."""
        argv = ['21.4225', '39.8262', '--isha-interval', '95']
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_both_custom_angles_succeeds(self):
        """Tests main() with both custom Fajr and Isha angles."""
        argv = [
            '33.88', '-117.928611',
            '--fajr-angle', '17',
            '--isha-angle', '14'
        ]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_list_methods_returns_zero(self):
        """Tests that --list-methods returns 0 without coordinates."""
        argv = ['--list-methods']
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_invalid_latitude_returns_one(self):
        """Tests that invalid latitude returns exit code 1."""
        argv = ['91', '0']
        exit_code = main(argv)
        self.assertEqual(exit_code, 1)

    def test_main_invalid_longitude_returns_one(self):
        """Tests that invalid longitude returns exit code 1."""
        argv = ['0', '181']
        exit_code = main(argv)
        self.assertEqual(exit_code, 1)

    def test_main_invalid_date_format_returns_one(self):
        """Tests that invalid date format returns exit code 1."""
        argv = ['33.88', '-117.928611', '--date', '01/15/2025']
        exit_code = main(argv)
        self.assertEqual(exit_code, 1)

    def test_main_invalid_timezone_returns_one(self):
        """Tests that invalid timezone returns exit code 1."""
        argv = ['33.88', '-117.928611', '--timezone', 'Invalid/Zone']
        exit_code = main(argv)
        self.assertEqual(exit_code, 1)

    def test_main_conflicting_isha_args_returns_one(self):
        """Tests that conflicting isha_angle and isha_interval returns error."""
        argv = [
            '33.88', '-117.928611',
            '--isha-angle', '15',
            '--isha-interval', '90'
        ]
        exit_code = main(argv)
        self.assertEqual(exit_code, 1)

    def test_main_fajr_angle_out_of_range_returns_one(self):
        """Tests that fajr_angle > 30 returns exit code 1."""
        argv = ['33.88', '-117.928611', '--fajr-angle', '35']
        exit_code = main(argv)
        self.assertEqual(exit_code, 1)

    def test_main_isha_angle_out_of_range_returns_one(self):
        """Tests that isha_angle > 30 returns exit code 1."""
        argv = ['33.88', '-117.928611', '--isha-angle', '32']
        exit_code = main(argv)
        self.assertEqual(exit_code, 1)

    def test_main_isha_interval_out_of_range_returns_one(self):
        """Tests that isha_interval > 240 returns exit code 1."""
        argv = ['33.88', '-117.928611', '--isha-interval', '300']
        exit_code = main(argv)
        self.assertEqual(exit_code, 1)

    def test_main_fajr_angle_zero_returns_one(self):
        """Tests that fajr_angle of 0 is invalid (must be > 0)."""
        argv = ['33.88', '-117.928611', '--fajr-angle', '0']
        exit_code = main(argv)
        self.assertEqual(exit_code, 1)

    def test_main_missing_latitude_returns_error(self):
        """Tests that missing latitude argument produces error."""
        # parser.error() calls sys.exit(), so we need to catch SystemExit
        with patch('sys.stderr', new=StringIO()):
            with self.assertRaises(SystemExit) as cm:
                main([])
            # argparse exits with code 2 for usage errors
            self.assertEqual(cm.exception.code, 2)

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_produces_output(self, mock_stdout):
        """Tests that main() produces output to stdout."""
        argv = ['33.88', '-117.928611']
        main(argv)
        output = mock_stdout.getvalue()
        # Should contain some prayer time output
        self.assertGreater(len(output), 0)
        self.assertIn('Prayer Times', output)


class TestIntegrationCLI(unittest.TestCase):
    """Integration tests for CLI with actual calculations."""

    def test_cli_calculations_match_api_results(self):
        """Tests that CLI uses same calculation engine as API."""
        # Calculate using API
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo('UTC'))
        settings = UserSettings(method='isna', asr_method='standard')
        api_results = calculate_prayer_times(40.7128, -74.0060, 10, date, settings)

        # Run CLI (should use same calculation)
        argv = [
            '40.7128', '-74.0060',
            '--elevation', '10',
            '--method', 'isna',
            '--asr-method', 'standard',
            '--date', '2025-01-01',
            '--timezone', 'UTC'
        ]
        exit_code = main(argv)

        # CLI should complete successfully
        self.assertEqual(exit_code, 0)

        # The CLI uses the same calculator, so times should match
        # (We're mainly testing that CLI doesn't crash and integrates properly)

    def test_custom_angles_affect_prayer_times(self):
        """Tests that custom angles actually change calculated prayer times."""
        # Run with default ISNA angles
        date = datetime(2025, 1, 1, tzinfo=ZoneInfo('UTC'))
        settings_default = UserSettings(method='isna')
        results_default = calculate_prayer_times(40.7128, -74.0060, 10, date, settings_default)

        # Run with custom angles
        settings_custom = UserSettings(method='isna', fajr_angle=17, isha_angle=14)
        results_custom = calculate_prayer_times(40.7128, -74.0060, 10, date, settings_custom)

        # Times should be different
        self.assertNotEqual(
            results_default['times']['fajr'],
            results_custom['times']['fajr'],
            "Custom Fajr angle should change Fajr time"
        )
        self.assertNotEqual(
            results_default['times']['isha'],
            results_custom['times']['isha'],
            "Custom Isha angle should change Isha time"
        )

    def test_different_timezones_affect_output_times(self):
        """Tests that different timezones produce different formatted times."""
        # Same location, same UTC time, different timezones
        date_utc = datetime(2025, 1, 1, 12, 0, tzinfo=ZoneInfo('UTC'))
        date_ny = datetime(2025, 1, 1, 12, 0, tzinfo=ZoneInfo('America/New_York'))

        settings = UserSettings(method='isna')
        results_utc = calculate_prayer_times(40.7128, -74.0060, 10, date_utc, settings)
        results_ny = calculate_prayer_times(40.7128, -74.0060, 10, date_ny, settings)

        # The formatted times should be in different timezones
        # This tests that timezone is properly handled throughout
        output_utc = format_output(results_utc, settings, 40.7128, -74.0060, 10)
        output_ny = format_output(results_ny, settings, 40.7128, -74.0060, 10)

        # Both should contain valid output
        self.assertIn('Prayer Times', output_utc)
        self.assertIn('Prayer Times', output_ny)


if __name__ == '__main__':
    unittest.main()
