"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Astronomical calculations for prayer time determination.

This module calculates the Sun's position and related astronomical data needed
to calculate prayer times.

Author: Omar Younis
Date: 19/10/2025 [dd/mm/yyyy]
"""


from typing import Dict
from prayer_times.utils.math_utils import dsin, dcos, dasin, datan2


def sun_coordinates(j_date: float) -> Dict[str, float]:
    """
    Calculates various Sun-related data needed to calculate prayer times.
    
    NOTE: The calculations in this module have been simplified but are still
          accurate enough for prayer time calculation (within two minutes is
          usually considered acceptable).

    Args:
        j_date (float): The Julian Date.

    Returns:
        Dict[str, float]: A dictionary containing all the relevant Sun data.
            - solar_lng: Mean longitude of the Sun, corrected for aberration (degrees)
            - mean_anomaly: Mean anomaly of the Sun (degrees)
            - ecliptic_lng: Ecliptic longitude of the Sun (degrees)
            - obliq_ecliptic: Obliquity of the ecliptic (degrees)
            - ascension: Right ascension of the Sun (degrees)
            - dist: Distance between Earth and Sun (astronomical units)
            - declination: Declination of the Sun (degrees)
            - semi_dia: Semi-diameter of the Sun (degrees)
    
    Example:
        >>> sun_data = sun_coordinates(2451544.5)   # Jan 1, 2000
        >>> print(sun_data['declination'])
        -23.07...
    """
    # Number of days since 01/01/2000 [n].
    num_days = j_date - 2451545.0

    # Mean longitude of the Sun, corrected for aberration [L] degrees.
    corr_mean_solar_lng = (280.466 + 0.9856474 * num_days) % 360

    # Mean Anomaly [g] degrees.
    mean_anomaly = (357.528 + 0.9856003 * num_days) % 360

    # Ecliptic Longitude [𝛌].
    ecliptic_lng = (corr_mean_solar_lng + (1.915 * dsin(mean_anomaly))
                    + (0.020 * dsin(2 * mean_anomaly)))

    # Obliquity of Ecliptic [𝛆].
    obli_ecliptic = 23.440 - 0.0000004 * num_days

    # Right Ascension [𝛂].
    right_ascension = datan2(dcos(obli_ecliptic) * dsin(ecliptic_lng), dcos(ecliptic_lng))

    # Declination [𝛅].
    declination = dasin(dsin(obli_ecliptic) * dsin(ecliptic_lng))

    # Distance between the Earth and the Sun [R].
    earth_sun_dist = (1.00014 - (0.01671 * dcos(mean_anomaly))
                      - (0.00014 * dcos(2 * mean_anomaly)))
    semi_diameter = 0.2666 / earth_sun_dist

    # All Sun coordinate data needed to calculate equation of time and hour angles.
    data = {
        "solar_lng": corr_mean_solar_lng,
        "mean_anomaly": mean_anomaly,
        "ecliptic_lng": ecliptic_lng,
        "obliq_ecliptic": obli_ecliptic,
        "ascension": right_ascension,
        "dist": earth_sun_dist,
        "declination": declination,
        "semi_dia": semi_diameter
        }

    return data


def _equation_of_time(sun_data: Dict[str, float]) -> float:
    """
    Calculates the equation of time based on the Sun coordinate data.
    
    NOTE: The equation of time represents the difference between (sundial time)
          and (clock time). This correction is needed because Earth's orbit is
          elliptical and is tilted on its axis.
    
    Equation of Time = (L - alpha) * 4
    
        where:
            L:          Mean longitude of Sun, corrected for aberration.
            alpha:      Right ascension
            4:          Conversion factor (4 minutes per degree)

    Args:
        sun_data (Dict[str, float]): A dictionary containing all the Sun coordinate
        data needed to find the equation of time. Use the `_sun_coordinates`
        function to get the Sun coordinate data.

    Returns:
        float: The equation of time in minutes.
    """
    return (sun_data["solar_lng"] - sun_data["ascension"]) * 4
