<h3 align="center">
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ
</h3><br>

# Hijri Calendar Conversion

## Table of Contents
1. [What is the Hijri Calendar?](#what-is-the-hijri-calendar)
1. [Calendar Comparison](#calendar-comparison)
1. [The Islamic Calendar System](#the-islamic-calendar-system)
1. [Conversion Method](#conversion-method)
1. [Step-by-Step Algorithm](#step-by-step-algorithm)
1. [Important Considerations](#important-considerations)
1. [Practical Usage](#practical-usage)

---

## What is the Hijri Calendar?
The **Hijri calendar**, also known as the **Islamic calendar**, is a lunar calendar used to date events in many Muslim countries and to determine Islamic holy days and festivals.

### Historical Background
**Name Origin:**
- "Hijri" comes from "Hijrah", the migration of Prophet Muhammad ﷺ from Mecca to Medina
- This event marks the beginning of the Islamic calendar: Year 1 AH

**Epoch Date:**
- The Hijri calendar epoch is **July 16, 622 AD** (Gregorian)
- Julian Day Number: **1948440**
- This is day 1 of Muharram, year 1 AH

### Religious Significance
The Hijri calendar is used to determine:
- **Ramadan** - The month of fasting (9th month)
- **Eid al-Fitr** - Festival after Ramadan (1st of Shawwal)
- **Hajj** - Pilgrimage period (8-12th of Dhu al-Hijjah)
- **Eid al-Adha** - Festival of Sacrifice (10th of Dhu al-Hijjah)
- Other important Islamic dates

---

## Calendar Comparison

### Hijri vs. Gregorian

| Feature | Hijri Calendar | Gregorian Calendar |
|---------|----------------|-------------------|
| **Type** | Lunar (based on Moon) | Solar (based on Sun) |
| **Year Length** | ~354.37 days | ~365.25 days |
| **Months** | 12 months | 12 months |
| **Month Length** | 29 or 30 days (alternating) | 28-31 days (variable) |
| **Leap Year Cycle** | 11 leap years per 30 years | 97 leap years per 400 years |
| **Leap Day** | Extra day in Dhu al-Hijjah | Extra day in February |
| **Seasons** | Drift through seasons | Fixed to seasons |
| **Start Date** | July 16, 622 AD | January 1, 1 AD |

### Key Differences

**1. Lunar vs. Solar**
- **Hijri:** Based on the phases of the Moon (29.5-day lunar cycle)
- **Gregorian:** Based on Earth's orbit around the Sun (365.25-day solar year)

**2. Year Length**
- A Hijri year is approximately **11 days shorter** than a Gregorian year
- Every 33 years, the Hijri calendar gains about one year relative to the Gregorian

**3. Seasonal Drift**
- Because the Hijri year is lunar, Islamic months drift through the seasons
- Ramadan occurs in different seasons over a 33-year cycle
- The Gregorian calendar stays aligned with seasons

---

## The Islamic Calendar System

### The 12 Hijri Months

| # | English | Arabic | Days |
|---|---------|--------|------|
| 1 | Muharram | مُحَرَّم | 30 |
| 2 | Safar | صَفَر | 29 |
| 3 | Rabi' al-Awwal | رَبِيع الأَوَّل | 30 |
| 4 | Rabi' al-Thani | رَبِيع الثَّانِي | 29 |
| 5 | Jumada al-Awwal | جُمَادَىٰ الأُولَىٰ | 30 |
| 6 | Jumada al-Thani | جمادى الثانية | 29 |
| 7 | Rajab | رَجَب | 30 |
| 8 | Sha'ban | شَعْبَان | 29 |
| 9 | Ramadan | رَمَضَان | 30 |
| 10 | Shawwal | شَوَّال | 29 |
| 11 | Dhu al-Qadah | ذُو القَعْدَة | 30 |
| 12 | Dhu al-Hijjah | ذُو الحِجَّة | 29 or 30* |

**In a leap year, Dhu al-Hijjah has 30 days instead of 29.*

### The 30-Year Cycle

The Hijri calendar uses a **30-year cycle** to determine leap years:

**Structure:**
- Each 30-year cycle contains:
- **19 common years** of 354 days
- **11 leap years** of 355 days
- Total: **10,631 days** per 30-year cycle

**Leap Years:**

The 11 leap years in each 30-year cycle occur in years: 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, and 29.

**Formula to check if a Hijri year is a leap year:**

$\text{Leap Year} = ((11 \times \text{Year} + 14) \bmod 30) < 11$

---

## Conversion Method

### Overview
Converting from Gregorian to Hijri requires three steps:
1. Gregorian → Julian Day Number (continuous day count)
1. Julian Day Number → Days since Hijri Epoch
1. Days since Epoch → Hijri Date (using the 30-year cycle)

### Why Do We Use Julian Day Number?
The Julian Day Number (JD) serves as a universal intermediary:
- Continuous count of days since January 1, 4713 BC
- Simplifies date arithmetic
- Eliminates calendar-specific complexity

---

## Step-by-Step Algorithm
This implementation uses the algorithm based on the 30-year cycle structure.

### Input: Julian Day Number
Assume we have already converted the Gregorian date to Julian Day Number (JD).

For the conversion process, we also add a correction factor `d_correction` (user-specified adjustment in days).

### Step 1: Days Since Hijri Epoch

$l = \lfloor \text{JD} + d_{\text{correction}} \rfloor - 1948440 + 10632$

Where:
- `1948440` = Julian Day of Hijri epoch (Muharram 1, 1 AH)
- `10632` = Adjustment to align with algorithm's internal reference point

### Step 2: Calculate Complete 30-Year Cycles

$n = \left\lfloor\frac{l - 1}{10631}\right\rfloor$

Where:
- $n$ = number of complete 30-year cycles
- `10631` = total days in one 30-year cycle

### Step 3: Remaining Days Within Current Cycle

$l = l - (10631 \times n) + 354$

This updates $l$ to represent the remaining days within the current 30-year cycle, with a 354-day offset for calculation convenience.

### Step 4: Determine Year Within Cycle

$j = \left\lfloor\frac{10985 - l}{5316}\right\rfloor \times \left\lfloor\frac{50 \times l}{17719}\right\rfloor + \left\lfloor\frac{l}{5670}\right\rfloor \times \left\lfloor\frac{43 \times l}{15238}\right\rfloor$

Where:
- $j$ = which year (0-29) within the current 30-year cycle
- This complex formula accounts for the irregular distribution of leap years

### Step 5: Refine to Day of Year

$l = l - \left\lfloor\frac{30 - j}{15}\right\rfloor \times \left\lfloor\frac{17719 \times j}{50}\right\rfloor - \left\lfloor\frac{j}{16}\right\rfloor \times \left\lfloor\frac{15238 \times j}{43}\right\rfloor + 29$

After this step, $l$ represents an intermediate value used to extract the month and day.

### Step 6: Extract Month

$\text{month} = \left\lfloor\frac{24 \times l}{709}\right\rfloor$

Where:
- The ratio `709/24 ≈ 29.54` approximates the average Hijri month length

### Step 7: Extract Day

$\text{day} = l - \left\lfloor\frac{709 \times \text{month}}{24}\right\rfloor$

This removes the month contribution to find the day within the month.

### Step 8: Calculate Hijri Year

$\text{year} = 30 \times n + j - 30$

Where:
- $n$ = number of complete 30-year cycles
- $j$ = year within the current cycle
- Subtract 30 to align with proper year numbering

### Result

The algorithm returns:
- Day: 1-30 (day of the month)
- Month: 1-12 (Hijri month number)
- Year: Hijri year (AH)

---

## Important Considerations

### 1. Astronomical vs. Observational

**Two Types of Hijri Calendar:**

**Astronomical Calendar**:
- Uses mathematical calculations (like this implementation)
- Predictable and consistent
- Based on the 30-year cycle

**Observational Calendar**:
- Based on actual moon sighting
- Begins when the crescent moon is physically observed
- Used officially in many Muslim countries
- Can vary by 1-2 days from astronomical calculations

**This calculator uses the astronomical method.**

### 2. Moon Sighting vs. Calculation

#### Why Differences Exist:
Islamic tradition emphasizes **physical observation** of the new crescent moon to mark the beginning of months.
Factors affecting sighting:
- Weather conditions (clouds, visibility)
- Geographic location
- Observer's eyesight and experience
- Atmospheric conditions
- Timing of moonset relative to sunset

**Result**: The officially declared Hijri date in a country may differ from the calculated date by ±2 days.

###  3. Correction Factor
The `d_correction` parameter allows users to adjust the calculated date:
```python
hijri = hijri_date(jd, d_correction=1)  # Add 1 day
hijri = hijri_date(jd, d_correction=-1)  # Subtract 1 day
```
**When to Use**:
- Match your local Islamic authority's announced dates
- Align with your community's practice
- Account for regional differences in moon sighting

**Common Values:**
- `-1` or `-2`: If calculations are ahead of local announcements
- `0`: No adjustment (pure astronomical calculation)
- `+1` or `+2`: If calculations are behind local announcements

### 4. Ramadan and Official Announcements
For **Ramadan** and **Eid**, always verify with:
- Official religious authorities in your country
- Regional moon sighting committees

The calculated date provides an estimate, but official announcements should take precedence for religious observances.

---
## Practical Usage

### How to Use This Library
```python
from datetime import datetime
from prayer_times.core.calendar import julian_date, hijri_date
from prayer_times.config import get_hijri_month_name

# Today's date
today = datetime.now()

# Convert to Julian Day
jd = julian_date(today)

# Convert to Hijri (no correction)
hijri = hijri_date(jd, d_correction=0)

# Get month name
month_en = get_hijri_month_name(hijri['month'], 'en')
month_ar = get_hijri_month_name(hijri['month'], 'ar')

# Display
print(f"Gregorian: {today.strftime('%B %d, %Y')}")
print(f"Hijri: {month_en} {hijri['day']}, {hijri['year']} AH")
print(f"Arabic: {month_ar} {hijri['day']}, {hijri['year']}")
```

### With Correction Factor
```python
# If your local mosque announced the date is 1 day ahead
hijri_adjusted = hijri_date(jd, d_correction=1)

month_name = get_hijri_month_name(hijri_adjusted['month'], 'en')
print(f"Adjusted: {month_name} {hijri_adjusted['day']}, {hijri_adjusted['year']} AH")
```

### Checking for Ramadan
```python
from prayer_times.config import is_ramadan

# Check if current Hijri month is Ramadan
if is_ramadan(hijri['month']):
    print("It is Ramadan!")
    print("Fasting and increased worship are encouraged.")
else:
    print(f"Current month: {get_hijri_month_name(hijri['month'], 'en')}")
```
---