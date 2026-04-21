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
