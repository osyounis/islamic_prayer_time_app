"""
  بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

This module contains functions to convert between Gregorian, Julian, and Hijri
calendar systems. These conversions are essential to calculate accurate prayer
times.

Author: Omar Younis
Date: 19/10/2025 [dd/mm/yyyy]
"""

import math
from datetime import datetime
from typing import Tuple, Dict

from prayer_times.config import REFERENCE_DATE, HIJRI_EPOCH_JD


def _month_and_year_offset(month: int, year: int) -> Tuple[int, int]:
    """
    Adds an offset to the year and month if needed to find the Julian Date.
    
    NOTE: This is an internal function only to be used by the `julian_date`
    function.
    
    When calculating the Julian Date, we would need to adjust the year and month
    that we supply to our Julian Date formula based on what month value is given.
    If our month is 1 or 2 we need to adjust our month by adding 12 to it. We also
    need to subtract a year from our year for the Julian Date formula to give us
    the correct answer. In short:
    
    If Month is 1 or 2, then Month = Month + 12 and Year = Year - 1
    Else Month and Year remain unchanged.

    Args:
        month (int): The month in number form (Jan = 1, Feb = 2, etc...)
        year (int): The year we are calculating for.

    Raises:
        ValueError: Month values cannot be 0 or negative values, so we raise and
        error if a value like that is supplied to the month.

    Returns:
        Tuple[int, int]: The (month, year) tuple to use for the Julian Date calculation.
    """
    # Month and year doesn't needed to be changed for all month values above 2.
    if month > 2:
        return month, year

    # Error for 0 and negative month values.
    elif month < 1:
        raise ValueError("Month cannot be 0 or negative")

    # We need to offset our month and year.
    else:
        month = month + 12
        year = year - 1
        return month, year


def _b_value(date: datetime) -> int:
    """
    Calculates the B-value correction factor for Julian Date conversion.

    NOTE: This is an internal function only to be used by the `julian_date` function.

    On October 15, 1582 [dd/mm/yyyy], the world transitioned from the Julian
    calendar to the Gregorian calendar. This reform addressed the accumulated
    drift in the Julian calendar's leap year system. The Gregorian calendar
    introduced more precise leap year rules: years divisible by 100 are NOT
    leap years unless they are also divisible by 400.

    The B-value compensates for the difference between these two calendar systems
    when calculating Julian Dates:

    - For dates BEFORE October 15, 1582: No correction needed (B = 0)
      These dates use the original Julian calendar system.

    - For dates ON or AFTER October 15, 1582: Apply correction (B = 2 - A + A/4)
      where A = floor(year / 100) represents the century number.
      This formula accounts for the century leap years that exist in the Julian
      calendar but are omitted in the Gregorian calendar.

    Args:
        date (datetime): The date you want to convert to a Julian date.

    Returns:
        int: The B-value correction factor (0 for Julian calendar dates,
        or a calculated offset for Gregorian calendar dates).
    """
    # Strip timezone info for comparison (only compare dates, not times/timezones)
    date_naive = date.replace(tzinfo=None) if date.tzinfo else date

    # Date is before Gregorian switch so no offset is needed.
    if REFERENCE_DATE > date_naive:
        return 0

    # Date is after Gregorian switch so offset is needed.
    a_value = int(date.year / 100)
    return 2 - a_value + int(a_value / 4)


def julian_date(date: datetime) -> int:
    """
    Calculates the Julian Date given a date.
    
    The Julian Date counts the number of days that have pasts since since
    January 1, 4713 BC, despite calender changes. It is a continuous count of
    the days. We need the Julian Date to calculate our prayer times. The equation
    for calculating the Julian Date is as follows:
    
    JD = int(365.25 * (Y + 4716)) + int(30.6001 * (M + 1)) + D + B - 1524.5
    
    where:
        JD: Julian Date
        Y: Year
        M: Month
        D: Day
        B: B Value offset

    Args:
        date (datetime): The date you want to calculate the Julian Date for.

    Returns:
        int: The Julian Date (the number of days that have passed from the date
        provided January 1, 4713 BC).
    
    Example:
        >>> date = datetime(2000, 1, 1)
        >>> julian_date(date)
        2451544.5
    """
    # Check whether we need to offset the month and year.
    month, year = _month_and_year_offset(date.month, date.year)

    # Check whether we need a B offset.
    b_offset = _b_value(date)

    # Calculate the Julian Date.
    j_date = (int(365.25 * (year + 4716)) + int(30.6001 * (month + 1))
              + date.day + b_offset - 1524.5)

    return j_date


def hijri_date(j_date: int, d_correction: int = 0) -> Dict[str, int]:
    """
    Calculates the Hijri Date given a Julian Date.

    The Hijri Date is the Islamic calendar. It is based on lunar observation and
    is how Ramadan is determined. Since the Hijri date is calculated using
    astronomical calculations but officially is determined (like in the case for
    determining when Ramadan is) by eye sight/human intervention, this function
    has a corrective factor (days to add or remove) to the calculated date to
    find the official date. This correction can keep changing so keep that in
    mind.

    To find the Hijri date, you need the Julian date first (the number of days
    that have passed from the date provided January 1, 4713 BC).

    The algorithm uses the Islamic calendar's 30-year cycle structure:
    - Each cycle contains 19 common years (354 days) and 11 leap years (355 days)
    - The leap years occur in years 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, and 29
    - Total days in a 30-year cycle = 10631 days

    Args:
        j_date (int): The Julian date to calculate the Hijri date for.
        d_correction (int): The number of days to add to the calculated date.

    Returns:
        Dict[str, int]: The day, month, and year of the Hijri Date.
    
    Example:
        >>> j_date = 2451544.5      # Jan 1, 2000
        >>> hijri_date(j_date)
        {'day': 24, 'month': 9, 'year': 1420}
    """
    # Step 1: Calculate days since the start of the Islamic calendar.
    # 1948440 is the Julian date for the Islamic epoch (July 16, 622 AD).
    # We add 10632 to align with the algorithm's internal reference point.
    l = math.floor(j_date + d_correction) - HIJRI_EPOCH_JD + 10632

    # Step 2: Calculate how many complete 30-year cycles have passed.
    # 'n' represents the number of complete 30-year cycles in the Islamic calendar.
    # Each cycle contains exactly 10631 days.
    n = math.floor((l - 1) / 10631)

    # Step 3: Update 'l' to represent the remaining days within the current cycle.
    # We add 354 (days in a common Islamic year) as a reference adjustment.
    l = l - 10631 * n + 354

    # Step 4: Determine the year within the current 30-year cycle.
    # 'j' represents which year (0-29) we are in within the current cycle.
    # This formula accounts for the irregular distribution of leap years.
    j = (math.floor((10985 - l) / 5316) * math.floor((50 * l) / 17719)
         + math.floor(l / 5670) * math.floor((43 * l) / 15238))

    # Step 5: Refine 'l' to represent the day of the year.
    # After this calculation, 'l' will represent an intermediate value used
    # to extract the month and day within the year.
    l = (l - math.floor((30 - j) / 15) * math.floor((17719 * j) / 50)
         - math.floor(j / 16) * math.floor((15238 * j) / 43) + 29)

    # Step 6: Extract the month from the refined 'l' value.
    # Islamic months alternate between 29 and 30 days (with some variation).
    # The ratio 709/24 ≈ 29.54 approximates the average month length.
    month = math.floor((24 * l) / 709)

    # Step 7: Calculate the day of the month by removing the month contribution.
    day = l - math.floor((709 * month) / 24)

    # Step 8: Calculate the Hijri year.
    # We multiply cycles 'n' by 30, add the year within the cycle 'j',
    # and subtract 30 to align with the proper year numbering.
    year = math.floor(30 * n + j - 30)

    return {"day": day, "month": month, "year": year}
