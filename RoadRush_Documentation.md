# Road Rush: The Master Documentation File

# Road Rush: Comprehensive Technical Documentation
**Prepared for Development Teams & Academic Review**

---

## Part 1: The Big Picture & Game Engine Basics

If a teacher asks you how your game works, you don't need to recite code. You just need to show them that you understand the **three fundamental concepts** that drive almost all 2D games, including *Road Rush*. 

### Concept 1: The Coordinate System (X and Y)
In math class, the origin `(0, 0)` is usually at the bottom-left of a graph.
In computers and game development (using Pygame), **`0, 0` is the top-left corner of the screen.**

*   **X-Axis:** Moves left to right. (`X=0` is the left edge, `X=480` is the right edge).
*   **Y-Axis:** Moves from top to bottom. (`Y=0` is the very top edge, `Y=800` is the bottom edge).
*   *Why this matters:* When your car drives "forward," the program actually subtracts from the Y-coordinate. When obstacles (like the Red Car) move toward you, the game *adds* to their Y-coordinate to make them fall down the screen.

### Concept 2: The Game Loop & Frames Per Second (FPS)
A video game is just a flipbook. It draws a picture, erases it, moves the objects slightly, and draws the next picture. It does this extremely fast. Our game runs at **60 Frames Per Second (FPS)**. 

If someone asks what a **"Game Loop"** is, explain that it is an infinite `while True` loop that does three things exactly 60 times every second:
1.  **Event Handling:** Did the player press the Left arrow key this frame? Did they press ESC?
2.  **Update State:** We see they pressed Left, so we update the car's `X` position. We update the timer. We move the enemy cars down by a few pixels.
3.  **Render (Draw):** We paint the screen entirely black, and then we paint the road, the car, the enemies, and the UI text at their *new* positions. 

### Concept 3: MVC Architecture (Model-View-Controller)
When building small scripts, people often put all their code into one massive file. Since *Road Rush* has AI enemies, persistent saving, UI overlays, and physics, doing that would make the code impossible to read.

Instead, we decided to build the game using **MVC Architecture**, which is an industry-standard software design pattern. If a teacher asks why you have so many folders, this is the answer: it keeps the code strictly organized by its *purpose*.

Here is how MVC is broken down in our game:

#### 1. Models (`models/` folder) - "The Data and The Rules"
*   **What it does:** Models only care about data. A car model knows its `X` and `Y` position, its color, and its lane. It does *not* know how to draw itself on the computer screen. It only handles facts.
*   **Examples:** `entities.py` (the factual properties of cars), `resources.py` (how many coins you have), `physics.py` (the math for overlapping rectangles).

#### 2. Views (`views/` folder) - "The Visuals and Sounds"
*   **What it does:** Views are blind and deaf. They only do what they are told. They take the Data from the Models and draw the pixels onto the screen, or play sounds out of the speakers.
*   **Examples:** `hud.py` (draws the yellow coins), `sound.py` (plays music), `feedback.py` (draws the "Game Over" text).

#### 3. Controllers (`controllers/` folder) - "The Middleman / The Brain"
*   **What it does:** Controllers bridge the gap. They listen to the player's keyboard, they change the Models, and they tell the Views what to show.
*   **Examples:** `collision.py` (it actively checks if a car Model hit a wall Model, and if so, it changes the Health Model), `traffic.py` (it decides when to spawn a new enemy Model), `controls.py` (handles the physical keyboard arrow keys).

---

### Project Map Summary
Here is exactly what you see when you open the main game folder:

```text
Road Rush/
├── assets/             # The raw physical `.mp3` and `.wav` media files
├── controllers/        # The Managers (Controls, Spawners, Physics collision logic)
├── models/             # The Data (Cars, Health, Road math, High-score logic)
├── views/              # The Display (Drawing screens, drawing UI, playing sound files)
├── main.py             # THE ENGINE. It glues the MVC together and runs the Game Loop.
├── settings.py         # THE RULES. Global constants like WIDTH=480, GRAY=(50,50,50).
├── strip_comments.py   # Utility script to clean up the code. (We ran it and are done with it).
├── buildozer.spec      # Instructions on how to turn this Python code into an Android APK.
└── RoadRush.spec       # Instructions on how to turn this Python code into a Windows EXE.
```


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


# Road Rush: Line-by-Line Documentation
**Prepared for Development Teams & Academic Review**

---

## Part 3: `.gitignore` (The Source Control Filter)

When working on a team project, programmers use Git and GitHub to save their code and share it. However, games often generate massive temporary folders, secret password files, and garbage cache files. If you upload these to GitHub, it ruins the project. 

The `.gitignore` file acts like a bouncer at a club. It tells Git exactly which files are **forbidden** from being saved to the online repository. Here is the line-by-line breakdown of why we block certain files:

### Python Temporary Files
```text
1: # Python
2: __pycache__/
3: *.pyc
4: *.pyo
```
*   **Line 1:** Lines starting with `#` in this file are just human-readable comments. This section organizes Python rules.
*   **Line 2:** `__pycache__/` blocks the entire folder named `__pycache__`. When Python runs your game for the first time, it translates the human code into machine code to run faster next time. It stores that machine code in this folder. We block it because everyone's computer generates their own automatically, and tracking it on GitHub causes constant conflict errors.
*   **Line 3:** `*.pyc` blocks any file ending in `.pyc` (Compiled Python Files). The `*` is a wildcard, meaning "literally any name as long as it ends with .pyc".
*   **Line 4:** `*.pyo` blocks Optimized Python Files, which are an older format of `.pyc`.

### PC Builder Files (PyInstaller)
```text
6: # PyInstaller output
7: build/
8: dist/
9: *.spec
```
*   **Line 7 & 8:** To play the game without installing Python, we use PyInstaller to build a classic `exe` app. PyInstaller dumps massive chunks of data into the `build/` and `dist/` folders. An `exe` file can be hundreds of megabytes. GitHub is designed for thousands of tiny text files. We block these folders so we don't accidentally push a 200MB `exe` into our source code storage!
*   **Line 9:** `*.spec` blocks spec files (but wait!). *Note: In our actual project development, we bypassed this rule for `RoadRush.spec` by manually adding it, because we wanted to keep the specific setup instructions safe.* 

### Android Mobile Builder Files (Buildozer)
```text
11: # Buildozer build artifacts
12: .buildozer/
13: bin/
```
*   **Line 12:** `.buildozer/` is the hidden folder where the mobile converter downloads immense amounts of Android Studio tools to compile the `APK`. It can exceed gigabytes of space. This is absolutely blocked.
*   **Line 13:** `bin/` is the final destination folder where the finished Android `APK` is dumped. Similar to the Windows `exe`, we don't want giant phone apps polluting our source code history.

### Historical Project Files
```text
15: # Extracted pptx text
16: extracted_text.txt
17: read_pptx.py
```
*   **Line 16 & 17:** Early in the project's lifespan, there was a PowerPoint presentation explaining the architecture, and a script written to extract the text from it. Since they were one-off throwaway scripts, we instruct Git to ignore them forever so they don't clutter the final project repo.

### Operating System Garbage
```text
19: # OS
20: .DS_Store
21: Thumbs.db
```
*   **Line 20:** `.DS_Store` stands for "Desktop Services Store". It is a hidden file automatically created by Apple Mac computers in almost every folder to remember where to place the icons. If a Mac user joined the team, their computer would secretly try to upload these files everywhere. We block it permanently here.
*   **Line 21:** `Thumbs.db` is the exact same concept, but for Windows computers protecting the image thumbnail caching. We block it to keep the repository strictly focused on Game Code only.


# Road Rush: Line-by-Line Documentation
**Prepared for Development Teams & Academic Review**

---

## Part 4: `RoadRush.spec` (The Windows EXE Builder Engine)

Python code cannot run on a computer unless the user goes through the hassle of downloading Python, installing libraries, and running command prompts. Normal players don't do that. They just want an `.exe` file.

We used an industry-standard package called **PyInstaller** to compile the game. When you run PyInstaller, it creates this `.spec` (Specification) file automatically. This file is essentially a set of blueprints telling the compiler how to pack our code, the Python engine, and our music into a playable Windows executable.

Here is what the compiler blueprints look like line-by-line:

### Initialization
```python
1: # -*- mode: python ; coding: utf-8 -*-
2: 
3: 
4: a = Analysis(
5:     ['main.py'],
```
*   **Line 1:** This is an encoding declaration. It guarantees the compiler will read our files using standard UTF-8 text formatting, meaning special characters won't crash the compiler.
*   **Line 4:** Initializes the `Analysis` object. Think of `Analysis` as a detective. It enters our code and tracks down every single dependency we imported.
*   **Line 5:** `['main.py']`. This tells the detective exactly where to start looking. It says, "Enter the project through `main.py` and figure out what else it needs."

### Paths and Asset Bundling
```python
6:     pathex=[],
7:     binaries=[],
8:     datas=[('assets', 'assets')],
```
*   **Line 6:** `pathex` would list other random folders on our hard drive we want to include. We leave it empty `[]` because everything is inside our game folder.
*   **Line 7:** `binaries` is where you would put extra `.dll` files (like custom physics engines). We don't need any, so it's empty.
*   **Line 8:** **This is the most critical manual edit in the file.** By default, the builder ONLY searches for `.py` code. It ignores music and images. We manually added `('assets', 'assets')`. This instructs the compiler: *"Take the entire 'assets' folder from my computer, and pack it directly into the final .exe file."* Without this line, the game would instantly crash for players when trying to play the `.mp3` music.

### Advanced Builder Options
```python
9:     hiddenimports=[],
10:    hookspath=[],
11:    hooksconfig={},
12:    runtime_hooks=[],
13:    excludes=[],
14:    noarchive=False,
15:    optimize=0,
16: )
```
*   **Lines 9–15:** These are advanced tools. `hiddenimports` forces the compiler to include libraries it might have missed. `excludes` lets us block massive unused libraries (like `numpy` or `pandas`) from bloating the file size. `optimize=0` tells the compiler not to aggressively alter our code, protecting stability over file size. 

### Generating the Output Archive
```python
17: pyz = PYZ(a.pure)
```
*   **Line 17:** PYZ stands for "Python Zip." It takes the pure Python code the detective (`Analysis`) found, compresses it entirely into a high-speed zip file, and encrypts it so players cannot easily steal the messy source code.

### The Final Executable (`exe`) Construction
```python
19: exe = EXE(
20:     pyz,
21:     a.scripts,
22:     a.binaries,
23:     a.datas,
24:     [],
25:     name='RoadRush',
26:     debug=False,
```
*   **Lines 19–24:** The `EXE` object puts the puzzle pieces together. It combines the zipped code (`pyz`), the Pygame libraries (`a.binaries`), and—most importantly—our music files we defined earlier (`a.datas`).
*   **Line 25:** `name='RoadRush'` explicitly names the final file `RoadRush.exe`.
*   **Line 26:** `debug=False` ensures that ugly developer text/warnings will not pop up in a terminal window for the end user.

### Window & System Configuration
```python
27:     bootloader_ignore_signals=False,
28:     strip=False,
29:     upx=True,
30:     upx_exclude=[],
31:     runtime_tmpdir=None,
32:     console=False,
```
*   **Line 28 & 29:** `strip` and `upx` are aggressive file compressors. UPX actively squeezes the size of the `.exe`. 
*   **Line 31:** `runtime_tmpdir=None` tells the packaged game where to temporarily extract its music when the player double-clicks the `.exe`. `None` forces it to use the default Windows temporary folder (`AppData/Local/Temp`), keeping their desktop clean.
*   **Line 32:** `console=False`. This is vital for actual game distribution. If this was `True`, a hideous black command prompt hacking window would appear behind the game. Setting it to `False` creates a pure, clean, professional windowed game just like one you'd buy from Steam.

```python
33:     disable_windowed_traceback=False,
34:     argv_emulation=False,
35:     target_arch=None,
36:     codesign_identity=None,
37:     entitlements_file=None,
38: )
```
*   **Lines 33–38:** These handle advanced system integration. For example, `target_arch` would be defined if we exclusively wanted to build for a Mac M1 Chip vs an Intel Chip. We leave them blank (`None`), letting PyInstaller automatically adapt to whatever Windows PC runs it.


# Road Rush: Line-by-Line Documentation
**Prepared for Development Teams & Academic Review**

---

## Part 5: `buildozer.spec` (The Android Mobile Builder)

Translating a Python game meant for a desktop computer into an Android app is exceptionally complex. A phone runs on a completely different operating system architecture (usually ARM) than a PC (x86). 

We used a tool called **Buildozer**, which essentially creates a tiny virtual Linux computer, downloads Android Studio, and translates your Python code into a native `.apk` file that can be installed on phones. 

Here is the line-by-line explanation of our translation blueprint. If you are asked how your game works on a phone, refer to this:

### The App Identity
```ini
1: # Buildozer spec for Road Rush
2: [app]
3: 
4: # App identity
5: title = Road Rush
6: package.name = roadrush
7: package.domain = org.roadrush
```
*   **Line 5:** `title = Road Rush` dictates the exact name that will appear under the application icon on an Android phone's home screen.
*   **Line 6 & 7:** `package.name` and `package.domain` combine to create the unique internal identifier: `org.roadrush.roadrush`. Google Play Store uses this to verify if an app is a brand-new game or just an update to an existing game. It must be unique in the world.

### Source Files & Exclusions
```ini
9: # Source — main.py must be the entry point
10: source.dir = .
11: source.include_exts = py,png,jpg,jpeg,gif,bmp,wav,ogg,mp3
12: source.exclude_dirs = __pycache__, build, dist, .git, .github, .buildozer, RoadRush.spec
```
*   **Line 10:** `source.dir = .` tells the builder that the source code is right here in this specific folder (the dot `.` signifies the current directory).
*   **Line 11:** `source.include_exts` is extremely important. We manually added `wav` and `mp3` to this. If we didn't, the compiler would ignore our music folder and the app would crash instantly on the phone when it tried to play the Start Screen music.
*   **Line 12:** `source.exclude_dirs` blocks the builder from packing garbage files or PC-only files (like `RoadRush.spec`) into the phone app.

### Core Translation Rules
```ini
14: # Version
15: version = 1.0
16: 
17: # Requirements for a pure-pygame Android app
18: # python3, sdl2, pygame are all available as p4a recipes
19: requirements = python3,sdl2,pygame
```
*   **Line 15:** Defines that this is version 1.0 of the app.
*   **Line 19:** `requirements` is the true magic line. An Android phone has zero idea what "Python" or "Pygame" is. This line strictly commands the builder: *"Download a tiny micro-version of Python3 and the SDL2 graphics engine, and force them into the app so the phone can understand the code."*

### Screen & Hardware Control
```ini
21: # Orientation
22: orientation = portrait
23: 
24: # Android settings
25: android.permissions = VIBRATE
26: android.archs = arm64-v8a, armeabi-v7a
```
*   **Line 22:** `orientation = portrait` locks the phone screen. If the user rotates their phone sideways, the game will ignore it. This prevents our 480x800 vertical game from being stretched horribly across a horizontal phone screen.
*   **Line 25:** Requests hardware permission from the Android OS to vibrate the phone (e.g., when the player crashes).
*   **Line 26:** Specifies the target processor chips (`arm64`, `armeabi`). This guarantees the app will run on 99% of modern Android devices.

### Underlying SDK Architecture
```ini
27: android.bootstrap = sdl2
28: android.minapi = 21
29: android.sdk = 34
30: android.ndk = 25b
31: android.ndk_api = 21
32: android.accept_sdk_license = True
33: android.skip_update = False
```
*   **Line 28 & 29:** `minapi = 21` means the game will refuse to install on ancient Android phones (older than Android 5.0). `sdk = 34` means the game is perfectly optimized for the absolute latest Android 14 phones.
*   **Line 30:** `ndk = 25b` forces the builder to use the Native Development Kit version 25. This was crucial for Pygame compatibility.
*   **Line 32:** Automatically accepts Google's legal user agreements so the compilation doesn't freeze halfway through waiting for a physical human to type "Yes".

### Display & Logging Toggles
```ini
35: # Fullscreen
36: fullscreen = 1
37: 
38: [buildozer]
39: log_level = 2
40: warn_on_root = 1
```
*   **Line 36:** `fullscreen = 1` hides the clock, battery percentage, and notification bar on the Android phone while playing. 
*   **Line 39:** `log_level = 2` ensures that if the translation process fails, the builder will vomit out an enormous amount of raw debug text so the developer can figure out exactly which file caused the crash.


# Road Rush: Line-by-Line Documentation
**Prepared for Development Teams & Academic Review**

---

## Part 6: `main.py` (The Engine Core)

This is the central file of the entire project. It is the "Engine" that glues all the Models, Views, and Controllers together. We will break this huge file down by its logical sections.

### 1. Imports and Setup (Lines 1 – 31)
```python
9: import pygame
10: import sys
...
13: from models.entities import Player, YellowCar, RedCar, Blocker, Coin, HeartPickup
14: from models.resources import HealthSystem, ScoreSystem, RecordSystem
...
27:     STATE_START    = "START"
...
31:     STATE_PAUSED   = "PAUSED"
```
*   **Lines 9–23:** Here we import `pygame` and literally every single class we wrote from the `models`, `views`, and `controllers` folders. 
*   **Line 25 (`class Game:`):** An Object-Oriented approach. The entire game runs as a single `Game` object. 
*   **Lines 27–31:** **State Machine definitions.** The game is always in one of these 5 modes. If it's `PAUSED`, cars stop moving. If it's `START`, the menu draws. This stops bugs where the player can die while in the menu.

### 2. The `__init__` Function: The Boot Sequence (Lines 33 – 81)
```python
34:         pygame.init()
35:         pygame.mixer.init()
36:         self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
38:         self.clock  = pygame.time.Clock()
```
*   **Lines 34–35:** Wakes up the Pygame graphics and Pygame sound (`mixer`) chips.
*   **Line 36:** Creates the actual game window based on the `WIDTH` and `HEIGHT` from `settings.py`.
*   **Line 38:** `Clock()` acts as the game's internal heartbeat, ensuring it runs exactly at 60 FPS (handled later in the loop).

```python
57:         self.sfx.load("crash", r_path("assets/sounds/crash.wav"))
...
62:         self.sfx.play_music(r_path("assets/sounds/spinopel-speed-race-344521.mp3"))
```
*   **Lines 57–62:** Loads all the sound effects into memory immediately so there is no loading lag when the player crashes. Line 62 explicitly starts the menu music automatically.

```python
73:         self.player = Player()
74:         self.all_sprites = pygame.sprite.Group(self.player)
```
*   **Lines 73–74:** Initializes the Player car, and adds it to an incredibly important Pygame feature: `sprite.Group()`. Groups allow us to update or draw 100 objects simultaneously with a single line of code later on.

### 3. `new_game(mode)`: The Reset Button (Lines 83 – 105)
```python
83:     def new_game(self, mode):
84:         self.current_mode = mode
...
100:         self.spawner = Spawner(self.player, self.all_sprites, self.enemies, self.blockers, self.coins_group, mode)
104:         pygame.time.set_timer(self.EV_SPAWN_OBSTACLE, Spawner.OBSTACLE_SPAWN_INIT_MS)
```
*   **Line 83:** This function is called when the player clicks "Easy", "Hard", or "Endless". 
*   **Lines 87–90:** Empties out all the Sprite Groups. If you died with 3 yellow cars on the screen, these lines delete them so your new game starts clean.
*   **Line 104:** Tells Pygame to trigger a hidden countdown timer. Every ~1.6 seconds, it will forcefully trigger an `EV_SPAWN_OBSTACLE` event.

### 4. `handle_events`: Listening to the Keyboard (Lines 107 – 155)
```python
107:     def handle_events(self):
108:         for event in pygame.event.get():
109:             if event.type == pygame.QUIT:
110:                 self.running = False
```
*   **Line 108:** This checks every button press you've made in the last 1/60th of a second.
*   **Lines 109–110:** If the player clicks the red 'X' in the top right of the Windows window, `self.running = False` breaks the infinite loop and gracefully closes the game.
*   **Lines 117–123:** If `state == STATE_START`, it ignores arrow keys and instead asks the `InputHandler` if you clicked a difficulty box. If you did, it switches the music and calls `new_game()`.
*   **Lines 141–152:** If `state == STATE_PLAYING`, it listens for the hidden timer events we set up earlier. If an obstacle timer goes off, it tells the Spawner controller to create a car.
*   **Line 155:** If nothing else happened, it sends the keyboard instructions to `handle_player_input` so the player car can change lanes. 

### 5. `update`: The Physics Engine (Lines 157 – 235)
```python
157:     def update(self):
158:         if self.state != self.STATE_PLAYING:
159:             return
```
*   **Lines 158–159:** If we are paused, dead, or in the menu, immediately cancel out of the update loop. This completely freezes the cars in place.

```python
163:         if self.boost_timer > 0:
164:             self.boost_timer -= 1
165:             effective_speed = self.progression.speed + self.boost_speed_bonus
...
174:         self.score_system.add_distance(effective_speed)
179:         self.road_system.update(effective_speed)
182:         self.enemies.update(effective_speed)
```
*   **Lines 163–174:** Checks if you collected 30 coins for a Boost. If you did, you get a massive `speed_bonus`. 
*   **Lines 179–182:** It takes that speed and applies it to the road stripes and the enemy cars. They all scroll downward at that exact speed.

```python
204:         new_state = self.collision_system.process_interactions(...)
...
219:         if new_state == "GAMEOVER":
220:             self.state = self.STATE_GAMEOVER
226:             self.sfx.play("lose")
```
*   **Line 204:** We pass all cars and players to our custom `CollisionSystem` to do the heavy math.
*   **Lines 219–226:** If the math detects the player lost their last heart, we lock the game into the `GAMEOVER` state and play the "lose" sound effect.

### 6. `draw`: Painting the Screen (Lines 237 – 268)
```python
237:     def draw(self):
...
241:         elif self.state == self.STATE_PLAYING:
242:             self.road.draw(self.screen)
247:             self.all_sprites.draw(self.screen)
248:             self.hud.draw(...)
268:         pygame.display.flip()
```
*   **Line 242:** Paints the gray background and white stripes first.
*   **Line 247:** Paints the cars *on top* of the road (order matters!).
*   **Line 248:** Paints the Hearts, Score, and Speedometer text *on top* of the cars.
*   **Line 268:** `pygame.display.flip()`. All drawing is actually done backstage. This command "flips" the backstage canvas to the front, revealing it instantly to the player to prevent screen tearing.

### 7. The Infinite Loop (Lines 270 – 281)
```python
270:     def run(self):
271:         while self.running:
272:             self.handle_events()
273:             self.update()
274:             self.draw()
275:             self.clock.tick(FPS)
280:     game = Game()
281:     game.run()
```
*   **Lines 271–275:** The beating heart of the game. It loops infinitely: Event -> Update -> Draw. 
*   **Line 275:** `clock.tick(FPS)`. If a computer is super fast, it might run this loop 5,000 times a second, crashing the cars instantly. This command puts the computer to sleep for milliseconds, forcing it to run exactly 60 times a second.
*   **Lines 280–281:** The moment Python opens `main.py`, it creates the massive Game Engine object, and calls `.run()` to start the heartbeat.


# Road Rush: Line-by-Line Documentation
**Prepared for Development Teams & Academic Review**

---

## Part 7: The Game Models (`models` folder)

In MVC Architecture, "Models" are the raw data and physical rules of the world. They do not know what the screen looks like; they only know math. This folder contains all the tangible objects you interact with constraint, scaling, and scoring.

### 1. `entities.py` (The Physical Objects)
This file dictates creating the cars and hitboxes.

```python
25: class Player(pygame.sprite.Sprite):
26:     def __init__(self):
35:         self.lane_index = 1
36:         self.rect.centerx = RoadSystem.get_lane_x(self.lane_index)
37:         self.rect.bottom = HEIGHT - 20
```
*   **Lines 25–37:** This creates the Player car. It forces the player to start in `lane_index = 1` (the second lane from the left). `rect` stands for Rectangle (the mathematical box representing the car), and we pin the bottom of the player's box exactly 20 pixels above the bottom of the screen (`HEIGHT - 20`).

```python
106: class RedCar(pygame.sprite.Sprite):
...
139:     def update(self, game_speed):
140:         self.exact_y += max(1.0, game_speed - 1.0)
```
*   **Lines 106–140:** This is the logic for the complex enemy AI. Notice `game_speed - 1.0`. The Red Car is mathematically designed to travel exactly 20 km/h slower than the player's speed (`1.0` speed unit), meaning it will slowly approach you from the top of the screen perfectly, no matter how fast you are driving.

```python
155:         else:
156:             if self.rect.top >= 0 and self.rect.top < self.player.rect.top:
157:                 if self.track_cooldown <= 0:
158:                     if self.lane_index < self.player.lane_index:
159:                         self.lane_index += 1  
```
*   **Lines 155–159:** The relentless Hard Mode tracker logic. If the Red Car is behind you (`self.rect.top < self.player.rect.top`), it checks if its cooldown timer has ended. If it has, it looks at the player's lane and shifts right (`+= 1`) or left (`-= 1`) to hunt them down. 

### 2. `physics.py` (The Collision Math)
```python
4: def check_collisions_aabb(sprite_to_check, group, hitbox_factor=0.8):
5:     for sprite in group:
6:         shrink_x = int(sprite.rect.width * (1 - hitbox_factor) / 2)
```
*   **Lines 4–6:** "AABB" stands for *Axis-Aligned Bounding Box*. It creates an invisible smaller box inside the car image. The `hitbox_factor=0.8` shrinks the crash zone to 80% of the image size. This is crucial for games; players hate when they visibly "dodge" a car but get hit by the invisible empty pixels near the side mirror. This gives the player a 20% margin of safety!

### 3. `difficulty.py` (The Speed Controller)
```python
12:         if mode == DifficultySettings.MODE_EASY:
13:             self.INITIAL_SPEED = 2.5
14:             self.MAX_SPEED = 7.0
15:             self.SPEED_INCREASE_AMOUNT = 0.5
16:         else: 
17:             self.INITIAL_SPEED = 3.5
18:             self.MAX_SPEED = 16.5
19:             self.SPEED_INCREASE_AMOUNT = 0.8
```
*   **Lines 12–19:** Extremely clear limits. In Easy Mode, you cap out at `7.0` (140 km/h). In Hard/Endless, you climb to `16.5` (an extreme 330 km/h) and the difficulty ramps up almost twice as fast (`0.8` jump).

### 4. `resources.py` (Scores and Progress)
```python
25:     def check_and_update(self, distance):
26:         if distance > self.best_distance:
27:             self.best_distance = distance
28:             self._save()
29:             return True
```
*   **Lines 25–29:** The High Score saver. Every time you die in Endless mode, it compares your run (`distance`) to the saved run (`self.best_distance`). If you beat it, it overwrites the `.roadrush_record.txt` file on your hard drive. 

```python
47:         if mode == 3:
48:             self.COINS_PER_STAR = 30
49:             self.STARS_TO_WIN = 999999
50:         elif mode == 2:
```
*   **Lines 47–50:** This sets the star thresholds. In Endless Mode (Mode `3`), you need 30 coins to earn a star which triggers the invincibility boost, and the amount to win is 999999—meaning you can never actually win the mode.

### 5. `road.py` (The Spatial Map)
```python
7: class RoadSystem:
8:     LANE_COUNT = 4
9:     LANES = [ROAD_LEFT + i * LANE_WIDTH + LANE_WIDTH // 2 for i in range(4)]
```
*   **Lines 7–9:** This is pure geometry. We tell it there are `4` lanes. The math perfectly calculates the exact center pixel of each lane dynamically. `ROAD_LEFT` is 40, `LANE_WIDTH` is 100. So the center of Lane 0 is 40 + (0) + 50 = 90. When a car asks "Where is the 1st lane?", it instantly answers `X=90`.


# Road Rush: Line-by-Line Documentation
**Prepared for Development Teams & Academic Review**

---

## Part 8: The Controllers (`controllers` folder)

In MVC Architecture, "Controllers" are the brains of the operation. If the Models are the cars on the road, the Controllers are the physical humans driving them. They listen for keyboard input, they dictate what happens during an accident, and they control the "Traffic Spawner" that decides when to create new obstacles.

### 1. `controls.py` (Handling Player Input)
This file strictly translates what happens on a physical keyboard into what happens inside the game.

```python
37:     def handle_player_input(event, player):
38:         if event.type == pygame.KEYDOWN:
39:             if event.key == pygame.K_LEFT:
40:                 player.move_left()
41:             elif event.key == pygame.K_RIGHT:
42:                 player.move_right()
```
*   **Lines 37–42:** This explicitly checks Keyboard events (`KEYDOWN`). If the physical button pressed was `K_LEFT`, it sends a command to the `player` Model saying "Move Left". The player Model then controls how to actually do that mathematically. 

```python
24:     def get_pause_interaction(event, w, h):
25:         if event.type == pygame.KEYDOWN:
26:             if event.key == pygame.K_ESCAPE:
27:                 return "RESUME"
```
*   **Lines 24–27:** Even menu logic is handled here. If the game is paused, hitting `K_ESCAPE` instantly returns the text `"RESUME"`, which the Engine (`main.py`) reads and uses to unpause the game.

### 2. `traffic.py` (The Spawner / Game Director)
This file is the "Traffic Cop". It uses random number generation to actively decide *how* and *when* to place cars and coins on the road.

```python
29:     def spawn_obstacle(self):
30:         occupied_lanes = {s.lane_index for s in self.enemies} 
31:         occupied_lanes.update({s.lane_index for s in self.blockers})
```
*   **Lines 29–31:** A crucial safety check. It takes the list of `enemies` and `blockers`, checks what lanes they are currently in, and stores them in a Python `Set` (a list of unique items). This allows the Spawner to immediately know which lanes are currently blocked so it doesn't accidentally spawn two cars on top of each other.

```python
37:         if self.mode == DifficultySettings.MODE_HARD:
38:             if random.random() < 0.65:
39:                 obs = YellowCar(lane)
40:             else:
41:                 obs = RedCar(lane, self.player)
```
*   **Lines 37–41:** Probability Math. In Hard Mode, it rolls a random percentage between 0.0 and 1.0 using `random.random()`. If the number is below `0.65` (meaning there is a 65% chance), it drops a Yellow Car. If not (35% chance), it drops the much more dangerous tracking Red Car.

### 3. `collision.py` (The Police / Physics Arbitrator)
This file actively watches the game waiting for cars to touch. If a crash occurs, it executes the consequences.

```python
10:     def process_interactions(self, player, enemies, blockers, coins, health, score):
...
13:         if player.inv_frames > 0:
14:             hit_enemies = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask)
15:             if hit_enemies:
16:                 self.sfx.play("crash")
17:             return "PLAYING"
```
*   **Lines 13–17:** When the player collects 30 coins for the Endless Boost, their `inv_frames` turns on. This function checks if they are invincible. If they hit a car while invincible, we instantly delete the enemy car (`True`), play a crash sound, and the player gets to keep driving safely (`return "PLAYING"`). 

```python
20:         hit_enemies = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask)
21:         hit_blockers = pygame.sprite.spritecollide(player, blockers, False, pygame.sprite.collide_mask)
...
24:             health.current -= 1
25:             self.sfx.play("crash")
26:             player.reset_invincibility()
```
*   **Lines 20–26:** The standard damage flow. The `spritecollide` tool mathematically overlaps the car rectangles. Notice `False`—the enemy car is NOT deleted this time. If a crash occurs, the game strips exactly 1 point of Health.

```python
28:             if health.current <= 0:
29:                 return "GAMEOVER"
```
*   **Lines 28–29:** The death check. If health hits `0`, it completely halts the game loop by returning `"GAMEOVER"`, signaling to `main.py` that the player has died.


# Road Rush: Line-by-Line Documentation
**Prepared for Development Teams & Academic Review**

---

## Part 9: The Views (`views` folder)

In MVC Architecture, "Views" are entirely responsible for the final output that the player actually sees and hears. They take raw text or math from the Models (like `Health = 2` or `Score = 150`), and they physically paint those numbers as red hearts and white text onto the computer monitor.

### 1. `sound.py` (The Audio Engine)
This file handles loading the custom `lnplusmusic` and `spinopel` soundtracks, and triggering the crash effects.

```python
4: class SoundManager:
5:     def __init__(self):
6:         self.sounds = {}
...
8:     def load(self, name, path):
9:         self.sounds[name] = pygame.mixer.Sound(path)
```
*   **Lines 4–9:** We initialize an empty Python Dictionary `{}`. A dictionary stores "Keys" and "Values". When we call `load("crash", "assets/crash.wav")`, it takes that exact `.wav` file off the hard drive, translates it into Pygame audio, and stores it under the word `"crash"`. 

```python
11:     def play(self, name):
12:         if name in self.sounds:
13:             self.sounds[name].play()
```
*   **Lines 11–13:** Very simple logic. When the collision system says `play("crash")`, the manager looks inside the dictionary. If it finds the sound, it plays it immediately. 

```python
15:     def play_music(self, path, loops=-1):
16:         pygame.mixer.music.load(path)
17:         pygame.mixer.music.play(loops)
```
*   **Lines 15–17:** Sound Effects (like crashing) use `mixer.Sound`. But background music uses `mixer.music`. Music files are massive (`.mp3`), so Pygame streams them dynamically instead of loading the whole 5-minute song into RAM. `loops=-1` tells Pygame to loop the music infinitely until the game ends.

### 2. `hud.py` (The Heads-Up Display)
The HUD paints the UI overlay on top of the moving cars.

```python
6: def draw_heart(surf, x, y, filled=True):
7:     color = RED if filled else (80, 40, 40)
8:     pygame.draw.circle(surf, color, (x + 6,  y + 6),  7)
9:     pygame.draw.circle(surf, color, (x + 16, y + 6),  7)
10:    pts = [(x - 1, y + 8), (x + 11, y + 21), (x + 23, y + 8)]
11:    pygame.draw.polygon(surf, color, pts)
```
*   **Lines 6–11:** How to draw a heart. Pygame does not have a built-in "draw heart" command. We had to use geometry. We draw two red circles side-by-side (`draw.circle`), and then draw a single triangle (`draw.polygon`) pointing downwards underneath them to form the shape of a heart. `filled=True` makes it bright red, `filled=False` paints it dark maroon to symbolize a missing, lost heart.

```python
43:         distance_str = f"Distance: {int(score.distance)} m"
44:         distance_surf = self.font.render(distance_str, True, WHITE)
45:         surf.blit(distance_surf, (WIDTH - distance_surf.get_width() - 10, 10))
```
*   **Lines 43–45:** First, we format the pure math distance into a string (`Distance: 50m`). Next, `font.render()` converts those letters into physical white pixels. Finally, `surf.blit()` is the ultimate command that slams those pixels directly onto the monitor into the top-right corner (`WIDTH - distance_surf.get_width()`).

### 3. `graphics.py` (The Road Renderer)
This paints the asphalt and the moving white stripes dividing the lanes.

```python
13:     def draw_road(self, surface):
14:         surface.fill(GRASS_LEFT)
15:         pygame.draw.rect(surface, ROAD_COLOR, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
```
*   **Lines 13–15:** Every single frame, we spray-paint the entire screen green (`GRASS_LEFT`). Then, we instantly paint a massive gray rectangle (`ROAD_COLOR`) straight down the middle to represent the asphalt.

```python
25:         for i in range(1, 4):
26:             line_x = ROAD_LEFT + i * LANE_WIDTH - DASH_WIDTH // 2
27:             for y in range(0, HEIGHT + DASH_HEIGHT + DASH_GAP, DASH_HEIGHT + DASH_GAP):
28:                 adj_y = y + self.road_system.scroll_offset
29:                 pygame.draw.rect(surface, LANE_LINE, (line_x, adj_y, DASH_WIDTH, DASH_HEIGHT))
```
*   **Lines 25–29:** Drawing the white dashed stripes is an illusion! We create a mathematical loop that paints white dashes (`LANE_LINE`) all the way down the screen. The magic is in `adj_y = y + road_system.scroll_offset`. Every frame, we move the start position of these lines downwards. Since the background stays still and the lines move down, it creates a perfect optical illusion that the green grass and car are flying forward!

### 4. `feedback.py` (Menu Screens and Pauses)
```python
28:     def draw_pause_screen(self, surface):
29:         overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
30:         overlay.fill(SHADOW)
31:         surface.blit(overlay, (0, 0))
```
*   **Lines 28–31:** When you press ESC, the entire game pauses. To make it *"look"* paused, we create a piece of virtual glass the exact size of the screen (`WIDTH, HEIGHT`). We tint that glass slightly black (`SHADOW`), and then we slap it directly over the camera (`surface.blit`). This dims the entire game instantly to indicate it is paused while we paint the "PAUSED" text on top of it.




# Road Rush: Line-by-Line Documentation
**Prepared for Development Teams & Academic Review**

---

## Part 10: Understanding `self` and `Sprite` 
*(A line-by-line breakdown of how we create cars)*

To truly understand where `self` comes from and what a `Sprite` is, we have to look exactly at lines 25 through 37 in **`models/entities.py`**. This is the exact code that builds the Player's car.

Here is the line-by-line breakdown of the code:

### Where does "Sprite" come from?
```python
1: import pygame
...
25: class Player(pygame.sprite.Sprite):
```
*   **Line 1:** We import the giant Pygame library, which contains thousands of pre-written tools made by other developers.
*   **Line 25:** This is where `Sprite` comes from. A "Sprite" is just a Pygame tool that handles drawing 2D pictures and calculating math hitboxes automatically. By writing `(pygame.sprite.Sprite)` in the parentheses, our `Player` class legally "inherits" all the powers of a Pygame Sprite. 

### Where does `self` come from?
```python
26:     def __init__(self):
27:         super().__init__()
```
*   **Line 26:** This is the absolute core of your question. `__init__` means "Initialize" (or "Birth"). It is the very first function that runs the millisecond a car is created. 
*   **But why `(self)`?** In Python, whenever a Class creates a specific object (like creating physical Car #1), that object needs a way to refer to its own physical body. Python *forces* you to write `self` as the very first word in the parentheses. `self` is literally a variable representing "the specific car being born right now."
*   **Line 27:** `super().__init__()` tells the Pygame `Sprite` tool to wake up and attach itself to our new car.

### Using `self` to attach data to the car
```python
28:         self.image_normal = pygame.Surface((CAR_W, CAR_H), pygame.SRCALPHA)
29:         _draw_car(self.image_normal, BLUE, BLUE_LIGHT, CAR_W, CAR_H)
30:         self.image = self.image_normal
```
*   **Line 28:** If we just typed `image_normal = ...`, the image would vanish the second the `__init__` function finished running. By typing `self.image_normal`, we staple the image directly to the body of the car permanently.
*   **Line 30:** `self.image` is a magic variable. Because our car is a `pygame.sprite.Sprite`, Pygame secretly looks directly at `self.image` every single frame to know what picture to draw on the screen.

### Using `self` for math and collision
```python
32:         self.rect = self.image.get_rect()
33:         self.radius = CAR_W // 2
...
35:         self.lane_index = 1
36:         self.rect.centerx = RoadSystem.get_lane_x(self.lane_index)
```
*   **Line 32:** `self.rect` is the second magic Sprite variable. `get_rect()` draws an invisible mathematical box exactly the size of `self.image`. Pygame uses `self.rect` to know if your car crashed into a wall.
*   **Line 35 & 36:** We set `self.lane_index = 1`. Because we used `self`, we can access `self.lane_index` 200 lines later in another file to know exactly what lane this specific car is driving in.

### SUMMARY FOR TEACHERS:
If the teacher asks: 
*   **"What is a Sprite?"** -> *"A Sprite is a built-in Pygame tool we imported that automatically handles the math for 2D images (`self.image`) and hitboxes (`self.rect`)."*
*   **"What is self?"** -> *"Self is a requirement in Python Object-Oriented Programming. It is a label that allows a specific object to refer to its own personal data. If we just typed `health = 3`, the code would crash because it wouldn't know WHOSE health. We type `self.health = 3` so the specific car knows we are talking about its specific body."*

