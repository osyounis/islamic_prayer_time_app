"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Qibla Direction Example - Islamic Prayer Time Calculator

This example calculates the Qibla direction for various locations.

Author: Omar Younis
Date: 22/10/2025 [dd/mm/yyyy]

"""


from prayer_times.core.qibla import qibla_direction


def main():
    """
    Calculate Qibla direction for various cities.
    """
    # Cities with their coordinates
    cities = {
        'Mecca, Saudi Arabia': (21.4225, 39.8262),
        'Medina, Saudi Arabia': (24.5247, 39.5692),
        'New York, USA': (40.7128, -74.0060),
        'Los Angeles, USA': (34.0522, -118.2437),
        'London, UK': (51.5074, -0.1278),
        'Paris, France': (48.8566, 2.3522),
        'Cairo, Egypt': (30.0444, 31.2357),
        'Istanbul, Turkey': (41.0082, 28.9784),
        'Karachi, Pakistan': (24.8607, 67.0011),
        'Jakarta, Indonesia': (-6.2088, 106.8456),
        'Tokyo, Japan': (35.6762, 139.6503),
        'Sydney, Australia': (-33.8688, 151.2093),
        'Toronto, Canada': (43.6532, -79.3832),
    }

    print("\n" + "="*70)
    print("Qibla Direction from Various Cities")
    print("="*70 + "\n")

    print(f"{'City':<30} {'Coordinates':<25} {'Qibla':<15}")
    print("-"*70)

    for city, (lat, lng) in cities.items():
        # Calculate Qibla
        qibla = qibla_direction(lat, lng)

        # Format coordinates
        lat_str = f"{abs(lat):.2f}°{'N' if lat >= 0 else 'S'}"
        lng_str = f"{abs(lng):.2f}°{'E' if lng >= 0 else 'W'}"
        coords = f"{lat_str}, {lng_str}"

        # Print
        print(f"{city:<30} {coords:<25} {qibla:>6.2f}°")

    print("="*70 + "\n")


if __name__ == '__main__':
    main()
