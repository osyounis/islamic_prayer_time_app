"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Tests for calendar conversion module.

This module tests Julian Day calculations and Hijri calendar conversions.

Author: Omar Younis
Date: 22/10/2025 [dd/mm/yyyy]
"""

import unittest
from datetime import datetime
from prayer_times.core.calendar import julian_date, hijri_date


class TestJulianDate(unittest.TestCase):
    """
    Tests for julian_date function.
    """

    def test_j2000_epoch(self):
        """Test J2000.0 epoch (January 1, 2000).
        This is a well-known reference point in astronomy.
        Note: julian_date function ignores time of day and returns midnight (.5).
        """
        date = datetime(2000, 1, 1)
        jd = julian_date(date)

        # J2000.0 reference is JD 2451545.0 (noon), but our function returns midnight
        self.assertAlmostEqual(jd, 2451544.5, delta=0.1)

    def test_unix_epoch(self):
        """Test Unix epoch (January 1, 1970).
        Known JD: 2440587.5
        """
        date = datetime(1970, 1, 1)
        jd = julian_date(date)

        self.assertAlmostEqual(jd, 2440587.5, delta=0.1)

    def test_hijri_epoch(self):
        """Test Islamic epoch (July 16, 622 AD).
        Known JD: 1948440
        """
        date = datetime(622, 7, 16)
        jd = julian_date(date)

        self.assertAlmostEqual(jd, 1948440.0, delta=1.0)

    def test_recent_date(self):
        """Test a recent date (January 1, 2025).
        Expected JD: 2460676.5
        """
        date = datetime(2025, 1, 1)
        jd = julian_date(date)

        # Test exact value
        self.assertAlmostEqual(jd, 2460676.5, delta=0.01)

    def test_leap_year(self):
        """Test February 29 on a leap year (2000).
        """
        date = datetime(2000, 2, 29)
        jd = julian_date(date)

        # Should be 59 days after Jan 1, 2000
        jd_jan1 = julian_date(datetime(2000, 1, 1))
        self.assertAlmostEqual(jd - jd_jan1, 59.0, delta=0.1)

    def test_sequential_dates(self):
        """Test that sequential dates increment JD by 1.
        """
        date1 = datetime(2025, 6, 1)
        date2 = datetime(2025, 6, 2)
        date3 = datetime(2025, 6, 3)

        jd1 = julian_date(date1)
        jd2 = julian_date(date2)
        jd3 = julian_date(date3)

        # Each day should increment JD by 1
        self.assertAlmostEqual(jd2 - jd1, 1.0, delta=0.01)
        self.assertAlmostEqual(jd3 - jd2, 1.0, delta=0.01)

    def test_month_adjustment(self):
        """Test that January and February are handled correctly.
        The algorithm treats Jan/Feb as months 13/14 of previous year internally,
        but should still produce correct JD values.
        """
        # Test January 15, 2025
        jan_date = datetime(2025, 1, 15)
        jd_jan = julian_date(jan_date)

        # Test February 15, 2025
        feb_date = datetime(2025, 2, 15)
        jd_feb = julian_date(feb_date)

        # Test March 15, 2025
        mar_date = datetime(2025, 3, 15)
        jd_mar = julian_date(mar_date)

        # Verify the differences are correct
        # Jan 15 to Feb 15 = 31 days (January has 31 days)
        self.assertAlmostEqual(jd_feb - jd_jan, 31.0, delta=0.01)

        # Feb 15 to Mar 15 = 28 days (February 2025 has 28 days - not a leap year)
        self.assertAlmostEqual(jd_mar - jd_feb, 28.0, delta=0.01)

        # Test the Dec-Jan boundary
        dec_date = datetime(2024, 12, 31)
        jan1_date = datetime(2025, 1, 1)

        jd_dec = julian_date(dec_date)
        jd_jan1 = julian_date(jan1_date)

        # Dec 31 to Jan 1 should be exactly 1 day
        self.assertAlmostEqual(jd_jan1 - jd_dec, 1.0, delta=0.01)


class TestHijriDate(unittest.TestCase):
    """
    Tests for hijri_date function.
    """

    def test_hijri_epoch(self):
        """Test the Islamic epoch (Muharram 1, 1 AH).
        Should correspond to July 16, 622 AD (JD 1948440).
        """
        jd = 1948440.0
        hijri = hijri_date(jd)

        self.assertEqual(hijri['day'], 1)
        self.assertEqual(hijri['month'], 1)
        self.assertEqual(hijri['year'], 1)

    def test_j2000_epoch(self):
        """Test J2000.0 epoch conversion to Hijri.
        January 1, 2000 AD (midnight) = Ramadan 23, 1420 AH
        """
        jd = 2451544.5  # Jan 1, 2000 (midnight)
        hijri = hijri_date(jd)

        # Test exact calculated values
        self.assertEqual(hijri['day'], 23)
        self.assertEqual(hijri['month'], 9)  # Ramadan
        self.assertEqual(hijri['year'], 1420)

    def test_recent_date(self):
        """Test a recent date conversion with known value.
        January 1, 2025 AD = Jumada Al-Thani 29, 1446 AH (calculated).
        """
        jd = 2460676.5  # Jan 1, 2025
        hijri = hijri_date(jd)

        # Test against the actual calculated value
        self.assertEqual(hijri['day'], 29)
        self.assertEqual(hijri['month'], 6)  # Jumada Al-Thani
        self.assertEqual(hijri['year'], 1446)

    def test_correction_factor(self):
        """Test that the correction factor adjusts dates properly.
        """
        jd = 2451544.5  # Jan 1, 2000

        # No correction
        hijri_0 = hijri_date(jd, d_correction=0)

        # +1 day correction
        hijri_plus1 = hijri_date(jd, d_correction=1)

        # -1 day correction
        hijri_minus1 = hijri_date(jd, d_correction=-1)

        # With +1 correction, day should increase by 1 (or wrap to next month)
        if hijri_plus1['month'] == hijri_0['month']:
            self.assertEqual(hijri_plus1['day'], hijri_0['day'] + 1)
        else:
            # Month wrapped
            self.assertEqual(hijri_plus1['day'], 1)
            self.assertEqual(hijri_plus1['month'], hijri_0['month'] + 1)

        # With -1 correction, day should decrease by 1 (or wrap to previous month)
        if hijri_minus1['month'] == hijri_0['month']:
            self.assertEqual(hijri_minus1['day'], hijri_0['day'] - 1)
        else:
            # Month wrapped backwards
            self.assertTrue(hijri_minus1['day'] >= 29)  # Last few days of previous month

    def test_year_progression(self):
        """Test that Hijri years progress correctly over time.
        Hijri year should increase by about 1.03 for each Gregorian year.
        """
        jd_2000 = 2451544.5  # Jan 1, 2000
        jd_2010 = 2455197.5  # Jan 1, 2010
        jd_2020 = 2458849.5  # Jan 1, 2020

        hijri_2000 = hijri_date(jd_2000)
        hijri_2010 = hijri_date(jd_2010)
        hijri_2020 = hijri_date(jd_2020)

        # From 2000 to 2010 (10 Gregorian years), should be ~10.3 Hijri years
        diff_2000_2010 = hijri_2010['year'] - hijri_2000['year']
        self.assertGreater(diff_2000_2010, 9)
        self.assertLess(diff_2000_2010, 12)

        # From 2010 to 2020 (10 Gregorian years)
        diff_2010_2020 = hijri_2020['year'] - hijri_2010['year']
        self.assertGreater(diff_2010_2020, 9)
        self.assertLess(diff_2010_2020, 12)

    def test_known_date_before_ramadan(self):
        """Test the day before Ramadan 2024.
        March 11, 2024 AD = Sha'ban 29, 1445 AH (calculated).
        """
        date = datetime(2024, 3, 11)
        jd = julian_date(date)
        hijri = hijri_date(jd)

        # Test exact calculated values
        self.assertEqual(hijri['day'], 29)
        self.assertEqual(hijri['month'], 8)  # Sha'ban (month before Ramadan)
        self.assertEqual(hijri['year'], 1445)


class TestSequentialConversion(unittest.TestCase):
    """
    Tests for sequential date conversions (consistency checks).
    """

    def test_sequential_days_same_month(self):
        """Test that sequential Gregorian dates in same Hijri month increment
        correctly.
        """
        # Start with Jan 1, 2025 (Jumada Al-Thani 29, 1446)
        jd1 = 2460676.5
        hijri1 = hijri_date(jd1)

        # Next day (Jan 2, 2025)
        jd2 = jd1 + 1
        hijri2 = hijri_date(jd2)

        # Should either be same month (day+1) or next month (day=1)
        if hijri2['month'] == hijri1['month']:
            # Same month - day should increment
            self.assertEqual(hijri2['day'], hijri1['day'] + 1)
        else:
            # Month changed - should be day 1 of next month
            self.assertEqual(hijri2['day'], 1)
            self.assertEqual(hijri2['month'], hijri1['month'] + 1)

    def test_month_length_validity(self):
        """Test that Hijri months have reasonable lengths (29 or 30 days).
        """
        # Start from the beginning of a Hijri month (Rajab 1, 1446)
        jd_start = 2460677.5  # Jan 2, 2025 = Rajab 1, 1446
        current_month = hijri_date(jd_start)['month']
        month_length = 0

        # Check up to 35 days (more than any month can be)
        for day_offset in range(35):
            jd = jd_start + day_offset
            hijri = hijri_date(jd)

            if hijri['month'] == current_month:
                month_length += 1
            else:
                # Month changed - check the length was valid
                self.assertIn(month_length, [29, 30],
                            f"Invalid month length: {month_length}")
                break

    def test_year_boundary(self):
        """Test conversion around Hijri year boundary.
        """
        # Find a date near end of Hijri year
        # Dhu al-Hijjah (month 12) should transition to Muharram (month 1)

        # Use a known date in late Hijri year
        # For example, we know Jan 1, 2025 is month 6, year 1446
        # So roughly 6 months later would be month 12, year 1446

        jd_mid_1446 = 2460676.5  # Jan 1, 2025 (month 6, year 1446)

        # Add approximately 6 months (180 days)
        jd_end_1446 = jd_mid_1446 + 180

        hijri = hijri_date(jd_end_1446)

        # Should be in year 1446 or 1447
        self.assertIn(hijri['year'], [1446, 1447])

        # If year 1446, month should be high (10-12)
        # If year 1447, month should be low (1-3)
        if hijri['year'] == 1446:
            self.assertGreaterEqual(hijri['month'], 10)
        else:  # year 1447
            self.assertLessEqual(hijri['month'], 3)


if __name__ == '__main__':
    unittest.main()
