"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

This module tests the great circle bearing calculation used to find the Qibla
direction (the direction towards the Kaaba in Makkah).

Author: Omar Younis
Date: 23/10/2025 [dd/mm/yyyy format]

"""

import unittest
from prayer_times.core.qibla import qibla_direction
from prayer_times.config import LAT_AL_KAABA, LNG_AL_KAABA


class TestQiblaDirection(unittest.TestCase):
    """
    Tests the qibla_direction function.
    """

    def test_new_york_city(self) -> None:
        """
        Tests the Qibla direction from New York City. Expected value of 58.48°.
        """
        qibla = qibla_direction(40.7128, -74.0060)

        # Verifying value is in the right quadrant (NE)
        self.assertGreater(qibla, 0)
        self.assertLess(qibla, 90)

        # Testing exact value.
        self.assertAlmostEqual(qibla, 58.48, delta=0.01)

    def test_london_uk(self) -> None:
        """
        Tests the Qibla direction from London, UK. Expected value: about 119°.
        """
        qibla = qibla_direction(51.5074, -0.1278)

        # Verifying value is in the right quadrant (SE)
        self.assertGreater(qibla, 90)
        self.assertLess(qibla, 180)

        # Testing exact value.
        self.assertAlmostEqual(qibla, 118.99, delta=0.01)

    def test_tokyo_japan(self) -> None:
        """
        Tests the Qibla direction from Tokyo, Japan. Expected value: 293°.
        """
        qibla = qibla_direction(35.6762, 139.6503)

        # Verifying value is in the right quadrant (NW)
        self.assertGreater(qibla, 270)
        self.assertLess(qibla, 360)

        # Testing exact value.
        self.assertAlmostEqual(qibla, 293.00, delta=0.01)

    def test_sydney_australia(self) -> None:
        """
        Tests the Qibla direction from Sydney, Australia.
        Expected value: about 277.50°.
        """
        qibla = qibla_direction(-33.8688, 151.2093)

        # Verifying value is in the right quadrant (W-NW)
        self.assertGreater(qibla, 270)
        self.assertLess(qibla, 300)

        # Testing exact value.
        self.assertAlmostEqual(qibla, 277.50, delta=0.01)

    def test_cairo_egypt(self) -> None:
        """
        Tests the Qibla direction from Cairo, Egypt.
        Expected value: about 136.14°.
        """
        qibla = qibla_direction(30.0444, 31.2357)

        # Verifying value is in the right quadrant (SE)
        self.assertGreater(qibla, 120)
        self.assertLess(qibla, 150)

        # Testing exact value.
        self.assertAlmostEqual(qibla, 136.14, delta=0.01)

    def test_jakarta_indonesia(self) -> None:
        """
        Tests the Qibla direction from Jakarta, Indonesia.
        Expected value: about 295.15°.
        """
        qibla = qibla_direction(-6.2088, 106.8456)

        # Verifying value is in the right quadrant (NW)
        self.assertGreater(qibla, 290)
        self.assertLess(qibla, 300)

        # Testing exact value.
        self.assertAlmostEqual(qibla, 295.15, delta=0.01)

    def test_at_kaaba_location(self) -> None:
        """
        Tests the Qibla direction calculation at the Kaaba. This test will not
        give a reliable value, rather this test is to make sure a value can be
        calculated without crashing.
        """
        qibla = qibla_direction(LAT_AL_KAABA, LNG_AL_KAABA)

        # Verifying calculation returns a bearing.
        self.assertIsInstance(qibla, float)
        self.assertGreaterEqual(qibla, 0.0)
        self.assertLess(qibla, 360.0)

    def test_very_close_to_kaaba(self) -> None:
        """
        Tests the Qibla at a point very close to the Kaaba (within Makkah).
        Value should still be a reasonable direction.
        """
        # Location ~1 km North of Kaaba
        qibla = qibla_direction(LAT_AL_KAABA + 0.01, LNG_AL_KAABA)

        # Should point roughly south (180°)
        self.assertGreater(qibla, 170)
        self.assertLess(qibla, 190)

    def test_same_latitude_as_kaaba(self) -> None:
        """
        Tests the  Qibla from a location on the same latitude as the Kaaba.
        This tests the calculation when starting and ending points share latitude.
        """
        # Location at same latitude but 90° longitude West
        qibla = qibla_direction(LAT_AL_KAABA, LNG_AL_KAABA - 90)

        # Should point generally East
        self.assertGreater(qibla, 45)
        self.assertLess(qibla, 135)

    def test_equator(self) -> None:
        """Tests the Qibla direction from a location on the equator.
        Tests calculation for latitude = 0.
        """
        # Location on equator, East of Kaaba (Kenya)
        qibla = qibla_direction(0.0, 40.0)

        # Should point generally North (slightly West)
        self.assertGreater(qibla, 330)
        self.assertLess(qibla, 360)

    def test_north_pole(self) -> None:
        """Tests the Qibla direction from a point near the North Pole.
        Extreme latitude case.
        """
        qibla = qibla_direction(89.0, 0.0)

        # From North Pole, Makkah is to the South
        # Should point roughly South (180°), but exact value depends on longitude
        self.assertIsInstance(qibla, float)
        self.assertGreaterEqual(qibla, 0.0)
        self.assertLess(qibla, 360.0)

    def test_south_pole(self) -> None:
        """Tests Qibla direction from a point near the South Pole.
        Extreme negative latitude case.
        """
        qibla = qibla_direction(-89.0, 0.0)

        # From South Pole, Makkah is to the North
        # Should point roughly North (0°), but exact value depends on longitude
        self.assertIsInstance(qibla, float)
        self.assertGreaterEqual(qibla, 0.0)
        self.assertLess(qibla, 360.0)

    def test_result_range(self) -> None:
        """
        Tests that the Qibla direction is always in range of [0, 360).
        Test multiple locations to ensure normalization works correctly.
        """
        test_locations = [
            (40.7128, -74.0060),   # New York
            (-33.8688, 151.2093),  # Sydney
            (51.5074, -0.1278),    # London
            (35.6762, 139.6503),   # Tokyo
            (-23.5505, -46.6333),  # São Paulo
        ]

        for lat, lng in test_locations:
            qibla = qibla_direction(lat, lng)
            self.assertGreaterEqual(qibla, 0.0,
                                f"Qibla {qibla} < 0 for ({lat}, {lng})")
            self.assertLess(qibla, 360.0,
                        f"Qibla {qibla} >= 360 for ({lat}, {lng})")

    def test_decimal_precision(self) -> None:
        """
        Test that the result is rounded to 2 decimal places.
        """
        qibla = qibla_direction(40.7128, -74.0060)

        # Convert to string to check decimal places
        qibla_str = str(qibla)

        # Find decimal point
        if '.' in qibla_str:
            decimal_part = qibla_str.split('.')[1]
            # Should have at most 2 decimal places
            self.assertLessEqual(len(decimal_part), 2,
                                f"Qibla {qibla} has more than 2 decimal places")

    def test_opposite_hemispheres(self) -> None:
        """
        Test locations in all four combinations of hemispheres.
        """
        # Northeast (North America)
        qibla_ne = qibla_direction(40.7128, -74.0060)
        self.assertGreater(qibla_ne, 0)
        self.assertLess(qibla_ne, 90)

        # Northwest (Alaska)
        qibla_nw = qibla_direction(61.2181, -149.9003)
        self.assertGreater(qibla_nw, 0)
        self.assertLess(qibla_nw, 360)

        # Southeast (South Africa)
        qibla_se = qibla_direction(-33.9249, 18.4241)
        self.assertGreater(qibla_se, 0)
        self.assertLess(qibla_se, 90)

        # Southwest (South America)
        qibla_sw = qibla_direction(-23.5505, -46.6333)
        self.assertGreater(qibla_sw, 0)
        self.assertLess(qibla_sw, 360)

    def test_eastern_vs_western_hemisphere(self) -> None:
        """
        Test that eastern and western hemispheres give different results.
        Cities at similar latitudes but opposite hemispheres should have
        opposite Qibla directions.
        """
        # New York (West) vs Istanbul (East), both about 41°N
        qibla_ny = qibla_direction(40.7128, -74.0060)
        qibla_istanbul = qibla_direction(41.0082, 28.9784)

        # Verify the values
        self.assertAlmostEqual(qibla_ny, 58.48, delta=0.01)
        self.assertAlmostEqual(qibla_istanbul, 151.62, delta=0.01)

        # They should be almost opposite of each other (at least 50° difference)
        self.assertGreater(abs(qibla_ny - qibla_istanbul), 50)

    def test_northern_vs_southern_hemisphere(self) -> None:
        """
        Test that northern and southern hemispheres can give different results.
        """
        # Similar longitude but opposite hemispheres
        qibla_north = qibla_direction(40.0, -100.0)  # North America
        qibla_south = qibla_direction(-40.0, -100.0)  # South America

        # They should be different
        self.assertNotEqual(qibla_north, qibla_south)


class TestQiblaEdgeCases(unittest.TestCase):
    """
    Test the edge cases when calculation the Qibla direction.
    """

    def test_international_date_line(self) -> None:
        """
        Tests the Qibla calculation near the International Date Line. Tests that
        the longitude wrapping works (180° / -180°).
        """
        # Just West of the date line
        qibla_west = qibla_direction(0.0, 179.0)

        # Just East of date line
        qibla_east = qibla_direction(0.0, -179.0)

        # Both should be valid bearings
        self.assertGreaterEqual(qibla_west, 0.0)
        self.assertLess(qibla_west, 360.0)
        self.assertGreaterEqual(qibla_east, 0.0)
        self.assertLess(qibla_east, 360.0)

        # Values should be close since locations are close together
        self.assertAlmostEqual(qibla_west, qibla_east, delta=5.0)

    def test_prime_meridian(self) -> None:
        """
        Tests the Qibla direction at the Prime Meridian.
        """
        qibla = qibla_direction(51.5074, 0.0)

        # Checking the answer is a valid bearing
        self.assertGreaterEqual(qibla, 0.0)
        self.assertLess(qibla, 360.0)

    def test_extreme_precision(self) -> None:
        """
        Tests that the Qibla function can handle very precise coordinates.
        """
        qibla = qibla_direction(40.712775897, -74.006058216)

        # Should return a valid result
        self.assertIsInstance(qibla, float)
        self.assertGreaterEqual(qibla, 0.0)
        self.assertLess(qibla, 360.0)

        # Result should be rounded to 2 decimals
        self.assertEqual(qibla, round(qibla,2))


if __name__ == '__main__':
    unittest.main()
