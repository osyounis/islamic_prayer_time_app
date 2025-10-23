"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Basic Usage Example - Islamic Prayer Time Calculator

This shows a simple example showing how to calculate prayer times for
Fullerton, CA and can be modified for your location.

Author: Omar Younis
Date: 22/10/2025 [dd/mm/yyyy]

"""

from datetime import datetime
from prayer_times.config import UserSettings
from prayer_times.calculator.calculator import calculate_prayer_times


def main():
    """
    Calculates and display the prayer times for today.
    """

    # ========================= CONFIGURATION =========================
    # You can change these values for your location

    # Example: Fullerton, CA
    LATITUDE = 33.88
    LONGITUDE = -117.928611
    ELEVATION = 50      # meters above sea level

    # Calculation method (see README for all options)
    METHOD = 'isna'     # Islamic Society of North America

    # Asr calculation method
    ASR_METHOD = 'standard'     # or 'hanafi'


    # ========================== CALCULATION ==========================
    # Create settings
    settings = UserSettings(
        method=METHOD,
        asr_method=ASR_METHOD,
        hijri_correction=2
    )

    # Calculate for today
    date = datetime.now()
    results = calculate_prayer_times(LATITUDE, LONGITUDE, ELEVATION, date, settings)


    # ========================= DISPLAY RESULTS ========================
    times = results['times_rounded']
    qibla = results['qibla']
    hijri = results['hijri_date']

    print("\n" + "="*60)
    print("Islamic Prayer Times")
    print("="*60)
    print(f"\nDate: {date.strftime('%A, %B %d, %Y')}")
    print(f"Location: {LATITUDE}°N, {LONGITUDE}°E")
    print(f"Method: {METHOD.upper()}")
    print(f"\nQibla Direction: {qibla:.2f}° from North")
    print(f"Hijri Date: {hijri['month']}/{hijri['day']}/{hijri['year']} AH")

    print("\n" + "-"*60)
    print("Prayer Times:")
    print("-"*60)
    print(f"Fajr        {times['fajr'].strftime('%I:%M %p')}    [{times['fajr'].strftime('%H:%M')}]")
    print(f"Sunrise     {times['sunrise'].strftime('%I:%M %p')}    [{times['sunrise'].strftime('%H:%M')}]")
    print(f"Dhuhr       {times['dhuhr'].strftime('%I:%M %p')}    [{times['dhuhr'].strftime('%H:%M')}]")
    print(f"Asr         {times['asr'].strftime('%I:%M %p')}    [{times['asr'].strftime('%H:%M')}]")
    print(f"Maghrib     {times['maghrib'].strftime('%I:%M %p')}    [{times['maghrib'].strftime('%H:%M')}]")
    print(f"Isha        {times['isha'].strftime('%I:%M %p')}    [{times['isha'].strftime('%H:%M')}]")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()