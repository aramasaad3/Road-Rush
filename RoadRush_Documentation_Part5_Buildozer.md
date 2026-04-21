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
