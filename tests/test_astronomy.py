"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

This module contains tests used to make sure that the astronomy module doesn't
have any errors.

Author: Omar Younis
Date: 22/10/2025 [dd/mm/yyyy format]

"""


import unittest
from prayer_times.core.astronomy import sun_coordinates, _equation_of_time


class TestSunCoordinates(unittest.TestCase):
    """
    Tests the sun_coordinates functions.
    """

    def test_j2000_epoch(self) -> None:
        """
        Test Sun data for J2000.0 epoch (Jan 1, 2000, noon) against the known
        value for this date based on astronomical tables.
        """
        jd = 2451545.0      # J2000.0
        sun_data = sun_coordinates(jd)

        # Check that all needed keys exist
        required_keys = ['solar_lng',
                         'mean_anomaly',
                         'ecliptic_lng',
                         'obliq_ecliptic',
                         'ascension',
                         'dist',
                         'declination',
                         'semi_dia']

        for key in required_keys:
            self.assertIn(key, sun_data)

        # Mean longitude should be about 289.46°
        self.assertAlmostEqual(sun_data['solar_lng'], 280.466, delta=1.0)

        # Mean anomaly should be about 357.53°
        self.assertAlmostEqual(sun_data['mean_anomaly'], 357.528, delta=1.0)

        # Obliquity should be about 23.44°
        self.assertAlmostEqual(sun_data['obliq_ecliptic'], 23.440, delta=0.01)

        # Declination should be about -23° (winter solstice was about 2 weeks prior)
        self.assertAlmostEqual(sun_data['declination'], -23.0, delta=2.0)


    def test_summer_solstice_declination(self) -> None:
        """
        Tests to see if the declination is positive and at a max near summer
        solstice. Around June 21, declination should be close to +23.44°.
        """
        # June 21, 2000 (value was looked up from a table)
        jd = 2451716.5
        sun_data = sun_coordinates(jd)

        # Declination should be positive and near max.
        self.assertGreater(sun_data['declination'], 20.0)
        self.assertLess(sun_data['declination'], 24.0)


    def test_winter_solstice_declination(self) -> None:
        """
        Tests to see if the declination is negative and close to minimum near
        the winter solstice. Around Dec 21, the declination should be close to
        -23.44°.
        """
        # Dec 21, 2000 (value was looked up from a table)
        jd = 2451899.5
        sun_data = sun_coordinates(jd)

        # Declination should be negative and near min.
        self.assertLess(sun_data['declination'], -20.0)
        self.assertGreater(sun_data['declination'], -24.0)


    def test_equinox_declination(self) -> None:
        """
        Tests that the declination is near 0° at the equinox. Around March 20
        and Sept 22 are the equinoxes. Declination should be close to 0°.
        """
        # March 20, 2000
        jd_1= 2451623.5
        sun_data_1 = sun_coordinates(jd_1)

        # Sept 22, 2000
        jd_2 = 2451809.5
        sun_data_2 = sun_coordinates(jd_2)

        # Declinations should be close to 0°.
        self.assertAlmostEqual(sun_data_1['declination'], 0.0, delta=2.0)
        self.assertAlmostEqual(sun_data_2['declination'], 0.0, delta=2.0)


    def test_earth_sun_distance_range(self) -> None:
        """
        Tests that the Earth-Sun distance is within the correct range. The
        distance should be between 0.983 and 1.017 AU.
        """
        # Test multiple random dates throughout the year.
        for day_offset in [0, 77, 185, 275]:
            jd = 2451545.0 + day_offset
            sun_data = sun_coordinates(jd)

            # Distances should be in the expected range (0.983 - 1.017 AU).
            self.assertGreater(sun_data['dist'], 0.98)
            self.assertLess(sun_data['dist'], 1.02)


class TestEquationOfTime(unittest.TestCase):
    """
    Tests the Equation of Time calculation.
    """

    def test_eot_specific_dates(self) -> None:
        """
        Tests the equation of time for specific dates with know values. The values
        are based on the implementation's calculation method
        """
        # Nov 3, 2000: EoT should be about +16 minutes
        jd = 2451851.5      # Nov 3, 2000
        sun_data = sun_coordinates(jd)
        eot = _equation_of_time(sun_data)
        self.assertAlmostEqual(eot, 16.4, delta=3.0)

        # Feb 12, 2000: EoT should be about -14 minutes
        jd = 2451586.5      # Feb 12, 2000
        sun_data = sun_coordinates(jd)
        eot = _equation_of_time(sun_data)
        self.assertAlmostEqual(eot, -14.3, delta=3.0)


if __name__ == '__main__':
    unittest.main()
