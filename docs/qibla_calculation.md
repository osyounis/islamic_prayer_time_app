<h3 align="center">
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ
</h3><br>

# Qibla Direction Calculation

## Table of Contents
1.  [What is the Qibla?](#what-is-the-qibla)
1.  [Geographic Coordinates](#geographic-coordinates)
1.  [Spherical Trigonometry Basics](#spherical-trigonometry-basics)
1.  [Great Circle Bearing](#great-circle-bearing)
1.  [Step-by-Step Calculation](#step-by-step-calculation)
1.  [Special Cases](#special-cases)
1.  [Implementation](#implementation)

---

## What is the Qibla?
The **Qibla** (قِبْلَة) is the direction that Muslims face when praying the five daily prayers. It points towards the **Kaaba** (الكعبة), in Mecca, Saudi Arabia.

**Kaaba Coordinates:**
- **Latitude:** 21.4225° North
- **Longitude:** 39.8262° East

---

## Geographic Coordinates

### Latitude and Longitude

**Latitude ($\phi$):**
- Measures the position North or South of the equator
- Range: -90° (South Pole) to +90° (North Pole)
- Equator is 0°
- **Sign Convention:** North is positive and South is negative

**Longitude ($\lambda$):**
- Measures the position East or West of the Prime Meridian
- Range: -180° to +180°
- Prime Meridian is 0°
- **Sign Convention:** East is positive and West is negative

### Earth as a Sphere
For Qibla calculations, we treat the Earth as a perfect sphere. Even though Earth isn't a perfect sphere and is slightly flatten at the poles due to the Earth's rotation (oblate spheroid), assuming the Earth is a perfect sphere give an accurate enough direction to pray todays.

#### Why?
The difference between the spherical and ellipsoidal calculations for a bearing is normally less than 0.1°, which is good enough for our purposes.

---

## Spherical Trigonometry Basics
Unlike flat-surface (planar) trigonometry, **spherical trigonometry** deals with triangles on the surface of a sphere.

### Great Circles
A **great circle** is the largest possible circle that can be drawn on a sphere. It divides the sphere into two equal hemispheres.

**Properties:**
- The shortest path between two points on a sphere follows a great circle
- All lines of longitude are great circles
- The equator is a great circle
- Lines of latitude (except the equator) are **not** great circles

**For Qibla:** The direction we seek is along the great circle that connects the observer's location to the Kaaba.

### Why Not a Straight Line on a Map?
On a flat map, the Qibla direction appears curved. This is because map projections distort the spherical Earth onto a flat surface. The true shortest path on the globe is a great circle arc.

---

## Great Circle Bearing
The **bearing** (or azimuth) is the angle measured clockwise from true North to the direction of travel.

**Bearing Convention:**
- **0° (or 360°):** North
- **90°:** East
- **180°:** South
- **270°:** West

### Formula
To find the bearing from point 1 (observer) to point 2 (Kaaba), we use the **great circle bearing formula:**

#### Step 1: Calculate the difference in longitude

$\Delta L = L_2 - L_1$

Where:
- $L_1$ = observer's longitude
- $L_2$ = Kaaba's longitude (39.8262°)

#### Step 2: Calculate intermediate values

$y = \sin(\Delta L) \times \cos(\phi_2)$

$x = \cos(\phi_1) \times \sin(\phi_2) - \sin(\phi_1) \times \cos(\phi_2) \times \cos(\Delta L)$

Where:
- $\phi_1$ = observer's latitude
- $\phi_2$ = Kaaba's latitude (21.4225°)

#### Step 3: Calculate the bearing

$\theta = \arctan2(y, x)$

The `atan2` function returns the angle in the correct quadrant, handling all cases automatically.

#### Step 4: Normalize to 0-360°

$\text{Qibla} = (\theta + 360) \bmod 360$

This ensures the result is always in the range [0°, 360°].

---

## Step-by-Step Calculation
Here is a complete walkthrough example for New York City.

Given:
- Observer (New York): $\phi_1 = 40.7128°$, $L_1 = -74.0060°$
- Kaaba (Mecca): $\phi_2 = 21.4225°$, $L_2 = 39.8262°$

### Step 1: Longitude Difference
$\Delta L = 39.8262° - (-74.0060°) = 113.8322°$

### Step 2: Calculate $y$
$y = \sin(113.8322°) \times \cos(21.4225°)$

$y = 0.9135 \times 0.9322 = 0.8515$

### Step 3: Calculate $x$
$x = \cos(40.7128°) \times \sin(21.4225°) - \sin(40.7128°) \times \cos(21.4225°) \times \cos(113.8322°)$

The equation breakdown:
- $\cos(40.7128°) = 0.7581$
- $\sin(21.4225°) = 0.3653$
- $\sin(40.7128°) = 0.6521$
- $\cos(21.4225°) = 0.9322$
- $\cos(113.8322°) = -0.4067$

$x = (0.7581 \times 0.3653) - (0.6521 \times 0.9322 \times -0.4067)$

$x = 0.2769 - (-0.2473) = 0.5242$

### Step 4: Calculate Bearing
$\theta = \arctan2(0.8515, 0.5242) = 58.41°$

### Step 5: Normalizing Bearing
$\text{Qibla} = (58.41° + 360°) \bmod 360° = 58.41°$

**Result:** From New York City, the Qibla direction is 58.41° from North (roughly northeast).

---

## Special Cases

### Case 1: Observer at the Kaaba
The closer you are to the Kaaba, the harder it is to get an accurate bearing. If you are standing at the Kaaba itself, there is really no specific direction that is technically valid. All you need to do is face the Kaaba you can see. This app may return an invalid bearing if you are that close.

**Coordinates**: $\phi = 21.4225°$, $L = 39.8262°$

Practically, you should check if the observer's coordinates are very close to the Kaaba (within ~1 km) and find a way to handle this edge case.

### Case 2: Antipodal Point
The antipodal point of the Kaaba is the point that is on the exact opposite side of the world:
- Latitude: -21.4225° (South)
- Longitude: -140.1738° (West)

Technically at this point (which is in the middle of the Pacific Ocean), there is no one bearing that gives you the shortest line to the Kaaba. All bearing will give you lines of the exact same length. At this location it technically don't matter where you face since all bearings give you the same lengths. This point is where the formula won't work.

**Practically**: This point is in the middle of the ocean, so most likely will never be used in a real-world scenario.

### Case 3: North and South Poles
At the North Pole ($\phi = 90\degree$), all directions point South. 
At the South Pole ($\phi = -90\degree$), all directions point North.

The formula does handles these cases mathematically, but the answer may not be intuitive.

---

## Implementation
To implement this library (`prayer_times/core/qibla.py`) you can follow the following code:
```python
def qibla_direction(your_latitude: float, your_longitude: float) -> float:
    # Step 1: Calculate longitude difference
    delta_lng = LNG_AL_KAABA - your_longitude

    # Step 2: Calculate y and x for atan2
    y = dsin(delta_lng) * dcos(LAT_AL_KAABA)
    x = (dcos(your_latitude) * dsin(LAT_AL_KAABA) -
         dsin(your_latitude) * dcos(LAT_AL_KAABA) * dcos(delta_lng))

    # Step 3: Calculate bearing using atan2
    theta = datan2(y, x)

    # Step 4: Normalize to 0-360° and round
    return round((360 + theta) % 360, 2)
```

**Note:** All the trigonometric functions (`dsin`, `dcos`, `datan2`) use degrees, not radians.

---