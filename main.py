"""
  بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

Islamic Prayer Time Calculator - Main Code

This is the main code to run the prayer time calculator. Edit the configuration
section below to set your location and preferences. You can run the file by
using:

    `python3 main.py`

Author: Omar Younis
Date: 20/10/2025 [dd/mm/yyyy]
"""

from datetime import datetime, timedelta
from prayer_times.config import UserSettings, CALCULATION_METHODS, HIJRI_MONTHS
from prayer_times.calculator.calculator import calculate_prayer_times


def main():
    """
    Main Function - configure your settings here and run calculations.
    """
    
    #======================================================================#
    #                          USER CONFIGURATION                          #
    #======================================================================#
    # Change these values for your location and preferences

    # Your geographic data (coordinates and elevation)
    LATITUDE = 33.88                # Fullerton, CA (positive = North)
    LONGITUDE = -117.928611         # (negative = West)
    ELEVATION = 50                  # meters above sea level

    # Your prayer calculation preferences
    settings = UserSettings(
        method='isna',              # Options: isna, mwl, uqu, ...
        asr_method='standard',      # Options: standard, hanafi
        hijri_correction=2          # Days to adjust Hijri date (+ or -)
    )

    # Date to calculate (0 = today, 1 = tomorrow, -1 = yesterday)
    DAY_OFFSET = 0

    #======================================================================#
    #                          CALCULATION                                 #
    #======================================================================#
    date = datetime.now() + timedelta(days=DAY_OFFSET)
    print()

    results = calculate_prayer_times(LATITUDE, LONGITUDE, ELEVATION, date, settings)

    #======================================================================#
    #                        DISPLAY RESULTS                               #
    #======================================================================#
    qibla = results['qibla']
    hij_date = results['hijri_date']
    times = results['times_rounded']

    method_name = CALCULATION_METHODS[settings.calculation_method]['name']
    method_key = settings.calculation_method.upper()

    # Format the output
    prayer_message = f"""
╔════════════════════════════════════════════════════════════╗
║              Islamic Prayer Time Calculator                ║
╚════════════════════════════════════════════════════════════╝
📍 Location
    Latitude:  {LATITUDE}\u00b0
    Longitude: {LONGITUDE}\u00b0
    Elevation: {ELEVATION}m

🕋 Qibla Direction: {qibla:06.2f}\u00b0  (from North)

📅 Gregorian Date:  {date.strftime("%A, %B %d, %Y")}

🌒 Hijri Date:  {HIJRI_MONTHS[hij_date["month"]]['en']} {hij_date['day']}, {hij_date['year']} AH
                {HIJRI_MONTHS[hij_date["month"]]['ar']} {hij_date['day']}, {hij_date['year']}

⚙️  Calculation Method: {method_name} ({method_key})
⚙️  Asr Method: {settings.asr_method.capitalize()}

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
    # Printing Messages
    print(prayer_message)
    print()

#===============================================================================
#                               Main Code
#===============================================================================
if __name__ == '__main__':
    main()
