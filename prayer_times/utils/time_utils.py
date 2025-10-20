"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

This module contains functions for time conversion and time formatting for
prayer time calculations.

Author: Omar Younis
Date: 28/09/2025 [dd/mm/yyyy format]

"""

from datetime import datetime, timedelta


def hours_to_time(date: datetime, hours: float) -> datetime:
    """
    Converts an hour amount into a time.
    
    Takes a date and a number of hours, and returns a datetime object
    representing that time on the given date.

    Args:
        date (datetime): The current date you are calculating.
        hours (float): The number of hours your want to convert.

    Returns:
        datetime: The current date plus the time the hours provided were
        converted from.
    
    Example:
        >>> date = datetime(2025, 1, 15)
        >>> hours_to_time(date, 5.5)
        datetime(2025, 1, 15, 5, 30)
    """
    # Gets the supplied date and sets the time of the datetime object to
    # zero (midnight).
    start = datetime.combine(date, datetime.min.time())

    # Finds what the time would be for the provided number of hours.
    time = start + timedelta(hours=hours)

    return time


def round_time(timestamp: datetime) -> datetime:
    """
    Rounds a timestamp to the nearest minute.
    
    If timestamp has 30 seconds or more, it rounds up to the next
    minute; otherwise it rounds downs.

    Args:
        timestamp (datetime): Your timestamp to round.

    Returns:
        datetime: The rounded timestamp with both seconds and
        microseconds set to 0.
    
    Example:
        >>> timestamp = datetime(2025, 1, 15, 5, 23, 45)
        >>> round_time(timestamp)
        datetime(2025, 1, 15, 5, 24, 0)
    """
    # Round up if we have 30 or more seconds.
    if timestamp.second >= 30:
        timestamp += timedelta(minutes=1)

    # Zero the seconds and microseconds and return that answer.
    return timestamp.replace(second=0, microsecond=0)
