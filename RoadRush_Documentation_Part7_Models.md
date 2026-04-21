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
