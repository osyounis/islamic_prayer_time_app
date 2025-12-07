#!/usr/bin/env python3
"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Command-Line Interface for Islamic Prayer Time Calculator

This module provides a command-line interface for calculating prayer times
with support for custom angles for research purposes.

Author: Omar Younis
Date: 07/12/2024 [dd/mm/yyyy]
"""

import argparse
import sys
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from typing import Optional

from prayer_times.calculator.calculator import calculate_prayer_times
from prayer_times.config import (
    UserSettings,
    CALCULATION_METHODS,
    HIJRI_MONTHS
)


def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures the argument parser.

    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog='prayer-times',
        description='Calculate Islamic prayer times for any location',
        epilog='For more information, visit: https://github.com/osyounis/islamic_prayer_time_app',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Position arguments (required unless using --list-methods)
    parser.add_argument(
        'latitude',
        type=float,
        nargs='?',
        help='Latitude in degrees (-90 to 90, positive for North)'
    )
    parser.add_argument(
        'longitude',
        type=float,
        nargs='?',
        help='Longitude in degrees (-180 to 180, positive for East)'
    )

    # Location arguments
    location = parser.add_argument_group('location settings')
    location.add_argument(
        '-e', '--elevation',
        type=float,
        default=0,
        metavar='METERS',
        help='Elevation in meters above sea level (default: 0)'
    )
    location.add_argument(
        '-z', '--timezone',
        type=str,
        metavar='TZ',
        help='IANA timezone (e.g., America/New_York, Asia/Dubai). '
             'If not provided, uses system local timezone.'
    )

    # Date arguments
    date_group = parser.add_argument_group('date settings')
    date_group.add_argument(
        '-d', '--date',
        type=str,
        metavar='YYYY-MM-DD',
        help='Date to calculate (ISO 8601 format: YYYY-MM-DD). '
             'Default: today'
    )

    # Calculation method arguments
    calc = parser.add_argument_group('calculation methods')
    calc.add_argument(
        '-m', '--method',
        type=str,
        default='isna',
        choices=list(CALCULATION_METHODS.keys()),
        metavar='METHOD',
        help=f'Calculation method. Options: {", ".join(CALCULATION_METHODS.keys())}. '
             f'Default: isna'
    )
    calc.add_argument(
        '-a', '--asr-method',
        type=str,
        default='standard',
        choices=['standard', 'hanafi'],
        metavar='ASR',
        help='Asr calculation method: standard or hanafi (default: standard)'
    )
    calc.add_argument(
        '--hijri-correction',
        type=int,
        default=0,
        metavar='DAYS',
        help='Days to adjust Hijri date (+ or -) (default: 0)'
    )

    # Custom angle arguments (for research)
    custom = parser.add_argument_group('custom angles (research)')
    custom.add_argument(
        '--fajr-angle',
        type=float,
        metavar='DEGREES',
        help='Custom Fajr angle in degrees (overrides method default). '
             'Valid range: 0-30 degrees.'
    )
    custom.add_argument(
        '--isha-angle',
        type=float,
        metavar='DEGREES',
        help='Custom Isha angle in degrees (overrides method default). '
             'Valid range: 0-30 degrees. Cannot use with --isha-interval.'
    )
    custom.add_argument(
        '--isha-interval',
        type=int,
        metavar='MINUTES',
        help='Fixed Isha time (minutes after Maghrib). '
             'Valid range: 0-240 minutes. Cannot use with --isha-angle.'
    )

    # Information arguments
    parser.add_argument(
        '--list-methods',
        action='store_true',
        help='List all available calculation methods and exit'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='Islamic Prayer Time Calculator v0.1.0'
    )

    return parser


def validate_coordinates(lat: float, lng: float) -> None:
    """
    Validates latitude and longitude values.

    Args:
        lat (float): Latitude
        lng (float): Longitude

    Raises:
        ValueError: If coordinates are out of valid range
    """
    if not (-90 <= lat <= 90):
        raise ValueError(
            f"Invalid latitude: {lat}. Must be between -90 and 90 degrees."
        )
    if not (-180 <= lng <= 180):
        raise ValueError(
            f"Invalid longitude: {lng}. Must be between -180 and 180 degrees."
        )


def parse_date(date_str: str, timezone_str: Optional[str] = None) -> datetime:
    """
    Parses ISO 8601 date string and creates timezone-aware datetime.

    Args:
        date_str (str): Date in YYYY-MM-DD format
        timezone_str (Optional[str]): IANA timezone name

    Returns:
        datetime: Timezone-aware datetime at midnight

    Raises:
        ValueError: If date format is invalid
        ZoneInfoNotFoundError: If timezone is invalid
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError(
            f"Invalid date format: '{date_str}'. "
            f"Use ISO 8601 format: YYYY-MM-DD (e.g., 2025-01-15)"
        )

    # Make timezone-aware
    if timezone_str:
        try:
            tz = ZoneInfo(timezone_str)
        except ZoneInfoNotFoundError:
            raise ZoneInfoNotFoundError(
                f"Invalid timezone: '{timezone_str}'. "
                f"Use IANA timezone names (e.g., America/New_York, Asia/Dubai)"
            )
        return date_obj.replace(tzinfo=tz)
    else:
        # Use system local timezone
        now = datetime.now().astimezone()
        return now.replace(
            year=date_obj.year,
            month=date_obj.month,
            day=date_obj.day,
            hour=0, minute=0, second=0, microsecond=0
        )


def format_output(results: dict, settings: UserSettings,
                 lat: float, lng: float, elev: float) -> str:
    """
    Formats prayer time results as a human-readable table.

    Args:
        results (dict): Results from calculate_prayer_times()
        settings (UserSettings): User settings used
        lat (float): Latitude
        lng (float): Longitude
        elev (float): Elevation

    Returns:
        str: Formatted output string
    """
    times = results['times_rounded']
    qibla = results['qibla']
    date = results['gregorian_date']
    hij_date = results['hijri_date']

    method_name = CALCULATION_METHODS[settings.calculation_method]['name']
    method_key = settings.calculation_method.upper()

    output = f"""
╔════════════════════════════════════════════════════════════╗
║              Islamic Prayer Time Calculator                ║
╚════════════════════════════════════════════════════════════╝
📍 Location
    Latitude:  {lat}°
    Longitude: {lng}°
    Elevation: {elev}m

🕋 Qibla Direction: {qibla:06.2f}°  (from North)

📅 Gregorian Date:  {date.strftime("%A, %B %d, %Y")}

🌒 Hijri Date:  {HIJRI_MONTHS[hij_date["month"]]['en']} {hij_date['day']}, {hij_date['year']} AH
                {HIJRI_MONTHS[hij_date["month"]]['ar']} {hij_date['day']}, {hij_date['year']}

⚙️  Calculation Method: {method_name} ({method_key})
⚙️  Asr Method: {settings.asr_method.capitalize()}"""

    # Add custom angle info if used
    if settings.fajr_angle is not None:
        output += f"\n⚙️  Custom Fajr Angle: {settings.fajr_angle}°"
    if settings.isha_angle is not None:
        output += f"\n⚙️  Custom Isha Angle: {settings.isha_angle}°"
    if settings.isha_interval is not None:
        output += f"\n⚙️  Custom Isha Interval: {settings.isha_interval} min after Maghrib"

    output += f"""

🕌 Prayer Times
══════════════════════════════════════
Fajr        {times['fajr'].strftime("%I:%M %p")}    [{times['fajr'].strftime("%H:%M")}]
Sunrise     {times['sunrise'].strftime("%I:%M %p")}    [{times['sunrise'].strftime("%H:%M")}]
Dhuhr       {times['dhuhr'].strftime("%I:%M %p")}    [{times['dhuhr'].strftime("%H:%M")}]
Asr         {times['asr'].strftime("%I:%M %p")}    [{times['asr'].strftime("%H:%M")}]
Maghrib     {times['maghrib'].strftime("%I:%M %p")}    [{times['maghrib'].strftime("%H:%M")}]
Isha        {times['isha'].strftime("%I:%M %p")}    [{times['isha'].strftime("%H:%M")}]
══════════════════════════════════════
"""
    return output


def list_methods() -> str:
    """
    Creates formatted list of all calculation methods.

    Returns:
        str: Formatted method list
    """
    output = "\nAvailable Calculation Methods:\n"
    output += "=" * 80 + "\n"

    for key, config in CALCULATION_METHODS.items():
        output += f"\n{key.upper():8s} - {config['name']}\n"
        output += f"         Fajr: {config['fajr_angle']}°"

        if config['isha_type'] == 'angle':
            output += f", Isha: {config['isha_angle']}°\n"
        else:
            output += f", Isha: {config['isha_offset_normal']} min after Maghrib"
            if config['isha_offset_ramadan'] != config['isha_offset_normal']:
                output += f" ({config['isha_offset_ramadan']} min in Ramadan)"
            output += "\n"

    output += "\n" + "=" * 80 + "\n"
    return output


def main(argv=None) -> int:
    """
    Main CLI entry point.

    Args:
        argv: Command-line arguments (for testing)

    Returns:
        int: Exit code (0 = success, 1 = error)
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        # Handle --list-methods
        if args.list_methods:
            print(list_methods())
            return 0

        # Check that latitude and longitude are provided
        if args.latitude is None or args.longitude is None:
            parser.error("the following arguments are required: latitude, longitude")

        # Validate coordinates
        validate_coordinates(args.latitude, args.longitude)

        # Parse date
        if args.date:
            date = parse_date(args.date, args.timezone)
        else:
            # Use today's date
            if args.timezone:
                try:
                    tz = ZoneInfo(args.timezone)
                    date = datetime.now(tz)
                except ZoneInfoNotFoundError:
                    raise ZoneInfoNotFoundError(
                        f"Invalid timezone: '{args.timezone}'. "
                        f"Use IANA timezone names (e.g., America/New_York)"
                    )
            else:
                date = datetime.now().astimezone()

        # Create UserSettings
        settings = UserSettings(
            method=args.method,
            asr_method=args.asr_method,
            hijri_correction=args.hijri_correction,
            fajr_angle=args.fajr_angle,
            isha_angle=args.isha_angle,
            isha_interval=args.isha_interval
        )

        # Calculate prayer times
        results = calculate_prayer_times(
            args.latitude,
            args.longitude,
            args.elevation,
            date,
            settings
        )

        # Format and print output
        output = format_output(results, settings, args.latitude,
                             args.longitude, args.elevation)
        print(output)

        return 0

    except (ValueError, ZoneInfoNotFoundError) as e:
        print(f"\nError: {e}\n", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {e}\n", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
