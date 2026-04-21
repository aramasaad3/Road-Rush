# Road Rush: Line-by-Line Documentation
**Prepared for Development Teams & Academic Review**

---

## Part 2: `settings.py` (The Master Configuration File)

This file is the "dictionary" for the game. Every other file looks here when it needs to know how big the screen is, what a specific color looks like, or how wide the road should be. Keeping these numbers in one file prevents errors across the project. 

Here is the exact line-by-line breakdown:

### Setup & Display Defaults
```python
1: import pygame
2: 
3: WIDTH  = 480
4: HEIGHT = 800
5: FPS    = 60
6: TITLE  = "Road Rush"
```
*   **Line 1:** Brings the Pygame library into the file so we can use its tools if necessary.
*   **Line 3:** `WIDTH = 480` sets the virtual width of the game window to 480 pixels.
*   **Line 4:** `HEIGHT = 800` sets the height to 800 pixels. This creates a vertical "phone-style" portrait window. 
*   **Line 5:** `FPS = 60` locks the game to exactly 60 Frames Per Second. The game loop will not run faster than 60 times a second.
*   **Line 6:** `TITLE = "Road Rush"` defines the text that will appear in the top title bar of the Windows window.

### RGB Color Definitions
```python
8: WHITE      = (255, 255, 255)
9: BLACK      = (0,   0,   0  )
10: RED        = (220, 50,  50 )
11: DARK_RED   = (120, 0,   0  )
12: BLUE       = (50,  120, 230)
13: BLUE_LIGHT = (100, 170, 255)
14: YELLOW     = (255, 220, 30 )
15: YELLOW_DK  = (200, 160, 0  )
16: GRAY       = (130, 130, 140)
17: DARK_GRAY  = (40,  42,  54 )
18: ROAD_COLOR = (55,  57,  68 )
19: GRASS_LEFT = (40,  80,  40 )
20: GRASS_RIGHT= (40,  80,  40 )
21: LANE_LINE  = (220, 220, 220)
22: GOLD       = (255, 200, 30 )
23: ORANGE     = (255, 140, 0  )
24: GREEN      = (80,  220, 100)
25: SHADOW     = (0,   0,   0,  90)
```
*   **Lines 8–24:** Computers understand colors as 3 numbers mixed together: **Red, Green, Blue (RGB)**. Each number is between `0` (off) and `255` (full throttle). For example, `(255, 255, 255)` means all light is on, creating `WHITE`. Instead of typing `(220, 50, 50)` everywhere in the code, we define it as `RED` here.
*   **Line 25:** Notice `SHADOW` has *four* numbers: `(0, 0, 0, 90)`. The last number is the "Alpha channel" (transparency). A `90` means it will be a semi-transparent black overlay.

### Dimensions & Object Sizes
```python
27: CAR_W   = 54
28: CAR_H   = 90
29: COIN_R  = 12
```
*   **Line 27:** `CAR_W = 54` sets all cars (Player, Yellow, Red) to be 54 pixels wide.
*   **Line 28:** `CAR_H = 90` sets all cars to be 90 pixels tall.
*   **Line 29:** `COIN_R = 12` sets the Radius (half the width of a circle) of the gold coins to 12 pixels. 

### Gameplay Rules
```python
31: INVINCIBILITY_FRAMES   = 90
32: RED_CAR_TRACK_FRAMES   = 50
```
*   **Line 31:** `INVINCIBILITY_FRAMES = 90`. Since the game runs at 60 FPS, this equals exactly 1.5 seconds. When the player takes damage, they briefly blink and become invincible for 1.5 seconds.
*   **Line 32:** `RED_CAR_TRACK_FRAMES = 50`. The interval the red car waits before re-calculating the player's exact position to hunt them down. 

### The Map & Road Geometry
```python
34: DASH_HEIGHT = 30
35: DASH_GAP    = 30
36: DASH_WIDTH  = 6
```
*   **Lines 34–36:** These control the white dividing lines on the street. Each painted strip is 30 pixels tall, 6 pixels wide, and has an empty gap of 30 pixels before the next one appears.

```python
38: ROAD_LEFT   = 40
39: ROAD_RIGHT  = 440
40: LANE_WIDTH  = 100
```
*   **Line 38:** `ROAD_LEFT = 40`. The first 40 pixels on the far left side of the screen are green grass. The gray road starts precisely at pixel X=40.
*   **Line 39:** `ROAD_RIGHT = 440`. The gray road ends perfectly at pixel X=440. `(440 - 40)` means the actual drivable road area is exactly 400 pixels wide.
*   **Line 40:** `LANE_WIDTH = 100`. Since the road is exactly 400 pixels wide, setting each lane to 100 means we perfectly fit 4 distinct drivable lanes on the screen (`4 * 100 = 400`).
