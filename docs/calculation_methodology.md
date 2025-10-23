<h3 align="center">
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ
</h3><br>

# Islamic Prayer Time Calculation Methodology

## Table of Contents
  1. [Introduction](#introduction)
  2. [Astronomical Foundation](#astronomical-foundation)
  3. [Prayer Times Overview](#prayer-times-overview)
  4. [Detailed Calculations](#detailed-calculations)
     - [Julian Day Number](#julian-day-number)
     - [Sun Position](#sun-position)
     - [Equation of Time](#equation-of-time)
     - [Hour Angle](#hour-angle)
  5. [Individual Prayer Times](#individual-prayer-times)
     - [Fajr](#fajr-dawn-prayer)
     - [Sunrise](#sunrise)
     - [Dhuhr](#dhuhr-noon-prayer)
     - [Asr](#asr-afternoon-prayer)
     - [Maghrib](#maghrib-sunset-prayer)
     - [Isha](#isha-night-prayer)
  6. [High Latitude Adjustments](#high-latitude-adjustments)
  7. [Calculation Methods Explained](#calculation-methods-explained)
  8. [Accuracy and Precision](#accuracy-and-precision)




## Introduction
Islamic prayer times are fundamentally tied to the position of the Sun in the sky. Unlike clock-based schedules, prayer times vary daily and by location because they depend on solar events (dawn, noon, sunset, etc.).

This document tries to explain the astronomical and mathematical foundations used to calculate these times accurately.

---

## Astronomical Foundation

### The Earth-Sun System
Prayer time calculations are based on three key concepts:

1. **Earth's Rotation** - The Earth rotates 360° in approximately 24 hours (one solar day)
1. **Earth's Orbit** - The Earth orbits the Sun, causing seasonal variations in day length
1. **Solar Angles** - Prayer times correspond to specific angles of the Sun below or above the horizon

### Coordinate Systems
We use two primary coordinate systems:
**Geographic Coordinates:**
- **Latitude ($\phi$)**: Position north/south of the equator (-90° to +90°)
- **Longitude ($L$)**: Position east/west of the Prime Meridian (-180° to +180°)
- **Elevation**: Height above sea level in meters (affects sunrise/sunset slightly)

**Celestial Coordinates:**
- **Right Ascension ($\alpha$)**: Celestial equivalent of longitude
- **Declination ($\delta$)**: Celestial equivalent of latitude
- **Hour Angle (H)**: Measures time since solar noon

---

## Prayer Times Overview
| Prayer | Arabic | Solar Event | Sun Position |
|--------|--------|-------------|--------------|
| Fajr | الفجر | Dawn begins | Specific angle below eastern horizon |
| Sunrise | الشروق | Sun appears | Top edge crosses horizon |
| Dhuhr | الظهر | Solar noon | Highest point + small offset |
| Asr | العصر | Afternoon | Shadow-based calculation |
| Maghrib | المغرب | Sunset | Sun completely sets |
| Isha | العشاء | Night begins | Specific angle below western horizon |

---

## Detailed Calculations

### Julian Day Number

The Julian Day (JD) is a continuous count of days since January 1, 4713 BC at noon. It simplifies astronomical calculations by providing a single number for any date.

#### Month and Year Adjustment

For the Julian Date calculation, if the month is January or February, we adjust:

$\text{If } M \in \{1, 2\}: \quad M' = M + 12, \quad Y' = Y - 1$

$\text{Otherwise}: \quad M' = M, \quad Y' = Y$

This adjustment treats January and February as months 13 and 14 of the previous year, which simplifies the calculation.

#### Gregorian Calendar Correction (B-Value)

On October 15, 1582, the world transitioned from the Julian to the Gregorian calendar. The B-value accounts for this:

For dates before October 15, 1582:

$B = 0$

For dates on or after October 15, 1582:

$A = \left\lfloor\frac{Y'}{100}\right\rfloor$

$B = 2 - A + \left\lfloor\frac{A}{4}\right\rfloor$

where $A$ represents the century number.

#### Julian Date Formula

$\text{JD} = \left\lfloor 365.25 \times (Y' + 4716)\right\rfloor + \left\lfloor 30.6001 \times (M' + 1)\right\rfloor + D + B - 1524.5$

Where:
- $Y'$ = Adjusted year
- $M'$ = Adjusted month
- $D$ = Day of month (1-31)
- $B$ = Gregorian calendar correction
- $\lfloor x \rfloor$ = Floor function (integer part of $x$)

Example:
For January 1, 2000:
- Original: $Y = 2000$, $M = 1$, $D = 1$
- After adjustment: $Y' = 1999$, $M' = 13$
- $A = \lfloor 1999/100 \rfloor = 19$
- $B = 2 - 19 + \lfloor 19/4 \rfloor = 2 - 19 + 4 = -13$
- $\text{JD} = \lfloor 365.25 \times 5715 \rfloor + \lfloor 30.6001 \times 14 \rfloor + 1 + (-13) - 1524.5$
- $\text{JD} = 2087685 + 428 + 1 - 13 - 1524.5$
- $\text{JD} = 2451544.5$

#### Days Since J2000.0:
For convenience, we measure days from the J2000.0 epoch (January 1, 2000, 12:00 TT):

$n = \text{JD} - 2451545.0$

**Note**: J2000.0 is defined as JD 2451545.0, which is noon on January 1, 2000.

---

### Sun Position
The Sun's position in the sky is described by several parameters that change throughout the year.

#### Mean Longitude ($L$)
The Sun's mean longitude, corrected for aberration:

$L = (280.466 + 0.9856474 \times n) \bmod 360$

**Note**: $L$ increases approximately 0.9856° per day (≈360° per year)

#### Mean Anomaly ($g$)
The Sun's mean anomaly (related to Earth's elliptical orbit):

$g = (357.528 + 0.9856003 \times n) \bmod 360$

#### Ecliptic Longitude ($\lambda$)
The Sun's true position along the ecliptic:

$\lambda = L + 1.915 \times \sin(g) + 0.020 \times \sin(2g)$

The correction terms account for Earth's elliptical orbit.

#### Obliquity of the Ecliptic ($\epsilon$)
The tilt of Earth's axis (currently about 23.44°, slowly decreasing):

$\varepsilon = 23.440 - 0.0000004 \times n$

#### Right Ascension ($\alpha$)
Converts ecliptic longitude to equatorial coordinates:

$\alpha = \arctan2(\cos(\varepsilon) \times \sin(\lambda), \cos(\lambda))$

#### Declination ($\delta$)
**This is the most important parameter for prayer time calculations.**

The Sun's declination is its angle north or south of the celestial equator:

$\delta = \arcsin(\sin(\varepsilon) \times \sin(\lambda))$

Key Properties:
- Ranges from approximately -23.44° (winter solstice) to +23.44° (summer solstice)
- Equals 0° at the equinoxes (about March 20, September 22)
- Determines how high the Sun rises at a given latitude
- Directly affects prayer times

---
  
### Equation of Time
The Equation of Time (EoT) accounts for the difference between "solar time" (actual Sun position) and "mean solar time" (clock time).

**Formula**:

$\text{EoT} = (L - \alpha) \times 4$

- Result is in minutes
- Factor of 4 converts degrees to minutes (360° ÷ 24 hours = 15°/hour = 4 minutes/degree)

**Why is this needed?**

Two factors cause solar time to differ from clock time:
1. Earth's elliptical orbit - Earth moves faster when closer to the Sun
1. Earth's axial tilt - The Sun appears to move unevenly across the sky

---

### Hour Angle
The hour angle ($H$) represents the time since solar noon, measured in degrees.

**For a given Sun altitude angle $\alpha$:**

$H = \arccos\left(\frac{\sin(\alpha) - \sin(\phi) \times \sin(\delta)}{\cos(\phi) \times \cos(\delta)}\right)$

Where:
- $\phi$ = observer's latitude
- $\delta$ = Sun's declination
- $\alpha$ = desired Sun altitude (negative for below horizon)

**Converting Hour Angle to Time:**

$T = 12 + \frac{H}{15} - \frac{L}{15} + \frac{\text{EoT}}{60} + \text{TZ}$

Where:
- $H$ = hour angle (degrees)
- $L$ = longitude (negative for West)
- $\text{EoT}$ = equation of time (minutes)
- $\text{TZ}$ = time zone offset (hours)

**Sign Convention:**
- Morning prayers (Fajr, Sunrise): Use $-H$ (before noon)
- Afternoon prayers (Asr): Use $+H$ (after noon)

---

## Individual Prayer Times

### Fajr (Dawn Prayer)

**INFO**: Fajr begins when the first light appears on the eastern horizon (astronomical dawn).

**Sun Angle**: Method-dependent (typically 15° to 20° below horizon)

**Formula**:

$\alpha_{\text{Fajr}} = -\text{FajrAngle}$

**Different Methods Examples**:

| Organization     | Fajr Angle |
|------------------|------------|
| ISNA             | 15°        |
| MWL              | 18°        |
| Egypt            | 19.5°      |
| Malaysia (JAKIM) | 20°        |

**Why the differences?**

The exact angle depends on:
- Local atmospheric conditions
- Traditional scholarly interpretations
- Geographic/climate considerations

**Calculation**:
1. Calculate Sun's declination $\delta$ for the date
1. Use hour angle formula with $\alpha = -\text{FajrAngle}$
1. Convert to local time

---

### Sunrise

**INFO**: Sunrise is when the Sun's upper edge first appears above the horizon.

**Sun Angle**: -0.833°

This accounts for:
- **Atmospheric refraction (≈0.583°)**: Light bends as it passes through the atmosphere, making the Sun appear higher
- **Sun's semi-diameter (≈0.25°)**: We see the top edge, not the center

**Formula**:

$\alpha_{\text{Sunrise}} = -0.833°$

**Note**: Sunrise marks the end of Fajr prayer time, not a prayer itself.

---

### Dhuhr (Noon Prayer)

**INFO****: Dhuhr begins slightly after the Sun passes its highest point (solar noon).

**Formula**:

Solar noon occurs when the Sun's hour angle is 0°:

$T_{\text{Noon}} = 12 - \frac{L}{15} + \frac{\text{EoT}}{60} + \text{TZ}$

**Offset for Dhuhr**:

Most scholars add a small offset (typically 1-2 minutes) after solar noon to ensure the Sun has clearly passed its zenith.

$T_{\text{Dhuhr}} = T_{\text{Noon}} + \text{offset}$

**Why the offset**?

Islamic jurisprudence considers the exact moment of solar noon (zawāl) as a prohibited time for prayer. The offset ensures this moment has passed.

---

### Asr (Afternoon Prayer)

**INFO**: Asr begins when the shadow of an object equals a specific ratio of its height (beyond the shadow at solar noon).

**Two Methods**:
1. **Standard (Shafi'i, Maliki, Hanbali)**:
   - Shadow length = object height + noon shadow
   - Shadow ratio: $s = 1$
1. **Hanafi**:
   - Shadow length = 2 × object height + noon shadow
   - Shadow ratio: $s = 2$

**Sun Angle Formula**:

$\alpha_{\text{Asr}} = \arctan\left(\frac{1}{s + \tan(|\phi - \delta|)}\right)$

Where:
- $s$ = shadow ratio (1 or 2)
- $\phi$ = latitude
- $\delta$ = Sun's declination

**Geometric Explanation**:

At solar noon, an object casts a minimum shadow due to the Sun being at its highest point. As the afternoon progresses, the shadow lengthens. Asr time is defined by when this shadow reaches a specific length relative to the object's height.

**Why two methods?**

Different schools of Islamic jurisprudence interpret the hadith descriptions of Asr time slightly differently, leading to two accepted calculations.

---

### Maghrib (Sunset Prayer)

**INFO**: Maghrib begins immediately when the Sun fully sets below the horizon.

**Sun Angle**: -0.833° (same as sunrise)

**Formula**:

$\alpha_{\text{Maghrib}} = -0.833°$

**Calculation**:

Use the hour angle formula with the sunset angle, solving for the afternoon hour angle:

$T_{\text{Maghrib}} = 12 + \frac{H}{15} - \frac{L}{15} + \frac{\text{EoT}}{60} + \text{TZ}$

**Note**: Maghrib has the shortest prayer window (until Isha begins), so it should be prayed promptly.

---

### Isha (Night Prayer)

**INFO**: Isha begins when the sky is completely dark (astronomical twilight ends).

**Two Calculation Types:**

#### 1. Angle-Based (Most Common)
Sun is a specific angle below the western horizon:

$\alpha_{\text{Isha}} = -\text{IshaAngle}$

**Different Methods Examples**:

| Organization | Isha Angle |
|--------------|------------|
| ISNA         | 15°        |
| MWL          | 17°        |
| Egypt        | 17.5°      |
| Karachi      | 18°        |


#### 2. Fixed-Time Interval (Used in some regions)
With this method, Isha is a fixed time after Maghrib:

$T_{\text{Isha}} = T_{\text{Maghrib}} + \text{interval}$

**Examples**:
- **Umm Al-Qura (Makkah)**: 90 minutes (normal), 120 minutes (Ramadan)
- **Gulf Region**: 90 minutes (both normal and Ramadan)

---

## High Latitude Adjustments

### The Problem
At latitudes approximately 48.5° away from the equator and greater, during certain times of year:
- The Sun may never reach the Fajr angle (white nights)
- The Sun may never reach the Isha angle
- Normal calculations fail

### Solutions
Three adjustment methods exist:
#### 1. Middle of the Night
Fajr and Isha are calculated as fractions of the night:

$T_{\text{Fajr}} = T_{\text{Sunset}} - \frac{1}{2}(\text{Night Duration})$

$T_{\text{Isha}} = T_{\text{Sunset}} + \frac{1}{2}(\text{Night Duration})$

Where Night Duration = time from sunset to sunrise the next day.

#### 2. One-Seventh Rule
The night is divided into sevenths:

$T_{\text{Fajr}} = T_{\text{Sunrise}} - \frac{1}{7}(\text{Night Duration})$

$T_{\text{Isha}} = T_{\text{Sunset}} + \frac{1}{7}(\text{Night Duration})$

#### 3. Angle-Based Rule (Selected approach for this app)
Use reduced angles or the nearest latitude where normal calculations work.

$\text{Night Duration} = (T_{\text{sunrise}} + 24\text{ hours}) - T_{\text{Maghrib}}$

$T_{\text{Fajr}} = T_{\text{sunrise}} - \left(\text{Night Duration} \times \frac{\text{FajrAngle}}{60}\right)$

$T_{\text{Isha}} = T_{\text{Maghrib}} + \left(\text{Night Duration} \times \frac{\text{IshaAngle}}{60}\right)$

**Note**: Muslims living at extreme latitudes should consult local Islamic scholars for guidance on which method to follow.

---

## Calculation Methods Explained

### Why Multiple Methods?
Different Islamic organizations have established calculation standards based on:

1. **Local Observation**: Historical observations in their region
1. **Scholarly Interpretation**: Different readings of hadith texts
1. **Practical Considerations**: Climate, visibility, community needs
1. **Astronomical Research**: Modern scientific measurements

### Choosing a Method
**Guidelines**:
- Use the method of your local mosque if you're part of a community
- Use the method for your region (e.g., ISNA for North America, JAKIM for Malaysia)
- When traveling, use the local method of your destination
- For personal use, choose the method that aligns with your understanding or preference

---

## Accuracy and Precision

### Expected Accuracy

This implementation provides prayer times accurate to within ±2 minutes for most locations.

**Factors Affecting Accuracy**:

1. **Atmospheric Conditions**
   - Humidity, temperature, pressure affect refraction
   - Can cause variations in time.
1. **Elevation**
   - Higher elevations see sunrise earlier and sunset later
   - The calculator accounts for elevation in sunrise/sunset
1. **Local Horizon**
   - Mountains, buildings may obscure the actual horizon
   - Calculations assume a flat, unobstructed horizon
1. **Calculation Method Choice**
   - Different methods inherently give different times
   - This is intentional, not an error

### Validation
Prayer times have been validated against:
- Published mosque timetables
- Established prayer time websites (e.g., PrayTimes.org)
- Other calculation libraries
- Astronomical software

### Limitations
This app can't account for:
- Local horizon obstructions (mountains, tall buildings)
- Unusual atmospheric conditions
- Local mosque adjustments or traditions
- Sighting committee decisions (moon sightings)

**Always defer to local Islamic authorities when in doubt.**

---

## Conclusion
This implementation tries to be both accurate and educational, helping Muslims determine when they should pray and how these times are calculated.

---