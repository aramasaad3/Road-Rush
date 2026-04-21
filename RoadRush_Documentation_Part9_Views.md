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
