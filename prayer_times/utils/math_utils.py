"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

This module contains utility math functions that are needed for this project.

NOTE: - Avoids using some built in Python functions since they do not exist in the
        Swift coding language. The ultimate goal is to use what is learned in this
        project to create an iOS app that does the same thing.
      
      - By default, the trigonometry functions in Python's `math` library use
        radians, not degrees. Therefore degree versions have been created since
        it is more convenient to use degrees for some of the calculations that
        take place. 


Author: Omar Younis
Date: 28/09/2025 [dd/mm/yyyy format]

"""

import math


def _degree_to_radians(degree: float) -> float:
    """Converts a given degree angle to a radian angle.

    Args:
        degree (float): A degree angle

    Returns:
        float: The radian angle of the provided degree angle.
    """
    return (degree * math.pi) / 180

def _radians_to_degree(radians: float) -> float:
    """Converts a given radian angle to a degree angle.

    Args:
        radians (float): A radian angle.

    Returns:
        float: A degree angle.
    """
    return (radians * 180) / math.pi

def dsin(angle: float) -> float:
    """Does the sin(x) operation given a degree angle.

    Args:
        angle (float): A degree angle.

    Returns:
        float: The result of sin(x) of the provided degree angle.
    """
    return math.sin(_degree_to_radians(angle))

def dcos(angle: float) -> float:
    """Does the cos(x) operation given a degree angle.

    Args:
        angle (float): A degree angle.

    Returns:
        float: The result of cos(x) of the provided degree angle.
    """
    return math.cos(_degree_to_radians(angle))

def dcot(angle: float) -> float:
    """Finds the cot(x) of the given degree angle.
       
       cot(x) = cos(x) / sin(x)

    Args:
        angle (float): A degree angle.

    Returns:
        float: The result of cot(x) of the provided degree angle.
    """
    radian_angle = _degree_to_radians(angle)
    return math.cos(radian_angle) / math.sin(radian_angle)

def dasin(value: float) -> float:
    """Find the degree angle of the asin(x) for a value.

    Args:
        value (float): Value to calculate asin(x) from.

    Returns:
        float: A degree angle from asin(x).
    """
    return _radians_to_degree(math.asin(value))

def dacos(value: float) -> float:
    """Finds the degree angle for the acos(x) function.

    Args:
        value (float): Value to calculate acos(x) from.

    Returns:
        float: A degree angle from acos(x).
    """
    return _radians_to_degree(math.acos(value))

def datan2(y_value: float, x_value: float) -> float:
    """Runs the atan2(y, x) function and returns a degree angle. 
    
    atan2() considers all four quadrants unlike atan().
    
    The atan2(y, x) function assumes you are trying to find the atan(y / x). The
    `math` library's atan2(y, x) function uses y as the numerator, and x as the
    denominator. It also returns the answer in radians.
    
    Args:
        y_value (float): The numerator of atan(y / x).
        x_value (float): The denominator of atan(y / x).


    Returns:
        float: The results of atan2(y, x) in degrees.
    """
    return _radians_to_degree(math.atan2(y_value, x_value))

def dacot(value: float) -> float:
    """Calculates the acot(x) for the provided value. atan2(x) is used in this
    calculation to keep track of the quadrant of the angle to make sure the
    correct angle is returned.
    
    Properties:
    - Range is (0° - 180°)
    - For x > 0: returns angle in (0° - 90°)
    - For x < 0: returns angle in (90° - 180°)
    - For x = 0: returns 90°

    Args:
        value (float): The value used to calculate acot(x) from.

    Returns:
        float: The degree angle of acot(x).
    """

    if value == 0:
        return 90.0

    angle = datan2(1, value)
    # If we get a negative value, need to adjust the angle to be in the corrrect
    # quadrant.
    if angle < 0:
        angle += 180.0
    return angle
