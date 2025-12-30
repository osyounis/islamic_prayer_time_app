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
import traceback

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

    # Reverse calculation arguments
    reverse = parser.add_argument_group('reverse calculation (research)')
    reverse.add_argument(
        '--reverse',
        action='store_true',
        help='Enable reverse calculation mode (calculate angles from observed times)'
    )
    reverse.add_argument(
        '--fajr-time',
        type=str,
        metavar='HH:MM',
        help='Observed Fajr time in HH:MM format (24-hour, required with --reverse)'
    )
    reverse.add_argument(
        '--maghrib-time',
        type=str,
        metavar='HH:MM',
        help='Observed Maghrib time in HH:MM format (24-hour, required with --reverse)'
    )
    reverse.add_argument(
        '--isha-time',
        type=str,
        metavar='HH:MM',
        help='Observed Isha time in HH:MM format (24-hour, required with --reverse)'
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
    if not -90 <= lat <= 90:
        raise ValueError(
            f"Invalid latitude: {lat}. Must be between -90 and 90 degrees."
        )
    if not -180 <= lng <= 180:
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
    except ValueError as exc:
        raise ValueError(
            f"Invalid date format: '{date_str}'. "
            f"Use ISO 8601 format: YYYY-MM-DD (e.g., 2025-01-15)"
        ) from exc

    # Make timezone-aware
    if timezone_str:
        try:
            tz = ZoneInfo(timezone_str)
        except ZoneInfoNotFoundError as exc:
            raise ZoneInfoNotFoundError(
                f"Invalid timezone: '{timezone_str}'. "
                f"Use IANA timezone names (e.g., America/New_York, Asia/Dubai)"
            ) from exc
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


def parse_time_string(time_str: str, date: datetime) -> datetime:
    """
    Parses HH:MM time string and combines with date.

    Args:
        time_str (str): Time in HH:MM format (24-hour)
        date (datetime): Date to combine with (must be timezone-aware)

    Returns:
        datetime: Combined date and time (timezone-aware)

    Raises:
        ValueError: If time format is invalid
    """
    try:
        hour, minute = map(int, time_str.split(':'))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Hour must be 0-23, minute must be 0-59")
        return date.replace(hour=hour, minute=minute, second=0, microsecond=0)
    except (ValueError, AttributeError) as exc:
        raise ValueError(
            f"Invalid time format: '{time_str}'. Use HH:MM format (24-hour), "
            f"e.g., 05:30 or 18:15"
        ) from exc


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


def format_reverse_output(results: dict, lat: float, lng: float, elev: float,
                         fajr_time: str, maghrib_time: str, isha_time: str,
                         date: datetime) -> str:
    """
    Formats reverse calculation results as human-readable output.

    Args:
        results (dict): Results from ReversePrayerCalculator.reverse_calculate()
        lat (float): Latitude
        lng (float): Longitude
        elev (float): Elevation
        fajr_time (str): Input Fajr time string
        maghrib_time (str): Input Maghrib time string
        isha_time (str): Input Isha time string
        date (datetime): Date of calculation

    Returns:
        str: Formatted output string
    """
    output = f"""
╔════════════════════════════════════════════════════════════╗
║         Islamic Prayer Time Reverse Calculator             ║
╚════════════════════════════════════════════════════════════╝
📍 Location
    Latitude:  {lat}°
    Longitude: {lng}°
    Elevation: {elev}m

📅 Date: {date.strftime("%A, %B %d, %Y")}

⏰ Input Prayer Times
══════════════════════════════════════
Fajr        {fajr_time}
Maghrib     {maghrib_time}
Isha        {isha_time}
══════════════════════════════════════

📐 Calculated Angles
══════════════════════════════════════
Fajr Angle:     {results['fajr_angle']:6.2f}° below horizon"""

    # Add method info if high latitude
    if results['fajr_method'] == 'high_latitude':
        output += " (Angle-Based Rule)"

    output += f"""
Isha Angle:     {results['isha_angle']:6.2f}° below horizon"""

    if results['isha_method'] == 'high_latitude':
        output += " (Angle-Based Rule)"

    output += f"""
Isha Interval:  {results['isha_minutes']:6.1f} minutes after Maghrib
══════════════════════════════════════

📊 Astronomical Data
══════════════════════════════════════
Solar Noon:     {results['midday'].strftime("%I:%M:%S %p")}  [{results['midday'].strftime("%H:%M:%S")}]
Sunrise:        {results['sunrise'].strftime("%I:%M:%S %p")}  [{results['sunrise'].strftime("%H:%M:%S")}]
══════════════════════════════════════
"""

    # Add warnings if any
    if results['warnings']:
        output += "\n⚠️  Warnings:\n"
        for warning in results['warnings']:
            output += f"  • {warning}\n"
        output += "\n"

    # Add interpretation help
    output += """
💡 Interpretation:
  These angles represent the Sun's position below the horizon at the
  observed prayer times. You can use these to identify which calculation
  method best matches your local mosque's times.

  Common methods for comparison:
    ISNA:  Fajr 15°, Isha 15°
    MWL:   Fajr 18°, Isha 17°
    EGAS:  Fajr 19.5°, Isha 17.5°
    UQU:   Fajr 18.5°, Isha 90 min after Maghrib
"""

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

        # Handle reverse mode
        if args.reverse:
            # Validate timezone is provided
            if not args.timezone:
                parser.error("--timezone is required when using --reverse")

            # Validate all times are provided
            if not all([args.fajr_time, args.maghrib_time, args.isha_time]):
                parser.error(
                    "--fajr-time, --maghrib-time, and --isha-time are "
                    "required with --reverse"
                )

            # Validate coordinates
            validate_coordinates(args.latitude, args.longitude)

            # Parse date
            if args.date:
                date = parse_date(args.date, args.timezone)
            else:
                # Use today's date
                try:
                    tz = ZoneInfo(args.timezone)
                    date = datetime.now(tz)
                except ZoneInfoNotFoundError as exc:
                    raise ZoneInfoNotFoundError(
                        f"Invalid timezone: '{args.timezone}'. "
                        f"Use IANA timezone names (e.g., America/New_York)"
                    ) from exc

            # Parse time strings
            fajr_time = parse_time_string(args.fajr_time, date)
            maghrib_time = parse_time_string(args.maghrib_time, date)
            isha_time = parse_time_string(args.isha_time, date)

            # Create reverse calculator
            from prayer_times.calculator.reverse_calculator import ReversePrayerCalculator
            calc = ReversePrayerCalculator(
                args.latitude, args.longitude, args.elevation
            )

            # Perform reverse calculation
            results = calc.reverse_calculate(
                date, fajr_time, maghrib_time, isha_time
            )

            # Format and print output
            output = format_reverse_output(
                results, args.latitude, args.longitude, args.elevation,
                args.fajr_time, args.maghrib_time, args.isha_time, date
            )
            print(output)

            return 0

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
                except ZoneInfoNotFoundError as exc:
                    raise ZoneInfoNotFoundError(
                        f"Invalid timezone: '{args.timezone}'. "
                        f"Use IANA timezone names (e.g., America/New_York)"
                    ) from exc
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
    except Exception as e:  # pylint: disable=broad-except
        # Catch any unexpected errors to provide graceful CLI error handling
        # rather than crashing with a raw traceback
        print(f"\nUnexpected error: {e}\n", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
