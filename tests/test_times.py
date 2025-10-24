"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Tests for prayer time calculation functions.

This module tests the individual prayer time calculation functions including:
Fajr, Sunrise, Dhuhr, Asr, Maghrib, and Isha.

Author: Omar Younis
Date: 23/10/2025 [dd/mm/yyyy]
"""

import unittest
from datetime import datetime
from prayer_times.calculator.times import (
    _hour_correction,
    midday_time_calc,
    dhuhr_time_calc,
    fajr_time_calc,
    sunrise_time_calc,
    asr_time_calc,
    maghrib_time_calc,
    isha_time_calc
)
from prayer_times.core.astronomy import sun_coordinates
from prayer_times.core.calendar import julian_date


class TestHourCorrection(unittest.TestCase):
    """
    Tests the _hour_correction helper function.
    """

    def setUp(self):
        """Sets up test data used across multiple tests."""
        # Use J2000.0 epoch for consistent sun data
        jd = 2451545.0
        self.sun_data = sun_coordinates(jd)
        self.latitude = 40.7128  # New York

    def test_different_angles_produce_different_offsets(self):
        """Tests that different angles produce different hour offsets."""
        theta1 = 90.0  # Horizon
        theta2 = 96.0  # Below horizon (twilight)

        offset1 = _hour_correction(theta1, self.latitude, self.sun_data)
        offset2 = _hour_correction(theta2, self.latitude, self.sun_data)

        # Different angles should produce different offsets
        self.assertNotEqual(offset1, offset2)

        # Greater angles should give larger offsets
        self.assertGreater(offset2, offset1)

    def test_returns_positive_hours(self):
        """Tests that hour correction returns positive values."""
        theta = 90.0
        hour_offset = _hour_correction(theta, self.latitude, self.sun_data)

        # Should return a positive number of hours that is less than half a day
        self.assertGreater(hour_offset, 0)
        self.assertLess(hour_offset, 12)


class TestMiddayTimeCalc(unittest.TestCase):
    """
    Tests the midday_time_calc function.
    """

    def test_midday_consistency_across_days(self):
        """
        Tests that the midday time is consistent across consecutive days.
        Should differ by less than 2 minutes due to equation of time.
        """
        lng = -74.0060

        # Calculates midday for two consecutive days
        date1 = datetime(2025, 3, 15)
        jd1 = julian_date(date1)
        sun_data1 = sun_coordinates(jd1)
        midday1 = midday_time_calc(date1, lng, sun_data1)

        date2 = datetime(2025, 3, 16)
        jd2 = julian_date(date2)
        sun_data2 = sun_coordinates(jd2)
        midday2 = midday_time_calc(date2, lng, sun_data2)

        # Time of day should be similar (within 2 minutes)
        time_diff = abs((midday2.hour * 60 + midday2.minute) -
                       (midday1.hour * 60 + midday1.minute))
        self.assertLess(time_diff, 2)

    def test_midday_returns_correct_date(self):
        """Tests that the midday calculation returns a time on the same date."""
        date = datetime(2025, 1, 1)
        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        lng = -74.0060

        midday = midday_time_calc(date, lng, sun_data)

        # Should be on the same day
        self.assertEqual(midday.date(), date.date())


class TestDhuhrTimeCalc(unittest.TestCase):
    """
    Tests the dhuhr_time_calc function.
    """

    def test_dhuhr_exactly_65_seconds_after_midday(self):
        """
        Tests that Dhuhr is exactly 65 seconds after midday.
        (Islamic jurisprudence: The Sun has passed its zenith.)
        """
        midday = datetime(2025, 1, 1, 12, 0, 0)
        dhuhr = dhuhr_time_calc(midday)

        # Should be exactly 65 seconds after midday
        diff = (dhuhr - midday).total_seconds()
        self.assertAlmostEqual(diff, 65.0, delta=0.01)


class TestSunriseTimeCalc(unittest.TestCase):
    """
    Tests the sunrise_time_calc function.
    """

    def test_sunrise_new_york_jan1_2025(self):
        """
        Tests the sunrise calculation for New York on Jan 1, 2025.
        Expected: 04:19:22
        """
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elevation = 10.0

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        sunrise = sunrise_time_calc(midday, lat, sun_data, elevation)

        # Verify calculated time
        expected_hour = 4
        expected_minute = 19

        self.assertEqual(sunrise.hour, expected_hour)
        self.assertAlmostEqual(sunrise.minute, expected_minute, delta=1)

    def test_sunrise_before_midday(self):
        """Tests that sunrise is always before midday."""
        date = datetime(2025, 1, 1)
        lat = 51.5074
        lng = -0.1278
        elevation = 50.0

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        sunrise = sunrise_time_calc(midday, lat, sun_data, elevation)

        # Sunrise must be before midday
        self.assertLess(sunrise, midday)

    def test_elevation_effect_on_sunrise(self):
        """Tests that the higher elevations causes an earlier sunrise.
        At 1000m elevation, sunrise should be about 9-10 minutes earlier
        than at sea level.
        """
        date = datetime(2025, 6, 21)
        lat = 51.5074
        lng = -0.1278

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)

        # Low elevation (sea level)
        sunrise_low = sunrise_time_calc(midday, lat, sun_data, 0)

        # High elevation (mountain at 1000m)
        sunrise_high = sunrise_time_calc(midday, lat, sun_data, 1000)

        # Higher elevation should have earlier sunrise
        self.assertLess(sunrise_high, sunrise_low)

        # Difference should be about 9-10 minutes (540-600 seconds)
        diff_seconds = (sunrise_low - sunrise_high).total_seconds()
        self.assertGreater(diff_seconds, 500)
        self.assertLess(diff_seconds, 650)


class TestAsrTimeCalc(unittest.TestCase):
    """
    Tests the asr_time_calc function.
    """

    def test_asr_standard_new_york_jan1_2025(self):
        """
        Tests the standard Asr calculation for New York on Jan 1, 2025.
        Expected: 11:21:04
        """
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        asr = asr_time_calc(midday, lat, sun_data, hanafi=False)

        # Verify calculated time
        expected_hour = 11
        expected_minute = 21

        self.assertEqual(asr.hour, expected_hour)
        self.assertAlmostEqual(asr.minute, expected_minute, delta=1)

    def test_asr_hanafi_later_than_standard(self):
        """
        Tests that Hanafi Asr is later than standard Asr.
        For New York on Jan 1, 2025, the difference should be about 37 minutes.
        """
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)

        asr_standard = asr_time_calc(midday, lat, sun_data, hanafi=False)
        asr_hanafi = asr_time_calc(midday, lat, sun_data, hanafi=True)

        # Hanafi should be later
        self.assertGreater(asr_hanafi, asr_standard)

        # Difference should be about 37 minutes
        diff_minutes = (asr_hanafi - asr_standard).total_seconds() / 60
        self.assertAlmostEqual(diff_minutes, 37.2, delta=2.0)

    def test_asr_after_dhuhr(self):
        """Tests that Asr is always after Dhuhr."""
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        dhuhr = dhuhr_time_calc(midday)
        asr = asr_time_calc(midday, lat, sun_data, hanafi=False)

        # Asr must be after Dhuhr
        self.assertGreater(asr, dhuhr)


class TestMaghribTimeCalc(unittest.TestCase):
    """
    Tests the maghrib_time_calc function.
    """

    def test_maghrib_new_york_jan1_2025(self):
        """
        Tests Maghrib calculation for New York on Jan 1, 2025.
        Expected: 13:39:34
        """
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elevation = 10.0

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        maghrib = maghrib_time_calc(midday, lat, sun_data, elevation)

        # Verify calculated time
        expected_hour = 13
        expected_minute = 39

        self.assertEqual(maghrib.hour, expected_hour)
        self.assertAlmostEqual(maghrib.minute, expected_minute, delta=1)

    def test_maghrib_after_midday(self):
        """Tests that Maghrib is always after midday."""
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elevation = 10.0

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        maghrib = maghrib_time_calc(midday, lat, sun_data, elevation)

        # Maghrib must be after midday
        self.assertGreater(maghrib, midday)

    def test_maghrib_roughly_symmetric_with_sunrise(self):
        """
        Tests that Maghrib and Sunrise are roughly symmetric around midday.
        Due to the equation of time, they won't be exactly symmetric, but
        should be within about 10 minutes.
        """
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elevation = 10.0

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        sunrise = sunrise_time_calc(midday, lat, sun_data, elevation)
        maghrib = maghrib_time_calc(midday, lat, sun_data, elevation)

        # Calculate time differences from midday
        sunrise_diff = (midday - sunrise).total_seconds()
        maghrib_diff = (maghrib - midday).total_seconds()

        # The difference should be within 10 minutes (600 seconds) of each other.
        self.assertAlmostEqual(sunrise_diff, maghrib_diff, delta=600)


class TestFajrTimeCalc(unittest.TestCase):
    """
    Tests the fajr_time_calc function.
    """

    def test_fajr_isna_new_york_jan1_2025(self):
        """
        Tests the ISNA Fajr calculation for New York on Jan 1, 2025.
        Expected: 02:58:09
        """
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elevation = 10.0

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        sunrise = sunrise_time_calc(midday, lat, sun_data, elevation)
        maghrib = maghrib_time_calc(midday, lat, sun_data, elevation)
        fajr = fajr_time_calc(midday, lat, sun_data, 'isna', sunrise, maghrib)

        # Verify calculated time
        expected_hour = 2
        expected_minute = 58

        self.assertEqual(fajr.hour, expected_hour)
        self.assertAlmostEqual(fajr.minute, expected_minute, delta=1)

    def test_fajr_before_sunrise(self):
        """Tests that Fajr is always before sunrise."""
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elevation = 10.0

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        sunrise = sunrise_time_calc(midday, lat, sun_data, elevation)
        maghrib = maghrib_time_calc(midday, lat, sun_data, elevation)
        fajr = fajr_time_calc(midday, lat, sun_data, 'isna', sunrise, maghrib)

        # Fajr must be before sunrise
        self.assertLess(fajr, sunrise)

    def test_fajr_different_methods(self):
        """
        Tests that different calculation methods give different Fajr times.
        MWL (18°) should be earlier than ISNA (15°).
        """
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elevation = 10.0

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        sunrise = sunrise_time_calc(midday, lat, sun_data, elevation)
        maghrib = maghrib_time_calc(midday, lat, sun_data, elevation)

        fajr_isna = fajr_time_calc(midday, lat, sun_data, 'isna', sunrise, maghrib)
        fajr_mwl = fajr_time_calc(midday, lat, sun_data, 'mwl', sunrise, maghrib)

        # Both should be before sunrise
        self.assertLess(fajr_isna, sunrise)
        self.assertLess(fajr_mwl, sunrise)

        # MWL should be earlier than ISNA
        self.assertLess(fajr_mwl, fajr_isna)


class TestIshaTimeCalc(unittest.TestCase):
    """
    Tests the isha_time_calc function.
    """

    def test_isha_isna_new_york_jan1_2025(self):
        """
        Tests the ISNA Isha calculation for New York on Jan 1, 2025.
        Expected: 15:00:47
        """
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elevation = 10.0

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        sunrise = sunrise_time_calc(midday, lat, sun_data, elevation)
        maghrib = maghrib_time_calc(midday, lat, sun_data, elevation)
        isha = isha_time_calc(midday, lat, sun_data, 'isna', maghrib, sunrise, ramadan=False)

        # Verify calculated time
        expected_hour = 15
        expected_minute = 0

        self.assertEqual(isha.hour, expected_hour)
        self.assertAlmostEqual(isha.minute, expected_minute, delta=1)

    def test_isha_after_maghrib(self):
        """Tests that Isha is always after Maghrib."""
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elevation = 10.0

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        sunrise = sunrise_time_calc(midday, lat, sun_data, elevation)
        maghrib = maghrib_time_calc(midday, lat, sun_data, elevation)
        isha = isha_time_calc(midday, lat, sun_data, 'isna', maghrib, sunrise, ramadan=False)

        # Isha must be after Maghrib
        self.assertGreater(isha, maghrib)

    def test_isha_uqu_ramadan_30_minutes_later(self):
        """
        Tests that the UQU method adds exactly 30 minutes more during Ramadan
        over the regular day.
        
        Normal: 90 minutes after Maghrib
        Ramadan: 120 minutes after Maghrib
        
        Difference: exactly 30 minutes
        """
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elevation = 10.0

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        sunrise = sunrise_time_calc(midday, lat, sun_data, elevation)
        maghrib = maghrib_time_calc(midday, lat, sun_data, elevation)

        # Non-Ramadan (90 minutes after Maghrib)
        isha_normal = isha_time_calc(midday, lat, sun_data, 'uqu',
                                     maghrib, sunrise, ramadan=False)

        # Ramadan (120 minutes after Maghrib)
        isha_ramadan = isha_time_calc(midday, lat, sun_data, 'uqu',
                                      maghrib, sunrise, ramadan=True)

        # Ramadan Isha should be exactly 30 minutes later than Non-Ramadan Isha
        diff_minutes = (isha_ramadan - isha_normal).total_seconds() / 60
        self.assertAlmostEqual(diff_minutes, 30.0, delta=0.01)

    def test_isha_different_methods(self):
        """Tests that different calculation methods give different Isha times."""
        date = datetime(2025, 1, 1)
        lat = 40.7128
        lng = -74.0060
        elevation = 10.0

        jd = julian_date(date)
        sun_data = sun_coordinates(jd)
        midday = midday_time_calc(date, lng, sun_data)
        sunrise = sunrise_time_calc(midday, lat, sun_data, elevation)
        maghrib = maghrib_time_calc(midday, lat, sun_data, elevation)

        # Angle-based method (ISNA: 15°)
        isha_isna = isha_time_calc(midday, lat, sun_data, 'isna',
                                   maghrib, sunrise, ramadan=False)

        # Angle-based method (MWL: 17°)
        isha_mwl = isha_time_calc(midday, lat, sun_data, 'mwl',
                                  maghrib, sunrise, ramadan=False)

        # Both should be after Maghrib
        self.assertGreater(isha_isna, maghrib)
        self.assertGreater(isha_mwl, maghrib)

        # Different methods should give different times
        self.assertNotEqual(isha_isna, isha_mwl)


class TestPrayerTimeSequence(unittest.TestCase):
    """
    Tests for the correct sequence of prayer times throughout the day.
    """

    def setUp(self):
        """Sets up a full day of prayer times for New York on Jan 1, 2025."""
        self.date = datetime(2025, 1, 1)
        self.jd = julian_date(self.date)
        self.sun_data = sun_coordinates(self.jd)
        self.lat = 40.7128
        self.lng = -74.0060
        self.elevation = 10.0

        # Calculates all times
        self.midday = midday_time_calc(self.date, self.lng, self.sun_data)
        self.sunrise = sunrise_time_calc(self.midday, self.lat,
                                         self.sun_data, self.elevation)
        self.dhuhr = dhuhr_time_calc(self.midday)
        self.asr = asr_time_calc(self.midday, self.lat, self.sun_data)
        self.maghrib = maghrib_time_calc(self.midday, self.lat,
                                         self.sun_data, self.elevation)
        self.fajr = fajr_time_calc(self.midday, self.lat, self.sun_data,
                                   'isna', self.sunrise, self.maghrib)
        self.isha = isha_time_calc(self.midday, self.lat, self.sun_data,
                                   'isna', self.maghrib, self.sunrise)

    def test_correct_chronological_sequence(self):
        """
        Tests that all prayer times are in correct order. The correct sequence
        is: Fajr < Sunrise < Dhuhr < Asr < Maghrib < Isha
        """
        self.assertLess(self.fajr, self.sunrise)
        self.assertLess(self.sunrise, self.dhuhr)
        self.assertLess(self.dhuhr, self.asr)
        self.assertLess(self.asr, self.maghrib)
        self.assertLess(self.maghrib, self.isha)

    def test_all_times_on_same_date(self):
        """Tests that all calculated prayer times are on the same date."""
        self.assertEqual(self.fajr.date(), self.date.date())
        self.assertEqual(self.sunrise.date(), self.date.date())
        self.assertEqual(self.dhuhr.date(), self.date.date())
        self.assertEqual(self.asr.date(), self.date.date())
        self.assertEqual(self.maghrib.date(), self.date.date())
        self.assertEqual(self.isha.date(), self.date.date())


if __name__ == '__main__':
    unittest.main()
