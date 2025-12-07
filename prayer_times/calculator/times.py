"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Prayer time calculation functions.

This module contains the functions needed to calculate each of the five daily
Islamic prayer times (Fajr, Dhuhr, Asr, Maghrib, Isha). There is also a
calculation to find out when midday is and when sunrise is as well.

Author: Omar Younis
Date: 20/10/2025 [dd/mm/yyyy]
"""

import math
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
from zoneinfo import ZoneInfo

from prayer_times.config import get_fajr_angle, get_isha_config, HIGH_LATITUDE_THRESHOLD, UserSettings
from prayer_times.utils.math_utils import dsin, dcos, dacos, dcot, dacot, dasin
from prayer_times.core.astronomy import _equation_of_time


def _hour_correction(theta: float, lat: float, sun_data: Dict[str, float]) -> float:
    """
    Finds the number of hours needed to offset from Dhuhr to find the other
    prayer times.
    
    NOTE: This is an internal help function that calculates the time offset from
    the solar noon (Time of Dhuhr) based on the Sun's position angle.

    Args:
        theta (float): The azimuth angle (Sun's position below/above the horizon).
        lat (float): Your latitude in degrees.
        sun_data (Dict[str, float]): A dictionary containing the Sun coordinate data.

    Returns:
        float: The number of hours needed to offset from Dhuhr to find the prayer
            time related to the provided theta angle.
    """
    delta = sun_data["declination"]
    hour_angle = dacos((dcos(theta) - (dsin(lat) * dsin(delta))) / (dcos(lat) * dcos(delta)))

    # There are 15 longitudinal degrees per hour so we divide by 15 to get the
    # time offset.
    return hour_angle / 15


def midday_time_calc(timestamp: datetime, lng: float, sun_data: Dict[str, float]) -> datetime:
    """
    Calculates when solar midday occurs based on a location and sun coordinates.

    Solar midday (solar noon) is when the Sun reaches its highest point in the
    sky. This is slightly different from clock noon due to the equation of time
    and longitude differences within a timezone.

    Args:
        timestamp (datetime): Your current date. Can be timezone-aware or naive.
            If timezone-aware, uses that timezone's offset.
            If naive, estimates timezone from longitude (standard time, no DST).
        lng (float): Your current longitude in degrees.
        sun_data (Dict[str, float]): A dictionary containing the Sun coordinate data.

    Returns:
        datetime: The time of Midday (in the same timezone as input).
    """
    today_date = datetime.combine(timestamp, datetime.min.time())

    # Preserve timezone awareness from input
    if timestamp.tzinfo is not None:
        # Use the timezone from the input datetime
        today_date = today_date.replace(tzinfo=timestamp.tzinfo)
        tz_offset = timestamp.utcoffset().total_seconds() / 3600
    else:
        # For naive datetimes, estimate timezone from longitude
        # Note: This doesn't account for DST, but works for tests
        tz_offset = round(lng / 15)

    # Longitudinal difference in hours. Also 15 longitudinal degrees is 1 hour.
    lng_diff = ((tz_offset * 15) - lng) / 15
    equ_time = _equation_of_time(sun_data)

    # Find the hour number for Midday and converting it to a datetime.
    midday_hours = 12 + lng_diff - (equ_time / 60)
    midday_time = today_date + timedelta(hours=midday_hours)

    return midday_time


def dhuhr_time_calc(timestamp: datetime) -> datetime:
    """
    Calculates when Dhuhr prayer time is.
    
    Dhuhr is the midday prayer. According to an Islamic Hadith, prayer for Dhuhr 
    should be down after the Sun has passed its highest point (zenith). Because
    of this we add 65 seconds to the Dhuhr time to make sure the Sun has passed
    its zenith.

    Args:
        timestamp (datetime): The solar midday timestamp.

    Returns:
        datetime: The Dhuhr prayer time.
    """
    # We add 65 seconds to pass when the sun is at its highest point [hadith].
    return timestamp + timedelta(seconds=65.0)


def fajr_time_calc(timestamp: datetime,
                   lat: float,
                   sun_data: Dict[str, float],
                   conven: str,
                   sunrise_time: datetime,
                   maghrib_time: datetime,
                   settings: Optional[UserSettings] = None) -> datetime:
    """
    Calculates the pray time for Fajr.

    Fajr is the pre-dawn prayer. The time begins when the sky starts to lighten
    (otherwise known as astronomical twilight). Different Islamic calculation
    methods use different angles below the horizon to define this moment.

    NOTE: For high latitudes (> 48.5°), the Angle-Based Rule is used to handle
          the case where normal twilight doesn't happen.

    Args:
        timestamp (datetime): Time of solar midday.
        lat (float): Your latitude in degrees.
        sun_data (Dict[str, float]): A dictionary containing the Sun coordinate data.
        conven (str): Which calculation method you use for the angle (e.g. 'isna', 'uqu').
        sunrise_time (datetime): Sunrise time (needed for high latitude calculation).
        maghrib_time (datetime): Maghrib time (needed for high latitude calculation).
        settings (Optional[UserSettings]): User settings with potential custom angle.

    Returns:
        datetime: Fajr prayer time.
    """
    fajr_angle = get_fajr_angle(conven, settings)

    # No need to adjust for high latitude.
    if abs(lat) <= HIGH_LATITUDE_THRESHOLD:
        # Find the theta angle of the Sun to indicate Fajr (angle will be below
        # the horizon).
        theta = 90 + fajr_angle
        hour_offset = _hour_correction(theta, lat, sun_data)
        return timestamp - timedelta(hours=hour_offset)

    # Need to adjust for high latitude using `Angle Base Rule`.
    night_duration = (sunrise_time + timedelta(24)) - maghrib_time
    return sunrise_time - (night_duration * (fajr_angle / 60))


def sunrise_time_calc(timestamp: datetime,
                      lat: float,
                      sun_data: Dict[str, float],
                      elevation: float) -> datetime:
    """
    Calculates the time of sunrise.
    
    Sunrise is calculated as the moment when the top edge of the Sun appears on
    the horizon. This is adjusted for atmospheric refraction (0.833°) and the
    elevation above sea level.
    
    NOTE: Sunrise marks when the Fajr prayer time window ends.

    Args:
        timestamp (datetime): Time of solar midday.
        lat (float): Your latitude in degrees.
        sun_data (Dict[str, float]): A dictionary containing the Sun coordinate data.
        elevation (float): Your altitude in meters above sea level.

    Returns:
        datetime: Sunrise time.
    """
    # 0.833° for atmospheric refraction, plus elevation correction
    theta = 90 + 0.83333 + (0.0347 * math.sqrt(elevation))
    hour_offset = _hour_correction(theta, lat, sun_data)

    return timestamp - timedelta(hours=hour_offset)


def asr_time_calc(timestamp: datetime,
                  lat: float,
                  sun_data: Dict[str, float],
                  hanafi=False) -> datetime:
    """
    Calculates the time of Asr prayer.
    
    Asr prayer time begins when the shadow of an object becomes a certain length:
    - Standard (Shafi'i, Maliki, Hanbali): Shadow length = object length
    - Hanafi: Shadow length = 2 * object length

    Args:
        timestamp (datetime): Time of solar midday.
        lat (float): Your latitude in degrees.
        sun_data (Dict[str, float]): A dictionary containing the Sun coordinate data.
        hanafi (bool): True for Hanafi calculation, False for standard calculation. Default: False.

    Returns:
        datetime: Asr prayer time.
    """
    delta = sun_data["declination"]
    a = dasin((dsin(lat) * dsin(delta)) + (dcos(lat) * dcos(delta)))

    # There are 2 juristic methods for asr. Hanafi says that the shadow of an
    # object needs to be two times the length of that object. Most other schools
    # say that the shadow of the object only needs to be equal to the length of
    # the object in question to indicate Asr time.
    if not hanafi:
        theta = abs(90 - dacot(1 + dcot(a)))
    else:
        theta = abs(90 - dacot(2 + dcot(a)))

    hour_offset = _hour_correction(theta, lat, sun_data)

    return timestamp + timedelta(hours=hour_offset)


def maghrib_time_calc(timestamp: datetime,
                      lat: float,
                      sun_data: Dict[str, float],
                      elevation: float) -> datetime:
    """
    Calculates the time of Maghrib.
    
    Maghrib is the evening prayer which happens just after sunset. The time is
    when the Sun's top edge disappears below the horizon, with corrections for
    atmospheric refraction and elevation.

    Args:
        timestamp (datetime): Time of solar midday.
        lat (float): Your latitude in degrees.
        sun_data (Dict[str, float]): A dictionary containing the Sun coordinate data.
        elevation (float): Your altitude in meters above sea level.

    Returns:
        datetime: Maghrib prayer time.
    """
    # Same angle calculation as sunrise (due to symmetry of the day around noon)
    theta = 90 + 0.83333 + (0.0347 * math.sqrt(elevation))
    hour_offset = _hour_correction(theta, lat, sun_data)

    # Add value rather than subtracted like in sunrise calculation (symmetry)
    return timestamp + timedelta(hours=hour_offset)


def isha_time_calc(timestamp: datetime,
                   lat: float,
                   sun_data: Dict[str, float],
                   conven: str,
                   maghrib_time: datetime,
                   sunrise_time: datetime,
                   ramadan: bool=False,
                   settings: Optional[UserSettings] = None) -> datetime:
    """
    Calculates the Isha prayer time.

    Isha is the night prayer. Most calculations are based on the Sun's angle
    below the horizon, similar to Fajr.

    Special cases example:
        Umm Al-Qura University (Makkah) uses a fixed time offset:
        - 90 minutes after Maghrib (normal months)
        - 120 minutes after Maghirb (during Ramadan)

    For high latitudes, the Angle-Based Rule is used.

    Args:
        timestamp (datetime): Time of solar midday.
        lat (float): Your latitude in degrees.
        sun_data (Dict[str, float]): A dictionary containing the Sun coordinate data.
        conven (str): Which convention you use (e.g. 'insa', 'mwl').
        maghrib_time (datetime): Maghrib time (needed for special case and high lat).
        sunrise_time (datetime): Sunrise time (needed for special case and high lat).
        ramadan (bool, optional): Is it Ramadan? Used for special case. Defaults: False.
        settings (Optional[UserSettings]): User settings with potential custom angle.

    Returns:
        datetime: Isha prayer time.
    """
    # Get Isha configuration (handles both angle-based and fixed-time methods)
    isha_config = get_isha_config(conven, settings)

    # Check if we need to use fixed-time method (e.g. 'uqu')
    if isha_config['type'] == 'fixed_time':
        # Use fixed minutes after Maghrib
        if ramadan:
            offset_minutes = isha_config['offset_ramadan']
        else:
            offset_minutes = isha_config['offset_normal']

        return maghrib_time + timedelta(minutes=offset_minutes)

    # Angle-based method
    isha_angle = isha_config['angle']

    # No need to adjust for high latitude
    if abs(lat) <= HIGH_LATITUDE_THRESHOLD:
        theta = 90 + isha_angle
        hour_offset = _hour_correction(theta, lat, sun_data)

        return timestamp + timedelta(hours=hour_offset)

    # Need to adjust for high latitude using `Angle-Based Rule`
    night_duration = (sunrise_time + timedelta(hours=24)) - maghrib_time
    return maghrib_time + (night_duration * (isha_angle /60))
