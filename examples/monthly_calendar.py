"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Monthly Prayer Calendar Example - Islamic Prayer Time Calculator

 This example generates a complete monthly prayer time calendar.

Author: Omar Younis
Date: 22/10/2025 [dd/mm/yyyy]

"""
from datetime import datetime
from calendar import monthrange
from prayer_times.config import UserSettings
from prayer_times.calculator.calculator import calculate_prayer_times


def main() -> None:
    """
    Generate a monthly prayer time calendar.
    """
    # ==================== CONFIGURATION ====================

    # Location (example: Fullerton, CA)
    LATITUDE = 33.88
    LONGITUDE = -117.928611
    ELEVATION = 50

    # Settings
    METHOD = 'isna'
    ASR_METHOD = 'standard'

    # Month to generate (change these as needed)
    YEAR = 2025
    MONTH = 3  # March

    # ==================== CALCULATION ====================

    settings = UserSettings(method=METHOD, asr_method=ASR_METHOD)

    # Get number of days in the month
    _, num_days = monthrange(YEAR, MONTH)

    # Print header
    month_name = datetime(YEAR, MONTH, 1).strftime('%B %Y')
    print("\n" + "="*90)
    print(f"Prayer Times for {month_name}")
    print(f"Location: {LATITUDE}°N, {LONGITUDE}°E | Method: {METHOD.upper()}")
    print("="*90 + "\n")

    # Print table header
    print(f"{'Date':<12} {'Fajr':>10} {'Sunrise':>10} {'Dhuhr':>10} {'Asr':>10} {'Maghrib':>10} {'Isha':>10}")
    print("-"*90)

    # Calculate for each day
    for day in range(1, num_days + 1):
        date = datetime(YEAR, MONTH, day)

        results = calculate_prayer_times(LATITUDE, LONGITUDE, ELEVATION, date, settings)
        times = results['times_rounded']

        # Format date
        date_str = date.strftime('%b %d, %a')

        # Print times
        print(f"{date_str:<12} "
            f"{times['fajr'].strftime('%I:%M %p'):>10} "
            f"{times['sunrise'].strftime('%I:%M %p'):>10} "
            f"{times['dhuhr'].strftime('%I:%M %p'):>10} "
            f"{times['asr'].strftime('%I:%M %p'):>10} "
            f"{times['maghrib'].strftime('%I:%M %p'):>10} "
            f"{times['isha'].strftime('%I:%M %p'):>10}")

    print("="*90 + "\n")


if __name__ == '__main__':
    main()
