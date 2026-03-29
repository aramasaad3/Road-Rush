import pygame
import math
from settings import *

# ─────────────────────────────────────────────────────────────────────────────
# Helper: draw a rounded car body
# ─────────────────────────────────────────────────────────────────────────────
def _draw_car(surface, body_color, accent_color, w, h):
    """Draw a stylized top-down car onto *surface* (which is w×h)."""
    # Body
    pygame.draw.rect(surface, body_color, (4, 8, w-8, h-16), border_radius=10)
    # Roof / windshield
    pygame.draw.rect(surface, accent_color, (8, h//4, w-16, h//3), border_radius=6)
    # Front lights
    pygame.draw.rect(surface, (255, 255, 200), (6, 8, 10, 8), border_radius=3)
    pygame.draw.rect(surface, (255, 255, 200), (w-16, 8, 10, 8), border_radius=3)
    # Rear lights
    pygame.draw.rect(surface, (220, 60, 60), (6, h-20, 10, 8), border_radius=3)
    pygame.draw.rect(surface, (220, 60, 60), (w-16, h-20, 10, 8), border_radius=3)
    # Wheels
    for x in (3, w-11):
        for y in (12, h-28):
            pygame.draw.rect(surface, BLACK, (x, y, 8, 16), border_radius=4)


# ─────────────────────────────────────────────────────────────────────────────
# Player
# ─────────────────────────────────────────────────────────────────────────────
# Lerp speed: fraction of distance covered per frame (0.0–1.0)
# Higher = snappier;  Lower = more floaty
STEER_LERP = 0.18

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_normal = pygame.Surface((CAR_W, CAR_H), pygame.SRCALPHA)
        _draw_car(self.image_normal, BLUE, BLUE_LIGHT, CAR_W, CAR_H)

        # Flashing image for invincibility
        self.image_flash = pygame.Surface((CAR_W, CAR_H), pygame.SRCALPHA)
        _draw_car(self.image_flash, (50, 50, 50), (100, 100, 100), CAR_W, CAR_H)

        self.image = self.image_normal
        self.rect  = self.image.get_rect()

        self.lane_index = 1
        # Float x positions for smooth interpolation
        self.current_x = float(LANES[self.lane_index])
        self.target_x  = float(LANES[self.lane_index])
        self.rect.centerx = int(self.current_x)
        self.rect.bottom  = HEIGHT - 60

        # Stats
        self.health = MAX_HEALTH
        self.stars  = 0
        self.coins  = 0

        # Invincibility
        self.inv_frames = 0
        self.flash_tick = 0

    # ── Movement: sets new target; car glides smoothly each frame ─────────────
    def move_left(self):
        if self.lane_index > 0:
            self.lane_index -= 1
            self.target_x = float(LANES[self.lane_index])

    def move_right(self):
        if self.lane_index < LANE_COUNT - 1:
            self.lane_index += 1
            self.target_x = float(LANES[self.lane_index])

    # ── Called after collision; returns True if actually took damage ───────────
    def take_hit(self):
        if self.inv_frames > 0:
            return False
        self.health -= 1
        self.inv_frames = INVINCIBILITY_FRAMES
        return True

    def update(self, _=None):
        # ── Smooth lateral slide ───────────────────────────────────────────────
        diff = self.target_x - self.current_x
        if abs(diff) < 0.5:
            self.current_x = self.target_x          # snap to rest when close enough
        else:
            self.current_x += diff * STEER_LERP     # exponential ease-in-out
        self.rect.centerx = int(self.current_x)

        # ── Invincibility blink ───────────────────────────────────────────────
        if self.inv_frames > 0:
            self.inv_frames -= 1
            self.flash_tick += 1
            self.image = self.image_flash if (self.flash_tick // 6) % 2 else self.image_normal
        else:
            self.flash_tick = 0
            self.image = self.image_normal

    def reset(self):
        self.lane_index = 1
        self.current_x  = float(LANES[self.lane_index])
        self.target_x   = float(LANES[self.lane_index])
        self.rect.centerx = int(self.current_x)
        self.health  = MAX_HEALTH
        self.stars   = 0
        self.coins   = 0
        self.inv_frames = 0
        self.flash_tick = 0
        self.image = self.image_normal


# ─────────────────────────────────────────────────────────────────────────────
# Simple Enemy – Yellow Car (straight-line mover)
# ─────────────────────────────────────────────────────────────────────────────
class YellowCar(pygame.sprite.Sprite):
    def __init__(self, lane_index, y_pos):
        super().__init__()
        self.image = pygame.Surface((CAR_W, CAR_H), pygame.SRCALPHA)
        _draw_car(self.image, YELLOW_DK, YELLOW, CAR_W, CAR_H)
        self.rect = self.image.get_rect()
        self.lane_index = lane_index
        self.rect.centerx = LANES[self.lane_index]
        self.rect.y = y_pos

    def update(self, game_speed):
        self.rect.y += game_speed * 0.75
        if self.rect.top > HEIGHT:
            self.kill()


# ─────────────────────────────────────────────────────────────────────────────
# Complex Enemy – Red Car
# Spawns in a random lane, shifts ONE lane toward the player exactly once,
# then drives straight for the rest of its life.
# ─────────────────────────────────────────────────────────────────────────────
class RedCar(pygame.sprite.Sprite):
    def __init__(self, y_pos, player):
        super().__init__()
        self.image = pygame.Surface((CAR_W, CAR_H), pygame.SRCALPHA)
        _draw_car(self.image, (180, 20, 20), RED, CAR_W, CAR_H)
        self.rect = self.image.get_rect()
        self.player = player

        # Spawn in a random lane (independent of player)
        import random
        self.lane_index = random.randint(0, LANE_COUNT - 1)
        self.rect.centerx = LANES[self.lane_index]
        self.rect.y = y_pos

        # Flag: has the one-time lane shift already happened?
        self.has_moved = False

    def update(self, game_speed):
        self.rect.y += game_speed * 0.85
        if self.rect.top > HEIGHT:
            self.kill()
            return

        # ── One-time ambush move ───────────────────────────────────────────────
        # Only shift once the car is fully on screen so the player can see it
        if not self.has_moved and self.rect.top >= 0:
            self.has_moved = True
            if self.lane_index < self.player.lane_index:
                self.lane_index += 1          # one step toward player
            elif self.lane_index > self.player.lane_index:
                self.lane_index -= 1          # one step toward player
            # If already in same lane → no move needed, stays put
            self.rect.centerx = LANES[self.lane_index]


# ─────────────────────────────────────────────────────────────────────────────
# Static Hazard – Concrete Blocker
# ─────────────────────────────────────────────────────────────────────────────
class Blocker(pygame.sprite.Sprite):
    def __init__(self, lane_index, y_pos):
        super().__init__()
        w, h = CAR_W + 6, CAR_H - 30
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (100, 100, 110), (0, 0, w, h), border_radius=5)
        # Stripes
        for i in range(3):
            stripe_x = 6 + i * (w // 3)
            pygame.draw.rect(self.image, (220, 80, 30), (stripe_x, 0, 8, h))
        pygame.draw.rect(self.image, (60, 60, 70), (0, 0, w, h), 3, border_radius=5)
        self.rect = self.image.get_rect()
        self.lane_index = lane_index
        self.rect.centerx = LANES[self.lane_index]
        self.rect.y = y_pos

    def update(self, game_speed):
        self.rect.y += game_speed
        if self.rect.top > HEIGHT:
            self.kill()


# ─────────────────────────────────────────────────────────────────────────────
# Collectible – Coin  
# ─────────────────────────────────────────────────────────────────────────────
class Coin(pygame.sprite.Sprite):
    def __init__(self, lane_index, y_pos):
        super().__init__()
        size = COIN_R * 2 + 4
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GOLD,     (size//2, size//2), COIN_R)
        pygame.draw.circle(self.image, YELLOW,   (size//2, size//2), COIN_R - 4)
        pygame.draw.circle(self.image, GOLD,     (size//2, size//2), COIN_R, 2)
        self.rect = self.image.get_rect()
        self.rect.centerx = LANES[lane_index]
        self.rect.y = y_pos
        self.lane_index = lane_index
        self._angle = 0  # for animation

    def update(self, game_speed):
        self.rect.y += game_speed
        if self.rect.top > HEIGHT:
            self.kill()
