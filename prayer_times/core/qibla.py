"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Qibla (قبلة) direction calculation.

This module calculates the bearing direction to face in order to pray, based on
the user's location and the Kaaba's location.

The calculation uses the Great Circle bearing formula to find the shortest path
on Earth's surface between two points.

Author: Omar Younis
Date: 19/10/2024 [dd/mm/yyyy]
"""

from prayer_times.config import LAT_AL_KAABA, LNG_AL_KAABA
from prayer_times.utils.math_utils import dsin, dcos, datan2


def qibla_direction(your_latitude: float, your_longitude: float) -> float:
    """
    Calculates the bearing direction to for prayer based on a location.
    
    This function takes a latitude and longitude value of your current location
    and uses it in combination with the latitude and longitude of The Kaaba to
    calculate the bearing angle on a compass to face. This is calculated using
    Greater Circles and uses the following equation:
    
    Δ𝛌= 𝛌2 - 𝛌1
    y = sin(Δ𝛌) * cos(𝛟2)
    x = [cos(𝛟1) * sin(𝛟2)] - [sin(𝛟1) * cos(𝛟2) * cos(Δ𝛌)]
    𝛉 = atan2(y, x)
    
    where:
        𝛌1: Starting point longitude
        𝛌2: Ending point longitude
        𝛟1: Starting point latitude
        𝛟2: Ending point longitude
        𝛉:  Bearing angle from north (0 degrees)

    The returned value is in degrees from true north (0 - 360) measure clockwise.
    
    Args:
        your_latitude (float): Your current latitude position in degrees.
            North is positive, South is negative.
            
        your_longitude (float): Your current longitude position in degrees.
            East is positive, West is negative.

    Returns:
        float: The bearing (in degrees) you need to face for prayer, measured
            clockwise from true north and rounded to 2 decimal places.
    
    Example:
        New York City:
        >>> qibla = qibla_direction(40.7128, -74.0060)
        >>> print(f"Qibla direction: {qibla} degrees")
        Qibla direction: 58.48 degrees
    """
    # Finds the delta in longitude between your location (starting point) and
    # The Kaaba (ending point).
    delta_lng = LNG_AL_KAABA - your_longitude

    # Finding the y and x values that are needed to run atan2(y, x) for the
    # Great Circle Bearing calculation [See function description for detailed
    # explanation of equation].
    y = dsin(delta_lng) * dcos(LAT_AL_KAABA)
    x = ((dcos(your_latitude) * dsin(LAT_AL_KAABA))
         - (dsin(your_latitude) * dcos(LAT_AL_KAABA) * dcos(delta_lng)))

    # Find the theta value needed to point to from bearing 000 degrees (also
    # known as 360 degrees).
    theta = datan2(y, x)

    # The answer makes sure that bearing is a value between 0 and 360, and has
    # an accuracy of 2 decimal points. You don't really need to be more accurate
    # with than that (usually 0.5 degree tolerance is more than enough).
    return round((360 + theta) % 360, 2)
