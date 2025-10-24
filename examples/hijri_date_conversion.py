"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Hijri Date Conversion Example - Islamic Prayer Time Calculator

This example shows how to convert dates between Gregorian and Hijri calendars.

Author: Omar Younis
Date: 22/10/2025 [dd/mm/yyyy]

"""


from datetime import datetime
from prayer_times.core.calendar import julian_date, hijri_date
from prayer_times.config import get_hijri_month_name


def main() -> None:
    """
    Demonstrate Hijri calendar conversion.
    """

    print("\n" + "="*80)
    print("Hijri Calendar Conversion Examples")
    print("="*80 + "\n")

    # Example 1: Convert today's date
    print("Example 1: Today's Date")
    print("-"*80)
    convert_and_display(datetime.now().astimezone())
    print()

    # Example 2: Convert a specific date
    print("Example 2: Specific Date (January 1, 2025)")
    print("-"*80)
    convert_and_display(datetime(2025, 1, 1))
    print()

    # Example 3: Show all Hijri months
    print("Example 3: All Hijri Months")
    print("-"*80)
    display_all_months()
    print()

    # Example 4: Effect of correction factor
    print("Example 4: Effect of Correction Factor")
    print("-"*80)
    demonstrate_correction()

    print("="*80 + "\n")


def convert_and_display(date, correction=0) -> None:
    """
    Convert a Gregorian date to Hijri and display both.
    
    Args:
        date (datetime): Gregorian date
        correction (int): Hijri correction factor
    """
    # Convert to Julian Day
    jd = julian_date(date)

    # Convert to Hijri
    hijri = hijri_date(jd, d_correction=correction)

    # Get month names
    month_en = get_hijri_month_name(hijri['month'], 'en')
    month_ar = get_hijri_month_name(hijri['month'], 'ar')

    # Display
    print(f"  Gregorian: {date.strftime('%A, %B %d, %Y')}")
    print(f"  Hijri:     {month_en} {hijri['day']}, {hijri['year']} AH")
    print(f"  Arabic:    {month_ar} {hijri['day']}, {hijri['year']}")

    if correction != 0:
        print(f"  (with correction: {correction:+d} day{'s' if abs(correction) > 1 else ''})")


def display_all_months() -> None:
    """
    Display all 12 Hijri months.
    """
    print(f"  {'#':<5} {'English Name':<25} {'Arabic Name':<25}")
    print("  " + "-"*55)

    for month_num in range(1, 13):
        en_name = get_hijri_month_name(month_num, 'en')
        ar_name = get_hijri_month_name(month_num, 'ar')
        print(f"  {month_num:<5} {en_name:<25} {ar_name:<25}")


def demonstrate_correction() -> None:
    """
    Show how the correction factor affects the date.
    """
    date = datetime.now().astimezone()
    jd = julian_date(date)

    print(f"  Date: {date.strftime('%B %d, %Y')}")
    print(f"  Julian Day: {jd}\n")

    for correction in [-2, -1, 0, +1, +2]:
        hijri = hijri_date(jd, d_correction=correction)
        month_en = get_hijri_month_name(hijri['month'], 'en')

        correction_str = f"({correction:+d})"
        print(f"  Correction {correction_str:>7}: {month_en} {hijri['day']}, {hijri['year']} AH")


if __name__ == '__main__':
    main()
