<h3 align="center">
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ
</h3><br>

# Islamic Prayer Time App
A Python approach for calculating Islamic prayer times and Qibla direction based on astronomical calculations.

[![Tests](https://github.com/osyounis/islamic_prayer_time_app/actions/workflows/tests.yml/badge.svg)](https://github.com/osyounis/islamic_prayer_time_app/actions/workflows/tests.yml)

---

## 📖 Overview
This project calculates the five daily Islamic prayer times (Fajr, Dhuhr, Asr, Maghrib, and Isha). It also calculates when sunrise is as well as the Qibla direction (the direction to pray) for any location on Earth. These calculations are based on astronomical algorithms and support multiple calculation methods used by different Islamic organizations around the world.

This project also attempts to explain how these calculations are done.

**Main Features:**
- 🕌 Calculates all five prayers times and sunrise.
- 🕋 Calculates the Qibla direction for any location.
- 📅 Convert between Gregorian and Hijri calendars.
- 🌍 Works for any location in the world (latitude, longitude, elevation).
- ⚙️ Supports multiple calculation methods used globally (ISNA, MWL, UQU, etc.).
- ⚙️ Supports two Asr calculation methods (Hanafi and Standard [All Others]).
- 🌐 Uses Angle-Based Rule for high latitude adjustments (regions above 48.5° and below -48.5°).
- 📦 Does not use any external dependencies or libraries (uses pure Python).

---

## 🚀 Quick Start

### Requirements
- Python 3.9 or higher

### Installation

**To clone** the repository and install, please run the following:

```bash
git clone https://github.com/osyounis/islamic_prayer_time_app.git
cd islamic_prayer_time_app
pip install -e .
```

The `-e` flag installs all the packages that were created in this project in editable mode. This makes it easier to explore and/or modify the code.

**Alternatively:** Install directly without cloning using Git:

```bash
pip install git+https://github.com/osyounis/islamic_prayer_time_app.git
```

### Basic Usage
To use this app, all you need to do is run the `main.py` file by running either:
```bash
python3 main.py
```
or
```bash
python main.py
```

Edit the configuration section in `main.py` to use your own custom settings for calculations (like your location).

---

## 🕌 Understanding Prayer Times
Islamic prayer times are based on the position of the sun throughout the day ans should be thought of as zones. Although it is better to pray at the beginning of the prayer time zone, you can pray anytime in that zone, otherwise you will have to make up that prayer later. The Islamic prayer times are as follows:

| Prayer | Timing | Description |
| --- | --- | --- |
| Fajr | Dawn | Begins when the sky starts to lighten (Sun is at a specific angle below the horizon) |
| Sunrise | Sunrise | **Not a prayer time**. When the Sun's upper edge shows on the horizon, it marks the end of Fajr |
| Dhuhr | Midday | Begins slightly after the Sun has passed its highest point in the sky (solar noon) |
| Asr | Afternoon | Begins when an object's shadow is equal to the object's shadow at noon plus the length of the object multiplied by a factor ([see Asr calculation methods](#asr-calculation-methods)) |
| Maghrib | Sunset | Begins when the sun fully sets below the horizon|
| Isha | Night | Begins when the sky becomes completely dark (Sun is at a specific angle below the horizon)

### Calculation Methods
Different Islamic organizations use slightly different angles for Fajr and Isha. This calculator supports:

| Method Code | Organization | Fajr Angle | Isha Angle/Time | Region |
  |-------------|--------------|------------|-----------------|--------|
  | `isna` | Islamic Society of North America | 15° | 15° | North America |
  | `mwl` | Muslim World League | 18° | 17° | Europe, Americas. Middle East |
  | `egas` | Egyptian General Authority of Survey | 19.5° | 17.5° | Africa, Middle East |
  | `uqu` | Umm al-Qura University, Makkah | 18.5° | 90 min after Maghrib* | Saudi Arabia |
  | `uisk` | University of Islamic Sciences, Karachi | 18° | 18° | Pakistan, Bangladesh, India |
  | `ut` | Institute of Geophysics, University of Tehran | 17.7° | 14° | Iran, parts of Central Asia |
  | `lri` | Shia Ithna Ashari, Leva Research Institute, Qum | 16° | 14° | Shia communities worldwide |
  | `gulf` | Gulf Region, Fixed Isha Time Interval | 19.5° | 90 min after Maghrib | Gulf countries |
  | `jakim` | Jabatan Kemajuan Islam Malaysia | 20° | 18° | Malaysia, Singapore, Brunei |

  **Note:** Methods marked with * use different times during Ramadan:
  - `uqu`: 90 minutes (normal), 120 minutes (Ramadan)
  - `gulf`: 90 minutes (both normal and Ramadan)

### Asr Calculation Methods
- **Standard** (Shafi'i, Maliki, Hanbali): Shadow Length = Object Height + Noon Shadow
- **Hanafi**: Shadow Length = 2 x Object Height + Noon Shadow

---

## 🕋 Qibla Direction
The Qibla is the direction towards the Kaaba in Mecca from your location. Muslims face that direction when praying. This app uses spherical trigonometry to compute the great circle bearing from any location to the Kaaba (21.4225°N, 39.8262°E).

The bearing is given in degrees clockwise from true North (0° = North, 90° = East, 180° = South, 270° = West).

---

## ⚙️ Configuration Options
### `UserSettings` Parameters
There are three parameters you can customize when a user's settings. These are showed in the following code block.
```python
from prayer_times.config import UserSettings

settings = UserSettings(
    method='isna'           # Calculation method for Fajr and Isha
    asr_method='standard'   # 'standard' or 'hanafi'
    hijri_correction=0      # Days to adjust Hijri date (e.g. +1, -1)
)
```
### High Latitude Adjustments
In areas far from the equator (48.5° latitude North and South of the equator), the Sun may not reach the angles required fro Fajr and Isha. There are multiple methods to solve this issue. They are different algorithms to calculate Fajr and Isha at these locations. Some of these algorithms are:
- **Middle of Night:** Fajr/Isha times based on middle of the night.
- **One-Seventh:** Night divided into sevenths.
- **Angle-Based Rule:** Uses alternative angle calculations.

This app uses the **Angle-Based Rule only** when an angle is provided which is greater than 48.5° latitude North and South of the equator.

---

## 🌒 Hijri Calendar
This app is includes a Gregorian to Hijri date conversion. The Hijri calendar is lunar-based.

**Note:** Hijri dates depend on moon sighting, which varies by location. To account for this, you can use the `hijri_correction` parameter to adjust for your location (usually -2, -1, 0, 1, or 2 days).

---

## 🔭 Scientific Background
### Astronomical Calculation
The prayer time calculation involve the following:
1. **Julian Day Number**: Converting Gregorian dates to continuous count of the days since Jan 1, 4713 BC at noon.
1. **Solar Position**: Calculating the Sun's declination and equation of time.
1. **Hour Angle**: Computing when the Sun reaches specific angles.
1. **Time Conversion**: Converting from solar time to local time.

### Key Formulas
  The formulas below are based on the actual implementation in this calculator.

  #### Julian Day Number
  > Converting a Gregorian date to Julian Day Number (JD):
  >
  > $\text{JD} = 367Y - \left\lfloor\frac{7(Y + \lfloor(M + 9)/12\rfloor)}{4}\right\rfloor + \left\lfloor\frac{275M}{9}\right\rfloor + D + 1721013.5$
  >
  > where $Y$ is the year, $M$ is the month, and $D$ is the day.

  #### Mean Longitude of the Sun
  > Corrected for aberration (in degrees):
  >
  > $L = (280.466 + 0.9856474 \times n) \bmod 360$

  #### Mean Anomaly
  > The Sun's mean anomaly (in degrees):
  >
  > $g = (357.528 + 0.9856003 \times n) \bmod 360$

  #### Ecliptic Longitude
  > The Sun's ecliptic longitude (in degrees):
  >
  > $\lambda = L + 1.915 \times \sin(g) + 0.020 \times \sin(2g)$

  #### Obliquity of the Ecliptic
  > The tilt of Earth's axis (in degrees):
  >
  > $\varepsilon = 23.440 - 0.0000004 \times n$

  #### Right Ascension
  > The Sun's right ascension (in degrees):
  >
  > $\alpha = \arctan2(\cos(\varepsilon) \times \sin(\lambda), \cos(\lambda))$

  #### Sun's Declination
  > The Sun's declination $\delta$ (angle relative to celestial equator):
  >
  > $\delta = \arcsin(\sin(\varepsilon) \times \sin(\lambda))$
  > 
  > This is the fundamental value used to calculate all prayer times.

  #### Equation of Time
  > The difference between apparent solar time and mean solar time (in minutes):
  >
  > $\text{EoT} = (L - \alpha) \times 4$
  >
  >where the factor of 4 converts degrees to minutes (since Earth rotates 360° in 24 hours = 1440 minutes).

  #### Hour Angle
  > For a given sun altitude angle $\alpha_{\text{sun}}$ below or above the horizon, the hour angle $H$ is:
  >
  > $H = \arccos\left(\frac{\sin(\alpha_{\text{sun}}) - \sin(\phi) \times \sin(\delta)}{\cos(\phi) \times \cos(\delta)}\right)$
  >
  > where:
  > - $\phi$ = observer's latitude
  > - $\delta$ = sun's declination
  > - $\alpha_{\text{sun}}$ = desired sun altitude angle (negative for below horizon)

  #### Prayer Time Calculation
  > The local time of prayer is calculated as:
  >
  > $T = 12 + \frac{H}{15} - \frac{\text{Lng}}{15} + \frac{\text{EoT}}{60} + \text{TZ}$
  > 
  > where:
  > - $H$ = hour angle in degrees
  > - $\text{Lng}$ = longitude in degrees (negative for West)
  > - $\text{EoT}$ = equation of time in minutes
  > - $\text{TZ}$ = time zone offset from UTC in hours
  > - Division by 15 converts degrees to hours (360° = 24 hours)

  #### Qibla Direction
  > The Qibla bearing $q$ from observer location $(\phi_1, L_1)$ to the Kaaba $(\phi_2, L_2)$:
  >
  >$q = \arctan2\left(\sin(\Delta L), \cos(\phi_1) \times \tan(\phi_2) - \sin(\phi_1) \times \cos(\Delta L)\right)$
  >
  > where:
  > - $\Delta L = L_2 - L_1$ (difference in longitude)
  > - $(\phi_2, L_2) = (21.4225°, 39.8262°)$ (Kaaba coordinates)
  >
  > The result is converted from radians to degrees and normalized to 0-360°.

### Further Reading
For detailed mathematical derivations and implementation details, see [`docs/calculation_methodology.md`](https://github.com/osyounis/islamic_prayer_time_app/blob/main/docs/calculation_methodology.md).

---

## 📁 Project Structure
```
islamic_prayer_time_app/
  ├── main.py                          # Simple example script
  ├── prayer_times/                    # Main package
  │   ├── config.py                    # Configuration and constants
  │   ├── calculator/
  │   │   ├── calculator.py            # Main calculation orchestrator
  │   │   └── times.py                 # Prayer time calculations
  │   ├── core/
  │   │   ├── astronomy.py             # Astronomical calculations
  │   │   ├── calendar.py              # Hijri calendar conversion
  │   │   └── qibla.py                 # Qibla direction calculation
  │   └── utils/
  │       ├── math_utils.py            # Mathematical utilities
  │       └── time_utils.py            # Time manipulation utilities
  ├── tests/                           # Unit tests
  │   ├── test_astronomy.py
  │   ├── test_calendar.py
  │   ├── test_qibla.py
  │   ├── test_times.py
  │   ├── test_calculator.py
  │   └── test_math.py
  ├── docs/                            # Documentation
  │   ├── api_reference.md
  │   ├── calculation_methodology.md
  │   ├── hijri_calendar.md
  │   └── qibla_calculation.md
  ├── examples/                        # Usage examples
  │   ├── basic_usage.py
  │   ├── multiple_locations.py
  │   ├── different_methods.py
  │   ├── monthly_calendar.py
  │   ├── qibla_only.py
  │   └── hijri_date_conversion.py
  └── pyproject.toml                   # Package metadata
```

---

## 🧪 Testing
You can run the tests in this project using these methods:

```bash
# Run all tests at once
python3 -m unittest discover tests

# Run tests with verbose output
python3 -m unittest discover tests -v

# Run a specific test file (e.g. test_math.py)
python3 tests/test_math.py
```

All tests are automatically run via GitHub Actions on every push and pull request.

### Current Test Coverage

- ✅ **Math utilities** - Trigonometric functions and conversions (29 tests)
- ✅ **Astronomy calculations** - Sun coordinates, equation of time, seasonal variations (6 tests)
- ✅ **Calendar conversions** - Julian Day, Hijri calendar (16 tests)
- ✅ **Qibla direction** - Major cities worldwide, edge cases (19 tests)
- ✅ **Prayer time calculations** - All 5 prayers + sunrise, multiple methods (23 tests)
- ✅ **Main calculator** - Full integration tests (12 tests)

**Total: 105 tests ✅**

---

## 🤝 Contributing
Contributions are welcome! This project is designed to run correctly but also to be educational for others.
### Ways to Contribute
If you would like to contribute to this project, below is a list of way you can contribute:
- 🐞 Report bugs or calculation errors/inaccuracies
- 📄 Improve documentation or add more examples
- 🧪 Add more test cases
- ✨ Suggest new features to add
- 🌍 Verify the calculations for your location

### Before Contributing
1. Ensure your code follows [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html)
1. Add tests for new features/functionality
1. Update documentation as needed
1. Verify all tests pass

---

## 📚 Resources & References
This implementation is based on astronomical algorithms and prayer time calculation methods from various
  Islamic and scientific sources.

  ### Primary References

  **Prayer Time Calculation Methodologies:**
  - **PrayTimes.org** - Comprehensive resource for Islamic prayer time calculations
    https://praytimes.org/

  - **Islamic Prayer Times Calculation** (Astronomy Center) - Detailed article on prayer time algorithms
    https://astronomycenter.net/article/2001_salat.html

  - **Calculating Prayer Times** by Radhifadlillah - Educational blog post with focus on Asr calculation  
    https://radhifadlillah.com/blog/2020-09-06-calculating-prayer-times/#factor-of-shadow-length-at-asr

  **Hijri Calendar Conversion:**
  - **Date Conversion Algorithms** (PDF) - Mathematical approach to Gregorian/Hijri conversion  
    https://astronomycenter.net/pdf/2001_conv.pdf

  **Geographic & Astronomical Calculations:**
  - **Calculate Distance, Bearing and More Between Latitude/Longitude Points** by Chris Veness
    https://www.movable-type.co.uk/scripts/latlong.html
    (Used for Qibla direction calculation using spherical trigonometry)

  **Open Source Implementations:**
  - **pyIslam** - Python library for Islamic prayer times and Qibla calculations
    https://github.com/abougouffa/pyIslam

  - **Islamic Network Prayer Times Library**
    https://1x.ax/islamic-network/libraries/prayer-times/~files

  ### Additional References

  **Books:**
  - **Astronomical Algorithms** (2nd Edition) by Jean Meeus - Standard reference for astronomical calculations

  **Organizations & Standards:**
  - **Islamic Society of North America (ISNA)** - North American calculation standards
  - **Muslim World League (MWL)** - International calculation standards
  - **Umm Al-Qura University** - Saudi Arabian calculation standards
  - **Egyptian General Authority of Survey** - Egyptian calculation standards
  - **University of Islamic Sciences, Karachi** - South Asian calculation standards
  - **Institute of Geophysics, University of Tehran** - Iranian calculation standards
  - **Jabatan Kemajuan Islam Malaysia (JAKIM)** - Malaysian calculation standards

  ### Notes on Implementation

  This project combines approaches from multiple sources to create a pure Python implementation with:
  - No external dependencies
  - Clear, educational code structure
  - Support for multiple calculation methods
  - Accurate astronomical calculations

  **Accuracy Verification:**
  Prayer times calculated by this library have been cross-referenced with:
  - Published timetables from local Islamic centers
  - Results from PrayTimes.org
  - Output from other established prayer time calculators

---

## 🪪 License
This project is licensed under **GNU General Public License v3.0 or later (GPL-3.0-or-later).**

See [LICENSE](https://github.com/osyounis/islamic_prayer_time_app/blob/main/LICENSE) for full text.

---

## ✍️ Author
**Omar Younis**

---

## ⚠️ Important Notes
1. **Accuracy**: While this calculator uses established astronomical algorithms, prayer times may vary slightly from local mosque announcements due to different conventions, adjustments, or local sighting committees.
1. **Hijri Dates**: Hijri calendar dates are calculated astronomically and may differ from official announcements based on moon sighting. Always verify with your local Islamic authority.
1. **High Latitudes**: In extreme latitudes (near polar regions), normal calculation methods may not work during certain times of year. The calculator includes adjustments using the Angle-Based Rule, but consult local scholars for guidance.
1. **Qibla**: Calculated Qibla direction is based on great circle calculations. Physical obstacles or magnetic declination may affect compass readings when aligning yourself for prayer.

---