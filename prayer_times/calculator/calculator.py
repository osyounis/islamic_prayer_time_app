"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Main prayer time calculator - runs all the calculations in one place.

This module is the main interface for calculating the Islamic prayer times. It
coordinates all the individual calculation modules to produce a complete set of
prayer times for any location and date.

The modules in question are:
- calendar
- astronomy
- qibla
- times

Author: Omar Younis
Date: 20/10/2025 [dd/mm/yyyy]
"""

from datetime import datetime
from typing import Dict, Optional

from prayer_times.config import UserSettings

from prayer_times.core.calendar import julian_date, hijri_date
from prayer_times.core.astronomy import sun_coordinates
from prayer_times.core.qibla import qibla_direction

from prayer_times.calculator.times import (
    midday_time_calc,
    dhuhr_time_calc,
    fajr_time_calc,
    sunrise_time_calc,
    asr_time_calc,
    maghrib_time_calc,
    isha_time_calc
)

from prayer_times.utils.time_utils import round_time


class PrayerTimeCalculator:
    """
    Main class to calculate all prayer time for a particular location.
    
    This class holds all the logic needed to calculate prayer times, Qibla
    direction, and calendar conversions for a specific location.
    
    Attributes:
        latitude (float): Latitude in degrees
        longitude (float): Longitude in degrees
        elevation (float): Elevation in meters above sea level
        settings (UserSettings): User preferences for calculations
    
    Example:
        >>> from prayer_times.config import UserSettings
        >>> settings = UserSettings(method='isna', asr_method='standard)
        >>> calc = PrayerTimeCalculator(33.88, -117.93, 50, settings)
        >>> results = calc.calculate()
        >>> print(results['times_rounded']['fajr'])
        05:23
    """

    def __init__(self, latitude: float, longitude: float, elevation: float,
                 settings: Optional[UserSettings] = None):
        """
        Initializes calculator with location and settings.

        Args:
            latitude (float): Your latitude in degrees (-90 to 90).
                Positive for North, negative for South.
                
            longitude (float): Your longitude in degrees (-180 to 180).
                Positive for East, negative for West.
                
            elevation (float): Your elevation in meters above sea level.
            
            settings (Optional[UserSettings], optional): User preferences. 
                If None, then default settings wil be used.
        
        Example:
            >>> # Fullerton, CA
            >>> calc = PrayerTimeCalculator(33.88, -117.928611, 50)
            
            >>> # With custom settings
            >>> settings = UserSettings(method='isna', asr_method='hanafi')
            >>> calc = PrayerTimeCalculator(33.88, -117.928611, 50, settings)
        """
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        # Uses custom settings if supplied, otherwise uses the default settings.
        self.settings = settings if settings else UserSettings()

    def calculate(self, date: Optional[datetime] = None) -> Dict:
        """
        Calculates all the prayer times for a given date.
        
        This method performs all the calculations and returns a dictionary
        containing:
        - Qibla direction
        - Gregorian and Hijri dates
        - All five prayer times (Fajr, Dhuhr, Asr, Maghrib, Isha)
        - Sunrise time
        - Precise and rounded times.

        Args:
            date (Optional[datetime], optional): The date to calculate for.
                If None, it uses the current date/time.

        Returns:
            Dict: All prayer times and related information. Dict structure:
                {
                    'qibla': float,
                    'gregorian_date': datetime,
                    'hijri_date': {'day': int, 'month': int, 'year': int},
                    'times': {
                        'fajr': datetime,
                        'sunrise': datetime,
                        'dhuhr': datetime,
                        'asr': datetime,
                        'maghrib': datetime,
                        'isha': datetime
                    },
                    'times_rounded': {
                        'fajr': datetime,
                        'sunrise': datetime,
                        'dhuhr': datetime,
                        'asr': datetime,
                        'maghrib': datetime,
                        'isha': datetime
                    }
                }

        Example:
            >>> calc = PrayerTimeCalculator(33.88, -117.93, 50)
            >>> results = calc.calculate()
            >>> print(f"Qibla: {results['qibla']}°")
            >>> print(f"Fajr: {results['times_rounded']['fajr'].strftime('%H:%M')}")
        """
        if date is None:
            # Use timezone-aware datetime for proper DST handling
            date = datetime.now().astimezone()

        # 1: Calculate Qibla direction
        qibla = qibla_direction(self.latitude, self.longitude)

        # 2: Calculate Julian and Hijri dates
        jul_date = julian_date(date)
        hij_date = hijri_date(jul_date, self.settings.hijri_correction)

        # 3: Calculate sun coordinates
        sun_info = sun_coordinates(jul_date)

        # 4: Calculate midday and Dhuhr (other times use this as a base)
        midday = midday_time_calc(date, self.longitude, sun_info)
        dhuhr = dhuhr_time_calc(midday)

        # 5: Calculate sunrise and Maghrib (used for Fajr and Isha in special cases)
        sunrise = sunrise_time_calc(dhuhr, self.latitude, sun_info, self.elevation)
        maghrib = maghrib_time_calc(dhuhr, self.latitude, sun_info, self.elevation)

        # 6: Calculate Fajr (might use sunrise and maghrib if high latitude)
        fajr = fajr_time_calc(dhuhr,
                              self.latitude,
                              sun_info,
                              self.settings.calculation_method,
                              sunrise,
                              maghrib,
                              self.settings)

        # 7: Calculate Isha (might use Maghrib time for fix-time method)
        is_ramadan = hij_date['month'] == 9
        isha = isha_time_calc(dhuhr,
                              self.latitude,
                              sun_info,
                              self.settings.calculation_method,
                              maghrib,
                              sunrise,
                              ramadan=is_ramadan,
                              settings=self.settings)

        # 8: Calculates Asr (depends on Standard or Hanafi)
        use_hanafi = self.settings.asr_method == 'hanafi'
        asr = asr_time_calc(dhuhr, self.latitude, sun_info, hanafi=use_hanafi)

        # 9: Create and return all results of calculations in a dict
        return {
            'qibla': qibla,
            'gregorian_date': date,
            'hijri_date': hij_date,
            'times': {
                'fajr': fajr,
                'sunrise': sunrise,
                'dhuhr': dhuhr,
                'asr': asr,
                'maghrib': maghrib,
                'isha': isha
            },
            'times_rounded': {
                'fajr': round_time(fajr),
                'sunrise': round_time(sunrise),
                'dhuhr': round_time(dhuhr),
                'asr': round_time(asr),
                'maghrib': round_time(maghrib),
                'isha': round_time(isha)
            }
        }

def calculate_prayer_times(latitude: float,
                            longitude: float,
                            elevation: float,
                            date: Optional[datetime] = None,
                            settings: Optional[UserSettings] = None) -> Dict:
    """
    Easy function to calculate prayer times.
    
    This is a simpler function that doesn't require creating a calculator
    object. Use this for one-time calculations. For multiple calculations at
    the same location, create a PrayerTimeCalculator object instead.

    Args:
        latitude (float): Your latitude in degrees.
        longitude (float): Your longitude in degrees.
        elevation (float): Your elevation in meters.
        date (Optional[datetime], optional): Date to calculate for.
            Default uses today's date.
        settings (Optional[UserSettings], optional): User preferences. Uses
            default settings if None.

    Returns:
        Dict: All prayer times and information
            (same as using PrayerTimeCalculator.calculate()).
    
    Example:
        >>> # Simple usage with default settings
        >>> times = calculate_prayer_times(33.88, -117.93, 50)
        >>> print(times['times_rounded']['fajr'])
        
        >>> # With custom settings
        >>> from prayer_times.config import UserSettings
        >>> from datetime import datetime
        >>> settings = UserSettings(method='isna', asr_method='hanafi')
        >>> date = datetime(2025, 1, 15)
        >>> times = calculate_prayer_times(33.88, -117.93, 50, date, settings)
    """
    calculator = PrayerTimeCalculator(latitude, longitude, elevation, settings)
    return calculator.calculate(date)
