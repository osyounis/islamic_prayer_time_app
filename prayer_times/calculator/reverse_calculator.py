"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Reverse Prayer Time Calculator

This module provides functionality to calculate the Fajr and Isha angles
that would produce observed prayer times at a given location. This is the
reverse of the normal calculation (which calculates times from angles).

Use cases:
- Research: Determine what calculation parameters a mosque uses
- Validation: Verify if local times match a specific calculation method
- Analysis: Study how prayer times vary with different angles

Author: Omar Younis
Date: 30/12/2024 [dd/mm/yyyy]
"""

from datetime import datetime, timedelta
from typing import Dict, List

from prayer_times.config import HIGH_LATITUDE_THRESHOLD
from prayer_times.utils.math_utils import dsin, dcos, dacos
from prayer_times.core.astronomy import sun_coordinates
from prayer_times.core.calendar import julian_date
from prayer_times.calculator.times import midday_time_calc, sunrise_time_calc


def _reverse_hour_correction(time_offset_hours: float, lat: float,
                            sun_data: Dict[str, float]) -> float:
    """
    Inverse of _hour_correction from times.py - calculates theta from time offset.

    This function reverses the hour angle calculation to determine what sun
    position angle (theta) would produce a given time offset from solar noon.

    Args:
        time_offset_hours (float): Time offset from solar noon in hours
        lat (float): Latitude in degrees
        sun_data (Dict[str, float]): Sun coordinate data containing declination

    Returns:
        float: Theta angle in degrees (90 + angle_below_horizon)

    Raises:
        ValueError: If calculation results in invalid arc-cosine domain
    """
    delta = sun_data["declination"]

    # Step 1: Convert time offset to hour angle (15 degrees per hour)
    hour_angle = time_offset_hours * 15

    # Step 2: Validate hour angle is in valid range
    if not 0 <= hour_angle <= 180:
        raise ValueError(
            f"Time offset {time_offset_hours:.2f}h produces invalid hour angle "
            f"{hour_angle:.2f}°. Must be in range [0, 180]°."
        )

    # Step 3: Reverse the _hour_correction formula
    # Original: hour_angle = acos((cos(theta) - sin(lat)*sin(delta)) / (cos(lat)*cos(delta)))
    # Solving for theta:
    # cos(theta) = cos(hour_angle) * cos(lat) * cos(delta) + sin(lat) * sin(delta)
    cos_theta = (dcos(hour_angle) * dcos(lat) * dcos(delta) +
                 dsin(lat) * dsin(delta))

    # Step 4: Clamp to valid domain for numerical stability
    # Sometimes floating point errors cause values slightly outside [-1, 1]
    cos_theta = max(-1.0, min(1.0, cos_theta))

    # Step 5: Calculate theta
    theta = dacos(cos_theta)

    return theta


def reverse_fajr_angle(fajr_time: datetime, midday: datetime, lat: float,
                      sun_data: Dict[str, float], sunrise_time: datetime,
                      maghrib_time: datetime,
                      check_high_lat: bool = True) -> Dict:
    """
    Calculates Fajr angle from observed Fajr time.

    Args:
        fajr_time (datetime): Observed Fajr prayer time
        midday (datetime): Solar noon time
        lat (float): Latitude in degrees
        sun_data (Dict[str, float]): Sun coordinate data
        sunrise_time (datetime): Sunrise time (for validation and high latitude)
        maghrib_time (datetime): Maghrib time (for high latitude calculation)
        check_high_lat (bool): Whether to check for high latitude adjustment

    Returns:
        Dict containing:
            'angle': Calculated Fajr angle in degrees
            'method': 'standard' or 'high_latitude'
            'valid': Boolean indicating if angle is in reasonable range
            'warnings': List of warning messages

    Raises:
        ValueError: If fajr_time is after midday or calculation impossible
    """
    # Validate fajr_time is before midday
    if fajr_time >= midday:
        raise ValueError(
            f"Invalid Fajr time: {fajr_time.strftime('%H:%M')} is not before "
            f"solar noon {midday.strftime('%H:%M')}"
        )

    warnings = []
    method = 'standard'

    # Check if high latitude
    is_high_lat = abs(lat) > HIGH_LATITUDE_THRESHOLD

    if is_high_lat and check_high_lat:
        # Use reverse of Angle-Based Rule
        # Original: fajr_time = sunrise - (night_duration * (fajr_angle / 60))
        # Solving for fajr_angle:
        # fajr_angle = 60 * (sunrise - fajr_time) / night_duration

        night_duration = (sunrise_time + timedelta(hours=24)) - maghrib_time
        time_diff = sunrise_time - fajr_time

        # Calculate angle
        angle = 60 * (time_diff.total_seconds() / 3600) / (night_duration.total_seconds() / 3600)

        method = 'high_latitude'
        warnings.append(
            f"High latitude ({lat:.1f}°) detected. Calculated angle is based on "
            f"Angle-Based Rule (proportional method), not actual solar angle."
        )
    else:
        # Standard calculation
        # Calculate time offset from solar noon
        time_offset = (midday - fajr_time).total_seconds() / 3600

        # Get theta using reverse hour correction
        try:
            theta = _reverse_hour_correction(time_offset, lat, sun_data)
        except ValueError as e:
            raise ValueError(f"Cannot calculate Fajr angle: {e}") from e

        # Extract angle below horizon
        angle = theta - 90

    # Validate angle range and add warnings
    valid = True
    if angle < 0 or angle > 30:
        warnings.append(
            f"Fajr angle {angle:.2f}° is outside valid range (0-30°). "
            f"This indicates invalid input time or extreme location."
        )
        valid = False
    elif angle < 12 or angle > 21:
        warnings.append(
            f"Fajr angle {angle:.2f}° is outside typical range (12-21°). "
            f"Please verify input times are correct."
        )

    return {
        'angle': angle,
        'method': method,
        'valid': valid,
        'warnings': warnings
    }


def reverse_isha_angle(isha_time: datetime, midday: datetime, lat: float,
                      sun_data: Dict[str, float], sunrise_time: datetime,
                      maghrib_time: datetime,
                      check_high_lat: bool = True) -> Dict:
    """
    Calculates Isha angle from observed Isha time.

    Args:
        isha_time (datetime): Observed Isha prayer time
        midday (datetime): Solar noon time
        lat (float): Latitude in degrees
        sun_data (Dict[str, float]): Sun coordinate data
        sunrise_time (datetime): Sunrise time (for high latitude calculation)
        maghrib_time (datetime): Maghrib time (for validation and high latitude)
        check_high_lat (bool): Whether to check for high latitude adjustment

    Returns:
        Dict containing:
            'angle': Calculated Isha angle in degrees
            'method': 'standard' or 'high_latitude'
            'valid': Boolean indicating if angle is in reasonable range
            'warnings': List of warning messages

    Raises:
        ValueError: If isha_time is before maghrib or calculation impossible
    """
    # Validate isha_time is after maghrib
    if isha_time <= maghrib_time:
        raise ValueError(
            f"Invalid Isha time: {isha_time.strftime('%H:%M')} is not after "
            f"Maghrib {maghrib_time.strftime('%H:%M')}"
        )

    warnings = []
    method = 'standard'

    # Check if high latitude
    is_high_lat = abs(lat) > HIGH_LATITUDE_THRESHOLD

    if is_high_lat and check_high_lat:
        # Use reverse of Angle-Based Rule
        # Original: isha_time = maghrib + (night_duration * (isha_angle / 60))
        # Solving for isha_angle:
        # isha_angle = 60 * (isha_time - maghrib) / night_duration

        night_duration = (sunrise_time + timedelta(hours=24)) - maghrib_time
        time_diff = isha_time - maghrib_time

        # Calculate angle
        angle = 60 * (time_diff.total_seconds() / 3600) / (night_duration.total_seconds() / 3600)

        method = 'high_latitude'
        warnings.append(
            f"High latitude ({lat:.1f}°) detected. Calculated angle is based on "
            f"Angle-Based Rule (proportional method), not actual solar angle."
        )
    else:
        # Standard calculation
        # Calculate time offset from solar noon
        time_offset = (isha_time - midday).total_seconds() / 3600

        # Get theta using reverse hour correction
        try:
            theta = _reverse_hour_correction(time_offset, lat, sun_data)
        except ValueError as e:
            raise ValueError(f"Cannot calculate Isha angle: {e}") from e

        # Extract angle below horizon
        angle = theta - 90

    # Validate angle range and add warnings
    valid = True
    if angle < 0 or angle > 30:
        warnings.append(
            f"Isha angle {angle:.2f}° is outside valid range (0-30°). "
            f"This indicates invalid input time or extreme location."
        )
        valid = False
    elif angle < 12 or angle > 20:
        warnings.append(
            f"Isha angle {angle:.2f}° is outside typical range (12-20°). "
            f"Please verify input times are correct."
        )

    return {
        'angle': angle,
        'method': method,
        'valid': valid,
        'warnings': warnings
    }


def calculate_isha_minutes(isha_time: datetime, maghrib_time: datetime) -> float:
    """
    Calculates minutes between Maghrib and Isha.

    This is useful for calculation methods that use fixed time intervals
    (e.g., Umm Al-Qura uses 90 minutes after Maghrib).

    Args:
        isha_time (datetime): Observed Isha time
        maghrib_time (datetime): Observed Maghrib time

    Returns:
        float: Minutes between Maghrib and Isha (rounded to 1 decimal)

    Raises:
        ValueError: If isha_time is before maghrib_time
    """
    if isha_time < maghrib_time:
        raise ValueError(
            f"Invalid times: Isha {isha_time.strftime('%H:%M')} is before "
            f"Maghrib {maghrib_time.strftime('%H:%M')}"
        )

    time_diff = isha_time - maghrib_time
    minutes = time_diff.total_seconds() / 60

    return round(minutes, 1)


def validate_prayer_time_sequence(fajr: datetime, sunrise: datetime,
                                  maghrib: datetime, isha: datetime) -> None:
    """
    Validates that prayer times are in correct chronological order.

    Args:
        fajr (datetime): Fajr time
        sunrise (datetime): Sunrise time
        maghrib (datetime): Maghrib time
        isha (datetime): Isha time

    Raises:
        ValueError: If times are not in correct order
    """
    if not (fajr < sunrise < maghrib < isha):
        raise ValueError(
            f"Prayer times must be in order: Fajr < Sunrise < Maghrib < Isha. "
            f"Got: Fajr={fajr.strftime('%H:%M')}, Sunrise={sunrise.strftime('%H:%M')}, "
            f"Maghrib={maghrib.strftime('%H:%M')}, Isha={isha.strftime('%H:%M')}"
        )


def validate_angle_range(angle: float, prayer_name: str,
                        min_angle: float = 0, max_angle: float = 30) -> List[str]:
    """
    Validates calculated angle is in reasonable range.

    Args:
        angle (float): Calculated angle
        prayer_name (str): Name of prayer (for error messages)
        min_angle (float): Minimum valid angle (default: 0)
        max_angle (float): Maximum valid angle (default: 30)

    Returns:
        List[str]: List of warning messages (empty if valid)
    """
    warnings = []
    if angle < min_angle or angle > max_angle:
        warnings.append(
            f"{prayer_name} angle {angle:.2f}° is outside typical range "
            f"({min_angle}° - {max_angle}°). This may indicate invalid input times."
        )
    return warnings


class ReversePrayerCalculator:
    """
    Main class for reverse prayer time calculations.

    Calculates what Fajr and Isha angles would produce observed prayer times
    at a given location.

    Attributes:
        latitude (float): Latitude in degrees
        longitude (float): Longitude in degrees
        elevation (float): Elevation in meters above sea level
    """

    def __init__(self, latitude: float, longitude: float, elevation: float):
        """
        Initialize reverse calculator with location.

        Args:
            latitude (float): Latitude in degrees (-90 to 90)
            longitude (float): Longitude in degrees (-180 to 180)
            elevation (float): Elevation in meters above sea level
        """
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def reverse_calculate(self, date: datetime, fajr_time: datetime,
                         maghrib_time: datetime, isha_time: datetime) -> Dict:
        """
        Calculates angles from observed prayer times.

        Args:
            date (datetime): Date of observation (timezone-aware)
            fajr_time (datetime): Observed Fajr time (timezone-aware)
            maghrib_time (datetime): Observed Maghrib time (timezone-aware)
            isha_time (datetime): Observed Isha time (timezone-aware)

        Returns:
            Dict containing:
                'fajr_angle': Calculated Fajr angle (float)
                'fajr_method': Calculation method used ('standard' or 'high_latitude')
                'isha_angle': Calculated Isha angle (float)
                'isha_method': Calculation method used ('standard' or 'high_latitude')
                'isha_minutes': Minutes after Maghrib (float)
                'midday': Calculated solar noon (datetime)
                'sunrise': Calculated sunrise (datetime)
                'astronomical_data': Sun coordinates (dict)
                'warnings': List of warnings (List[str])
                'high_latitude': Boolean indicating if location is high latitude
                'valid': Boolean indicating if all calculated values are valid

        Raises:
            ValueError: If times are invalid or calculation is impossible
        """
        # Step 1: Calculate astronomical data
        jd = julian_date(date)
        sun_data = sun_coordinates(jd)

        # Step 2: Calculate midday (solar noon)
        midday = midday_time_calc(date, self.longitude, sun_data)

        # Step 3: Calculate sunrise (for validation and high latitude detection)
        sunrise = sunrise_time_calc(midday, self.latitude, sun_data, self.elevation)

        # Step 4: Validate time sequence
        try:
            validate_prayer_time_sequence(fajr_time, sunrise, maghrib_time, isha_time)
        except ValueError as e:
            raise ValueError(
                f"Invalid prayer time sequence. {e}\n"
                f"Note: Calculated sunrise is {sunrise.strftime('%H:%M')}. "
                f"If your observed times don't match this sequence, please check inputs."
            ) from e

        # Step 5: Calculate Fajr angle
        fajr_result = reverse_fajr_angle(
            fajr_time, midday, self.latitude, sun_data, sunrise, maghrib_time
        )

        # Step 6: Calculate Isha angle
        isha_result = reverse_isha_angle(
            isha_time, midday, self.latitude, sun_data, sunrise, maghrib_time
        )

        # Step 7: Calculate Isha minutes after Maghrib
        isha_minutes = calculate_isha_minutes(isha_time, maghrib_time)

        # Step 8: Compile warnings
        all_warnings = fajr_result['warnings'] + isha_result['warnings']

        # Add warning if Fajr and Isha angles differ significantly
        angle_diff = abs(fajr_result['angle'] - isha_result['angle'])
        if angle_diff > 10:
            all_warnings.append(
                f"Large difference between Fajr ({fajr_result['angle']:.2f}°) and "
                f"Isha ({isha_result['angle']:.2f}°) angles ({angle_diff:.2f}° difference). "
                f"This is unusual - please verify input times."
            )

        # Step 9: Compile results
        return {
            'fajr_angle': fajr_result['angle'],
            'fajr_method': fajr_result['method'],
            'isha_angle': isha_result['angle'],
            'isha_method': isha_result['method'],
            'isha_minutes': isha_minutes,
            'midday': midday,
            'sunrise': sunrise,
            'astronomical_data': sun_data,
            'warnings': all_warnings,
            'high_latitude': abs(self.latitude) > HIGH_LATITUDE_THRESHOLD,
            'valid': fajr_result['valid'] and isha_result['valid']
        }


def reverse_calculate_angles(lat: float, lng: float, elev: float,
                            date: datetime, fajr_time: datetime,
                            maghrib_time: datetime, isha_time: datetime) -> Dict:
    """
    Convenience function to calculate angles from observed prayer times.

    This is a simplified interface similar to calculate_prayer_times()
    from the forward calculator.

    Args:
        lat (float): Latitude in degrees
        lng (float): Longitude in degrees
        elev (float): Elevation in meters
        date (datetime): Date of observation
        fajr_time (datetime): Observed Fajr time
        maghrib_time (datetime): Observed Maghrib time
        isha_time (datetime): Observed Isha time

    Returns:
        Dict: Results from ReversePrayerCalculator.reverse_calculate()
    """
    calculator = ReversePrayerCalculator(lat, lng, elev)
    return calculator.reverse_calculate(date, fajr_time, maghrib_time, isha_time)
