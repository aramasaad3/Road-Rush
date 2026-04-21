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
