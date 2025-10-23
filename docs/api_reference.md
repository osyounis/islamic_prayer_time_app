<h3 align="center">
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ
</h3><br>

# API Reference

## Table of Contents

1. [Overview](#overview)
1. [Configuration Module](#configuration-module)
1. [Calculator Module](#calculator-module)
1. [Core Modules](#core-modules)
   - [Astronomy](#astronomy)
   - [Calendar](#calendar)
   - [Qibla](#qibla)
1. [Utility Modules](#utility-modules)
   - [Math Utils](#math-utils)
   - [Time Utils](#time-utils)
1. [Complete Usage Examples](#complete-usage-examples)

---

# Overview
This API reference documents all public functions and classes in the Islamic Prayer Time Calculator library.

**Package Structure:**
```
prayer_times/
├── config.py              # Configuration and constants
├── calculator/
│   └── calculator.py      # Main calculation orchestrator
├── core/
│   ├── astronomy.py       # Astronomical calculations
│   ├── calendar.py        # Calendar conversions
│   └── qibla.py           # Qibla direction
└── utils/
    ├── math_utils.py      # Mathematical utilities
    └── time_utils.py      # Time manipulation
```

---

## Configuration Module

### `prayer_times.config`
*Contains configuration settings, constants, and the `UserSettings` class.*

#### Constants:

##### `LAT_AL_KAABA`
```python
LAT_AL_KAABA = 21.4225
```
Latitude of the Kaaba in Mecca, Saudi Arabia.

##### `LNG_AL_KAABA`
```python
LNG_AL_KAABA = 39.8262
```
Longitude of the Kaaba in Mecca, Saudi Arabia.

##### `HIGH_LATITUDE_THRESHOLD`
```python
HIGH_LATITUDE_THRESHOLD = 48.5
```
Latitude threshold (in degrees) above an below which high latitude adjustments are applied.

##### `CALCULATION_METHODS`
```python
CALCULATION_METHODS = {
    'mwl': {...},
    'isna': {...},
    'egas': {...},
    'uqu': {...},
    'uisk': {...},
    'ut': {...},
    'lri': {...},
    'gulf': {...},
    'jakim': {...}
}
```
Dictionary containing all available calculation methods with their parameters.

##### `HIJRI_MONTHS`
```python
HIJRI_MONTHS = {
    1: {"en": "Muharram", "ar": "مُحَرَّم"},
    2: {"en": "Safar", "ar": "صَفَر"},
    # ... (months 3-12)
}
```
Dictionary mapping Hijri month numbers to their English and Arabic names.

---

#### `UserSettings` Class
User preferences for prayer time calculation.

**Constructor**:
```python
UserSettings(
    method: str = 'isna',
    asr_method: str = 'standard',
    hijri_correction: int = 0
)
```

**Parameters**:
- `method` (str): Calculation method key (e.g., 'isna', 'mwl', 'uqu')
- `asr_method` (str): 'standard' (Shafi'i/Maliki/Hanbali) or 'hanafi'
- `hijri_correction` (int): Days to adjust Hijri date (e.g., -1, 0, +1, +2)

**Attributes**:
- `calculation_method` (str): The selected calculation method
- `asr_method` (str): The selected Asr calculation method
- `hijri_correction` (int): The Hijri date adjustment

**Example**:
```python
from prayer_times.config import UserSettings

# Create settings for North America
settings = UserSettings(
    method='isna',
    asr_method='standard',
    hijri_correction=0
)

# Create settings for Hanafi calculation
hanafi_settings = UserSettings(
    method='mwl',
    asr_method='hanafi'
)
```

**Raises**:
- `ValueError`: If method key is invalid
- `ValueError`: If asr_method is not 'standard' or 'hanafi'

---

#### Helper Functions

##### `get_method_config(method_key: str) -> Dict[str, Any]`
Gets the complete configuration for a calculation method.

**Parameters**:
- `method_key` (str): The method key (e.g., 'isna', 'mwl')

**Returns**:
- `Dict[str, Any]`: Configuration dictionary containing fajr_angle, isha_angle, etc.

**Raises**:
- `ValueError`: If method_key is invalid

**Example**:
```python
from prayer_times.config import get_method_config

config = get_method_config('isna')
print(config['name'])  # "Islamic Society of North America"
print(config['fajr_angle'])  # 15.0
```

##### `get_method_name(method_key: str) -> str`
Gets the full name of a calculation method.

**Parameters**:
- method_key (str): The method key

**Returns**:
- str: Full name of the method

**Example**:
```python
from prayer_times.config import get_method_name

name = get_method_name('uqu')
print(name)  # "Umm al-Qura University, Makkah"
```

##### `get_fajr_angle(method_key: str) -> float`
Gets the Fajr angle for a calculation method.

***Parameters**:
- `method_key` (str): The method key

**Returns**:
- `float`: Fajr angle in degrees

**Example**:
```python
from prayer_times.config import get_fajr_angle

angle = get_fajr_angle('isna')
print(angle)  # 15.0
```

##### `get_isha_config(method_key: str) -> Dict[str, Any]`
Gets the Isha configuration (angle-based or fixed-time).

**Parameters**:
- `method_key` (str): The method key

**Returns**:
- `Dict[str, Any]`: Configuration dictionary with one of these formats:
- `Angle-based`: {'type': 'angle', 'angle': \<float\>}
- `Fixed-time`: {'type': 'fixed_time', 'offset_normal': \<int\>, 'offset_ramadan': \<int\>}

**Example**:
```python
from prayer_times.config import get_isha_config

# Angle-based method
config = get_isha_config('isna')
print(config)  # {'type': 'angle', 'angle': 15.0}

# Fixed-time method
config = get_isha_config('uqu')
print(config)  # {'type': 'fixed_time', 'offset_normal': 90, 'offset_ramadan': 120}
```

##### `list_all_methods() -> Dict[str, str]`
Gets all available calculation methods.

**Returns**:
- `Dict[str, str]`: Dictionary mapping method keys to their full names

**Example**:
```python
from prayer_times.config import list_all_methods

methods = list_all_methods()
for key, name in methods.items():
    print(f"{key}: {name}")
```

##### `get_hijri_month_name(month: int, language: str = 'en') -> str`
Gets the name of a Hijri month.

**Parameters**:
- `month` (int): Hijri month number (1-12)
- `language` (str): 'en' for English or 'ar' for Arabic

**Returns**:
- `str`: Month name in the specified language

**Raises**:
- `ValueError`: If month is not between 1-12
- `ValueError`: If language is not 'en' or 'ar'

**Example**:
```python
from prayer_times.config import get_hijri_month_name

print(get_hijri_month_name(9, 'en'))  # "Ramadan"
print(get_hijri_month_name(9, 'ar'))  # "رَمَضَان"
```

---

## Calculator Module

### `prayer_times.calculator.calculator`
Main calculation orchestrator that combines all components.

#### `calculate_prayer_times(latitude, longitude, elevation, date, settings)`
Calculates all prayer times and related information for a given location and date.

**Parameters**:
- `latitude` (float): Observer's latitude in degrees (-90 to 90)
- `longitude` (float): Observer's longitude in degrees (-180 to 180)
- `elevation` (float): Elevation above sea level in meters
- `date` (datetime): Date to calculate prayer times for
- `settings` (UserSettings): User configuration settings

**Returns**:
- `Dict[str, Any]`: Dictionary containing:
  - `'times_rounded'`: Dictionary of prayer times (datetime objects, rounded to nearest minute)
  - `'fajr'`, `'sunrise'`, `'dhuhr'`, `'asr'`, `'maghrib'`, `'isha'`
  - `'times_precise'`: Dictionary of prayer times (datetime objects, not rounded)
  - `'qibla'`: Qibla direction in degrees from North (float)
  - `'hijri_date'`: Dictionary with keys `'day'`, `'month'`, `'year'`

**Example**:
```python
from datetime import datetime
from prayer_times.config import UserSettings
from prayer_times.calculator.calculator import calculate_prayer_times

# Location: Fullerton, CA
latitude = 33.88
longitude = -117.928611
elevation = 50

# Settings
settings = UserSettings(method='isna', asr_method='standard')

# Calculate for today
date = datetime.now()
results = calculate_prayer_times(latitude, longitude, elevation, date, settings)

# Access rounded times
print(f"Fajr: {results['times_rounded']['fajr'].strftime('%I:%M %p')}")
print(f"Dhuhr: {results['times_rounded']['dhuhr'].strftime('%I:%M %p')}")
print(f"Asr: {results['times_rounded']['asr'].strftime('%I:%M %p')}")
print(f"Maghrib: {results['times_rounded']['maghrib'].strftime('%I:%M %p')}")
print(f"Isha: {results['times_rounded']['isha'].strftime('%I:%M %p')}")

# Access Qibla and Hijri date
print(f"Qibla: {results['qibla']:.2f}°")
print(f"Hijri Date: 
{results['hijri_date']['day']}/{results['hijri_date']['month']}/{results['hijri_date']['year']}")
```

---

## Core Modules

### Astronomy

#### `prayer_times.core.astronomy`
Astronomical calculations for sun position.

##### `sun_coordinates(j_date: float) -> Dict[str, float]`
Calculates sun position data needed for prayer times.

**Parameters**:
- `j_date` (float): Julian Date

**Returns**:
- `Dict[str, float]`: Dictionary containing:
  - `'solar_lng'`: Mean longitude (degrees)
  - `'mean_anomaly'`: Mean anomaly (degrees)
  - `'ecliptic_lng'`: Ecliptic longitude (degrees)
  - `'obliq_ecliptic'`: Obliquity of ecliptic (degrees)
  - `'ascension'`: Right ascension (degrees)
  - `'dist'`: Earth-Sun distance (AU)
  - `'declination'`: Declination (degrees)
  - `'semi_dia'`: Semi-diameter (degrees)

Example:
```python
from prayer_times.core.astronomy import sun_coordinates

sun_data = sun_coordinates(2451544.5)  # Jan 1, 2000
print(f"Declination: {sun_data['declination']:.2f}°")
```

---

### Calendar

#### `prayer_times.core.calendar`
Calendar conversion functions (Gregorian ↔ Julian ↔ Hijri).

##### `julian_date(date: datetime) -> float`
Converts a Gregorian date to Julian Date.

**Parameters**:
- `date` (datetime): Gregorian date

**Returns**:
- `float`: Julian Date (number of days since Jan 1, 4713 BC)

**Example**:
```python
from datetime import datetime
from prayer_times.core.calendar import julian_date

date = datetime(2000, 1, 1)
jd = julian_date(date)
print(f"Julian Date: {jd}")  # 2451544.5
```

##### `hijri_date(j_date: float, d_correction: int = 0) -> Dict[str, int]`
Converts a Julian Date to Hijri date.

**Parameters**:
- `j_date` (float): Julian Date
- `d_correction` (int): Days to adjust the calculated date

**Returns**:
- `Dict[str, int]`: Dictionary with keys `'day'`, `'month'`, `'year'`

**Example**:
```python
from prayer_times.core.calendar import hijri_date

j_date = 2451544.5  # Jan 1, 2000
hijri = hijri_date(j_date)
print(f"{hijri['day']}/{hijri['month']}/{hijri['year']}")  # 24/9/1420
```

---

### Qibla

#### `prayer_times.core.qibla`
Qibla direction calculation.

##### `qibla_direction(your_latitude: float, your_longitude: float) -> float`
Calculates the Qibla bearing direction.

**Parameters**:
- `your_latitude` (float): Observer's latitude in degrees (North positive, South negative)
- `your_longitude` (float): Observer's longitude in degrees (East positive, West negative)

**Returns**:
- `float`: Bearing in degrees from true North (0-360), rounded to 2 decimal places

Example:
```python
from prayer_times.core.qibla import qibla_direction

# New York City
qibla = qibla_direction(40.7128, -74.0060)
print(f"Qibla direction: {qibla}°")  # 58.48°

# Fullerton, CA
qibla = qibla_direction(33.88, -117.928611)
print(f"Qibla direction: {qibla}°")  # ~24.81°
```

---

## Utility Modules

### Math Utils

#### `prayer_times.utils.math_utils`
Mathematical utility functions (degree-based trigonometry).

All trigonometric functions work with degrees instead of radians.

> ##### `dsin(degrees: float) -> float`
> Sine function using degrees.
> 
> Example:
> ```python
> from prayer_times.utils.math_utils import dsin
> 
> result = dsin(30)
> print(result)  # 0.5
> ```

> ##### `dcos(degrees: float) -> float`
> Cosine function using degrees.

> ##### `dcot(degrees: float) -> float`
> Cotangent function using degrees.
>
> Raises:
> - `ZeroDivisionError`: If angle is 0° or 180° (where cot is undefined)

> ##### `dasin(value: float) -> float`
> Arcsine function returning degrees.

> ##### `dacos(value: float) -> float`
> Arccosine function returning degrees.

> ##### `dacot(value: float) -> float`
> Arccotangent function returning degrees.
>
> Returns:
> - Values in range [0°, 180°]
> - Returns 90° when value is 0

> ##### `datan2(y: float, x: float) -> float`
> Two-argument arctangent function returning degrees.
>
> Returns:
> - Bearing angle in range [0°, 360°]

---

### Time Utils

#### prayer_times.utils.time_utils
Time conversion and formatting utilities.

##### `round_time(timestamp: datetime) -> datetime`
Rounds a timestamp to the nearest minute.

Parameters:
- `timestamp` (datetime): Timestamp to round

Returns:
- `datetime`: Rounded timestamp (seconds and microseconds set to 0)

Example:
```python
from datetime import datetime
from prayer_times.utils.time_utils import round_time

timestamp = datetime(2025, 1, 15, 5, 23, 45)
rounded = round_time(timestamp)
print(rounded)  # 2025-01-15 05:24:00
```

---

## Complete Usage Example

### Example 1: Basic Prayer Times
```python
from datetime import datetime
from prayer_times.config import UserSettings
from prayer_times.calculator.calculator import calculate_prayer_times

# Your location
latitude = 33.88
longitude = -117.928611
elevation = 50

# Settings
settings = UserSettings(method='isna')

# Calculate
date = datetime.now()
results = calculate_prayer_times(latitude, longitude, elevation, date, settings)

# Display
times = results['times_rounded']
print(f"Fajr:    {times['fajr'].strftime('%I:%M %p')}")
print(f"Sunrise: {times['sunrise'].strftime('%I:%M %p')}")
print(f"Dhuhr:   {times['dhuhr'].strftime('%I:%M %p')}")
print(f"Asr:     {times['asr'].strftime('%I:%M %p')}")
print(f"Maghrib: {times['maghrib'].strftime('%I:%M %p')}")
print(f"Isha:    {times['isha'].strftime('%I:%M %p')}")
```

### Example 2: Different Calculation Methods
```python
from datetime import datetime
from prayer_times.config import UserSettings
from prayer_times.calculator.calculator import calculate_prayer_times

location = (33.88, -117.928611, 50)  # lat, lng, elevation
date = datetime.now()

methods = ['isna', 'mwl', 'egas', 'uqu']

for method in methods:
    settings = UserSettings(method=method)
    results = calculate_prayer_times(*location, date, settings)

    print(f"\n{method.upper()} Method:")
    print(f"  Fajr: {results['times_rounded']['fajr'].strftime('%I:%M %p')}")
    print(f"  Isha: {results['times_rounded']['isha'].strftime('%I:%M %p')}")
```

### Example 3: Hanafi Asr Calculation
```python
from datetime import datetime
from prayer_times.config import UserSettings
from prayer_times.calculator.calculator import calculate_prayer_times

location = (33.88, -117.928611, 50)
date = datetime.now()

# Standard Asr
standard = UserSettings(method='isna', asr_method='standard')
results_std = calculate_prayer_times(*location, date, standard)

# Hanafi Asr
hanafi = UserSettings(method='isna', asr_method='hanafi')
results_hanafi = calculate_prayer_times(*location, date, hanafi)

print(f"Standard Asr: {results_std['times_rounded']['asr'].strftime('%I:%M %p')}")
print(f"Hanafi Asr:   {results_hanafi['times_rounded']['asr'].strftime('%I:%M %p')}")
```

### Example 4: Monthly Prayer Times
```python
from datetime import datetime, timedelta
from prayer_times.config import UserSettings
from prayer_times.calculator.calculator import calculate_prayer_times

location = (33.88, -117.928611, 50)
settings = UserSettings(method='isna')

# Calculate for entire month
date = datetime(2025, 3, 1)
print("March 2025 Prayer Times:")
print("-" * 60)

for day in range(1, 32):
    try:
        current_date = datetime(2025, 3, day)
        results = calculate_prayer_times(*location, current_date, settings)
        times = results['times_rounded']

        print(f"{current_date.strftime('%b %d')}: "
            f"Fajr {times['fajr'].strftime('%I:%M %p')}, "
            f"Dhuhr {times['dhuhr'].strftime('%I:%M %p')}, "
            f"Maghrib {times['maghrib'].strftime('%I:%M %p')}")
    except ValueError:
        break  # Month ended
```

### Example 5: Qibla Direction Only
```python
from prayer_times.core.qibla import qibla_direction

cities = {
    'New York': (40.7128, -74.0060),
    'London': (51.5074, -0.1278),
    'Tokyo': (35.6762, 139.6503),
    'Sydney': (-33.8688, 151.2093),
}

for city, (lat, lng) in cities.items():
    qibla = qibla_direction(lat, lng)
    print(f"{city}: {qibla:.2f}° from North")
```

### Example 6: Hijri Calendar Conversion
```python
from datetime import datetime
from prayer_times.core.calendar import julian_date, hijri_date
from prayer_times.config import get_hijri_month_name

# Convert today to Hijri
date = datetime.now()
jd = julian_date(date)
hijri = hijri_date(jd)

month_name_en = get_hijri_month_name(hijri['month'], 'en')
month_name_ar = get_hijri_month_name(hijri['month'], 'ar')

print(f"Gregorian: {date.strftime('%B %d, %Y')}")
print(f"Hijri: {month_name_en} {hijri['day']}, {hijri['year']} AH")
print(f"Arabic: {month_name_ar} {hijri['day']}, {hijri['year']}")
```

---

**For more information, see [`/docs/calculation_methodolgy.md`](https://github.com/osyounis/islamic_prayer_time_app/blob/main/docs/calculation_methodology.md).**

---