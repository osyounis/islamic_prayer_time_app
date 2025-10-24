"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Multiple Locations Example - Islamic Prayer Time Calculator

This example shows how to calculate prayer times for multiple cities 
around the world.

Author: Omar Younis
Date: 22/10/2025 [dd/mm/yyyy]

"""

from datetime import datetime
from prayer_times.config import UserSettings
from prayer_times.calculator.calculator import calculate_prayer_times


# Define cities with their coordinates
CITIES = {
    'Mecca, Saudi Arabia': {
        'lat': 21.4225,
        'lng': 39.8262,
        'elevation': 277,
        'method': 'uqu'  # Umm al-Qura University
    },
    'New York, USA': {
        'lat': 40.7128,
        'lng': -74.0060,
        'elevation': 10,
        'method': 'isna'  # Islamic Society of North America
    },
    'London, UK': {
        'lat': 51.5074,
        'lng': -0.1278,
        'elevation': 11,
        'method': 'mwl'  # Muslim World League
    },
    'Cairo, Egypt': {
        'lat': 30.0444,
        'lng': 31.2357,
        'elevation': 23,
        'method': 'egas'  # Egyptian General Authority of Survey
    },
    'Karachi, Pakistan': {
        'lat': 24.8607,
        'lng': 67.0011,
        'elevation': 10,
        'method': 'uisk'  # University of Islamic Sciences, Karachi
    },
    'Kuala Lumpur, Malaysia': {
        'lat': 3.1390,
        'lng': 101.6869,
        'elevation': 22,
        'method': 'jakim'  # JAKIM
    },
}


def main() -> None:
    """
    Calculate and display prayer times for multiple cities.
    """
    date = datetime.now().astimezone()

    print("\n" + "="*90)
    print(f"Prayer Times Around the World - {date.strftime('%B %d, %Y')}")
    print("="*90 + "\n")

    for city, info in CITIES.items():
        # Create settings for this city
        settings = UserSettings(method=info['method'], asr_method='standard')

        # Calculate prayer times
        results = calculate_prayer_times(
            info['lat'],
            info['lng'],
            info['elevation'],
            date,
            settings
        )

        times = results['times_rounded']
        qibla = results['qibla']

        # Display results
        print(f"{city}")
        print(f"  Coordinates: {info['lat']}°, {info['lng']}°")
        print(f"  Method: {info['method'].upper()}")
        print(f"  Qibla: {qibla:.1f}°")
        print(f"  Fajr: {times['fajr'].strftime('%I:%M %p')} | "
            f"Dhuhr: {times['dhuhr'].strftime('%I:%M %p')} | "
            f"Asr: {times['asr'].strftime('%I:%M %p')} | "
            f"Maghrib: {times['maghrib'].strftime('%I:%M %p')} | "
            f"Isha: {times['isha'].strftime('%I:%M %p')}")
        print()

    print("="*90 + "\n")


if __name__ == '__main__':
    main()
