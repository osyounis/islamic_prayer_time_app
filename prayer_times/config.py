"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

This file holds the configuration setting and constants used for the Islamic
Prayer Time App.

In this module:
- Reference constants (e.g. Kaaba coordinates).
- Prayer calculation method configurations.
- Hijri calendar data.
- Default user settings.
- Functions to safely access configurations.

Author: Omar Younis
Date: 19/10/2025 [dd/mm/yyyy]

"""

from datetime import datetime
from typing import Dict, Any


#===============================================================================
#                               CONSTANTS
#===============================================================================
# Latitude and Longitude of Al Kaaba [These remain as unchanging constants].
LAT_AL_KAABA = 21.4225
LNG_AL_KAABA = 39.8262

# Calendar reference dates needed fro astronomical calculations.
REFERENCE_DATE = datetime(1582, 10, 15) # Switched to Gregorian calendar date
HIJRI_EPOCH_JD = 1948440    # The Julian date for when the Hijri calendar was
                            # adopted otherwise known as the Islamic epoch
                            # (July 16, 622 AD)

# The latitude threshold for when to switch over to a special calculation method
# for Fajr and Isha prayer.
HIGH_LATITUDE_THRESHOLD = 48.5  # degrees


#===============================================================================
#                  CALCULATION METHOD CONFIGURATIONS
#===============================================================================
CALCULATION_METHODS = {
    'mwl': {
        'name': 'Muslim World League',
        'fajr_angle': 18.0,
        'isha_angle': 17.0,
        'isha_type': 'angle'
    },
    'isna': {
        'name': 'Islamic Society of North America',
        'fajr_angle': 15.0,
        'isha_angle': 15.0,
        'isha_type': 'angle'
    },
    'egas': {
        'name': 'Egyptian General Authority of Survey',
        'fajr_angle': 19.5,
        'isha_angle': 17.5,
        'isha_type': 'angle'
    },
    'uqu': {
        'name': 'Umm al-Qura University, Makkah',
        'fajr_angle': 18.5,
        'isha_angle': None,
        'isha_type': 'fixed_time',
        'isha_offset_normal': 90,   # Minutes after Maghrib (not Ramadan)
        'isha_offset_ramadan': 120  # Minutes after Maghrib (Ramadan)
    },
    'uisk': {
        'name': 'University of Islamic Sciences, Karachi',
        'fajr_angle': 18.0,
        'isha_angle': 18.0,
        'isha_type': 'angle'
    },
     'ut': {
        'name': 'Institute of Geophysics, University of Tehran',
        'fajr_angle': 17.7,
        'isha_angle': 14.0,
        'isha_type': 'angle'
    },
     'lri': {
        'name': 'Shia Ithna Ashari, Leva Research Institute, Qum',
        'fajr_angle': 16.0,
        'isha_angle': 14.0,
        'isha_type': 'angle'
    },
     'gulf': {
        'name': 'Gulf Region, Fixed Isha Time Interval',
        'fajr_angle': 19.5,
        'isha_angle': None,
        'isha_type': 'fixed_time',
        'isha_offset_normal': 90,   # Minutes after Maghrib (not Ramadan)
        'isha_offset_ramadan': 90  # Minutes after Maghrib (Ramadan)
     },
     'jakim': {
        'name': 'Jabatan Kemajuan Islam Malaysia',
        'fajr_angle': 20.0,
        'isha_angle': 18.0,
        'isha_type': 'angle'
    },
}


#===============================================================================
#                          HIJRI CALENDAR DATA
#===============================================================================
HIJRI_MONTHS = {
    1: {"en": "Muharram", "ar": "مُحَرَّم"},
    2: {"en": "Safar", "ar": "صَفَر"},
    3: {"en": "Rabi' Al-Awwal", "ar": "رَبِيع الأَوَّل"},
    4: {"en": "Rabi' Al-Thani", "ar": "رَبِيع الثَّانِي"},
    5: {"en": "Jumada Al-Awwal", "ar": "جُمَادَىٰ الأُولَىٰ"},
    6: {"en": "Jumada Al-Thani", "ar": "جمادى الثانية"},
    7: {"en": "Rajab", "ar": "رَجَب"},
    8: {"en": "Sha'ban", "ar": "شَعْبَان"},
    9: {"en": "Ramadan", "ar": "رَمَضَان"},
    10: {"en": "Shawwal", "ar": "شَوَّال"},
    11: {"en": "Dhu Al-Qadah", "ar": "ذُو القَعْدَة"},
    12: {"en": "Dhu Al-Hijjah", "ar": "ذُو الحِجَّة"}
}


#===============================================================================
#                         DEFAULT USER SETTINGS
#===============================================================================
DEFAULT_CALCULATION_METHOD = 'isna'
DEFAULT_ASR_METHOD = 'standard'  # Options: 'standard' [shadow length = object]
                                 # or 'hanafi' [shadow length = 2 times object]

DEFAULT_HIJRI_CORRECTION = 0    # Days to adjust Hijri date
DEFAULT_HIGH_LATITUDE_METHOD = 'angle_based'    # Method for high latitude


#===============================================================================
#                         CONFIG HELPER FUNCTIONS
#===============================================================================
def get_method_config(method_key: str) -> Dict[str, Any]:
    """
    Gets calculation method configuration if valid, otherwise throws an error
    and lists the valid method_keys available.

    Args:
        method_keys (str): The method key (e.g. 'isna', 'mwl', 'uqu')
    
    Raises:
        ValueError: If method_key is not valid

    Returns:
        Dict[str, Any]: The configuration details dictionary for the provided
                        method.
    
    Example:
        >>> config = get_method_config('isna')
        >>> print(config['name'])
        'Islamic Society of North America'
    """
    # If not a valid method, throws and error and lists the valid method keys.
    if method_key not in CALCULATION_METHODS:
        valid_methods = ', '.join(CALCULATION_METHODS.keys())
        raise ValueError(
            f"Invalid method '{method_key}'. "
            f"Valid methods: {valid_methods}"
        )
    return CALCULATION_METHODS[method_key]


def get_method_name(method_key: str) -> str:
    """
    Gets the full name of a calculation method.

    Args:
        method_key (str): The method key (e.g. 'isna', 'uqu')

    Returns:
        str: The full name of the method
    
    Example:
        >>> get_method_name('uqu')
        'Umm al-Qura University, Makkah'
    """
    return get_method_config(method_key)['name']


def get_fajr_angle(method_key: str) -> float:
    """
    Gets the Fajr angle for a particular calculation method.

    Args:
        method_key (str): The method key (e.g. 'isna', 'uqu')

    Returns:
        float: The Fajr angle in degrees
    
    Example:
        >>> get_fajr_angle('isna')
        15.0
    """
    return get_method_config(method_key)['fajr_angle']


def get_isha_config(method_key: str) -> Dict[str, Any]:
    """
    Gets the Isha prayer configuration for a calculation method.
    
    This handles when we are using a fixed_time interval after Maghrib, or if we
    are going to use an angle based approach to find Isha prayer time.

    Args:
        method_key (str): The method key (e.g. 'isna', 'uqu')

    Returns:
        Dict[str, Any]: Configuration dictionary with one of the following
        formats:
        
        Angle-Based method:
        {
            'type': 'angle',
            'angle': <float>    # degrees below horizon
        }
        
        Fixed-Time method:
        {
            'type': 'fixed_time',
            'offset_normal': <int>,  # minutes after Maghrib
            'offset_ramadan': <int>  # minutes after Maghrib during Ramadan
        }
    
    Examples:
        Angle-Based method:
        >>> config = get_isha_config('isna')
        >>> print(config)
        {'type': 'angle', 'angle': 15.0}
        
        Fixed-Time method:
        >>> config = get_isha_config('uqu')
        >>> print(config)
        {'type': 'fixed_time', 'offset_normal': 90, 'offset_ramadan': 120}
    """
    config = get_method_config(method_key)
    # Need to check if we need to do the fixed method or angle method.
    if config['isha_type'] == 'angle':
        return {
            'type': 'angle',
            'angle': config['isha_angle']
        }
    # Using the fixed_time method.
    return {
        'type': 'fixed_time',
        'offset_normal': config['isha_offset_normal'],
        'offset_ramadan': config['isha_offset_ramadan']
    }


def is_ramadan(hijri_month: int) -> bool:
    """
    Checks if a given month is Ramadan.

    Args:
        hijri_month (int): The Hijri month as a number (1- 12)

    Returns:
        bool: True if the month is Ramadan (month 9), False otherwise.
    
    Example:
        >>> is_ramadan(9)
        True
        >>> is_ramadan(8)
        False
    """
    return hijri_month == 9


def get_hijri_month_name(month: int, language: str = 'en') -> str:
    """
    Get the name of the Hijri month in English or Arabic.

    Args:
        month (int): The Hijri month number (1-12)
        language (str, optional): The language code - 'en' for English, 'ar' for
                                  Arabic . Defaults to 'en'.

    Raises:
        ValueError: If month number is not between 1-12
        ValueError: If language code is invalid

    Returns:
        str: The month name in the provided language
    
    Example:
        >>> get_hijri_month_name(9, 'en')
        'Ramadan'
        >>> get_hijri_month_name(9, 'ar')
        'رَمَضَان'
    """
    if month not in HIJRI_MONTHS:
        raise ValueError(f"Invalid month number: {month}. Must be between 1-12.")
    if language not in {'en', 'ar'}:
        raise ValueError(f"Invalid language: {language}. Must be 'en' or 'ar'.")
    return HIJRI_MONTHS[month][language]


def list_all_methods() -> Dict[str, str]:
    """
    Gets a dictionary of method keys and their full names for all available
    calculation methods.

    Returns:
        Dict[str, str]: Dictionary of method keys and their full names.
    
    Example:
        >>> methods = list_all_methods()
        >>> for key, name in methods.items():
        ...     print(f"{key}: {name}")
        mwl: Muslim Work League
        isna: Islamic Society of North America
        ...
    """
    return {key: config['name'] for key, config in CALCULATION_METHODS}


#===============================================================================
#                         USER SETTINGS CLASS
#===============================================================================
class UserSettings:
    """
    A user's preferences for the prayer calculation.
    
    This class provides an easy way to bundle a user's preferences.
    
    Attributes:
        calculation_method: The calculation method used (e.g. 'isna')
        asr_method: Asr calculation method - 'standard' or 'hanafi'
        hijri_correction: Days to adjust calculated Hijri date (default: 0)
    
    Example:
        >>> settings = UserSettings(method='isna', asr_method='standard')
        >>> print(settings.calculation_method)
        'isna'
    """

    def __init__(self,
                 method: str = DEFAULT_CALCULATION_METHOD,
                 asr_method: str = DEFAULT_ASR_METHOD,
                 hijri_correction: int = DEFAULT_HIJRI_CORRECTION):
        """
        Initialize user settings

        Args:
            method (str, optional): Calculation method key. Defaults to 
            DEFAULT_CALCULATION_METHOD.
            
            asr_method (str, optional): 'standard' or 'hanafi'. Defaults to
            DEFAULT_ASR_METHOD.
            
            hijri_correction (int, optional): Days to adjust Hijri date.
            Defaults to DEFAULT_HIJRI_CORRECTION.

        Raises:
            ValueError: If method key is invalid.
            ValueError: If asr_method isn't recognized.
        """
        # Checking if method exsists
        if method not in CALCULATION_METHODS:
            valid_methods = ', '.join(CALCULATION_METHODS.keys())
            raise ValueError(
                f"Invalid calculation method '{method}'. "
                f"Valid methods: {valid_methods}"
            )
        # Checking if asr_method is a valid option
        if asr_method not in {"standard", "hanafi"}:
            raise ValueError(
                f"Invalid asr_method '{asr_method}. "
                f"Must be 'standard' or 'hanafi'."
            )

        self.calculation_method = method
        self.asr_method = asr_method
        self.hijri_correction = hijri_correction


    def __repr__(self):
        """
        String representation of UserSettings
        """
        return (f"UserSettings(method='{self.calculation_method}', "
                f"asr_method='{self.asr_method}', "
                f"hijri_correction={self.hijri_correction})")
