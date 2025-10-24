"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Calculation Methods Comparison Example - Islamic Prayer Time Calculator

This example compares prayer times using different calculation methods to show
how they differ.

Author: Omar Younis
Date: 22/10/2025 [dd/mm/yyyy]

"""

from datetime import datetime
from prayer_times.config import UserSettings, get_method_name
from prayer_times.calculator.calculator import calculate_prayer_times


def main() -> None:
    """
    Compare prayer times using different calculation methods.
    """

    # Location (example: Fullerton, CA)
    LATITUDE = 33.88
    LONGITUDE = -117.928611
    ELEVATION = 50

    date = datetime.now()

    # Methods to compare
    methods = ['isna', 'mwl', 'egas', 'uqu', 'uisk', 'jakim']

    print("\n" + "="*100)
    print(f"Comparison of Calculation Methods - {date.strftime('%B %d, %Y')}")
    print(f"Location: {LATITUDE}°N, {LONGITUDE}°E")
    print("="*100 + "\n")

    # Print header
    print(f"{'Method':<40} {'Fajr':>10} {'Dhuhr':>10} {'Asr':>10} {'Maghrib':>10} {'Isha':>10}")
    print("-"*100)

    for method in methods:
        # Create settings
        settings = UserSettings(method=method, asr_method='standard')

        # Calculate
        results = calculate_prayer_times(LATITUDE, LONGITUDE, ELEVATION, date, settings)
        times = results['times_rounded']

        # Get method name
        method_name = get_method_name(method)

        # Display
        print(f"{method_name:<40} "
            f"{times['fajr'].strftime('%I:%M %p'):>10} "
            f"{times['dhuhr'].strftime('%I:%M %p'):>10} "
            f"{times['asr'].strftime('%I:%M %p'):>10} "
            f"{times['maghrib'].strftime('%I:%M %p'):>10} "
            f"{times['isha'].strftime('%I:%M %p'):>10}")

    print("="*100)

    # Show Asr method comparison
    print("\n" + "="*60)
    print("Asr Calculation Method Comparison")
    print("="*60 + "\n")

    for asr_method in ['standard', 'hanafi']:
        settings = UserSettings(method='isna', asr_method=asr_method)
        results = calculate_prayer_times(LATITUDE, LONGITUDE, ELEVATION, date, settings)
        asr_time = results['times_rounded']['asr']

        method_desc = ("Standard (Shafi'i, Maliki, Hanbali)"
                       if asr_method == 'standard' else "Hanafi")
        print(f"{method_desc:<40} Asr: {asr_time.strftime('%I:%M %p')}")

    print("="*60 + "\n")


if __name__ == '__main__':
    main()
