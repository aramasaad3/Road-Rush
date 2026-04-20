import pygame
import math
from settings import *
from models.road import RoadSystem

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
        self.current_x = float(RoadSystem.get_lane_x(self.lane_index))
        self.target_x  = float(RoadSystem.get_lane_x(self.lane_index))
        self.rect.centerx = int(self.current_x)
        self.rect.bottom  = HEIGHT - 60

        # Stats

        # Invincibility
        self.inv_frames = 0
        self.flash_tick = 0

    # ── Movement: sets new target; car glides smoothly each frame ─────────────
    def move_left(self):
        if self.lane_index > 0:
            self.lane_index -= 1
            self.target_x = float(RoadSystem.get_lane_x(self.lane_index))

    def move_right(self):
        if self.lane_index < RoadSystem.LANE_COUNT - 1:
            self.lane_index += 1
            self.target_x = float(RoadSystem.get_lane_x(self.lane_index))

    # ── Called after collision; returns True if actually took damage ───────────
    def take_hit(self):
        if self.inv_frames > 0:
            return False
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
        self.current_x  = float(RoadSystem.get_lane_x(self.lane_index))
        self.target_x   = float(RoadSystem.get_lane_x(self.lane_index))
        self.rect.centerx = int(self.current_x)
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
        self.rect.centerx = RoadSystem.get_lane_x(self.lane_index)
        self.exact_y = float(y_pos)
        self.rect.y = int(self.exact_y)

    def update(self, game_speed):
        self.exact_y += max(1.0, game_speed - 1.0) # Player speed - 20km/h
        self.rect.y = int(self.exact_y)
        if self.rect.top > HEIGHT:
            self.kill()


# ─────────────────────────────────────────────────────────────────────────────
# Complex Enemy – Red Car
# Easy: shifts ONE lane toward the player once.
# Hard/Endless: continuously tracks the player with smooth lane changes.
# ─────────────────────────────────────────────────────────────────────────────
REDCAR_LERP = 0.08  # How fast the red car slides laterally (0→1)
REDCAR_TRACK_COOLDOWN = 60  # Frames between lane-change decisions in Hard/Endless

class RedCar(pygame.sprite.Sprite):
    def __init__(self, y_pos, player, mode=1):
        super().__init__()
        self.image = pygame.Surface((CAR_W, CAR_H), pygame.SRCALPHA)
        _draw_car(self.image, (180, 20, 20), RED, CAR_W, CAR_H)
        self.rect = self.image.get_rect()
        self.player = player
        self.mode = mode

        # Spawn in a random lane (independent of player)
        import random
        self.lane_index = random.randint(0, RoadSystem.LANE_COUNT - 1)
        self.target_cx = float(RoadSystem.get_lane_x(self.lane_index))
        self.current_cx = self.target_cx
        self.rect.centerx = int(self.current_cx)
        self.exact_y = float(y_pos)
        self.rect.y = int(self.exact_y)

        # Tracking state
        self.has_moved = False          # For Easy mode one-time shift
        self.track_cooldown = 0         # For Hard/Endless continuous tracking

    def update(self, game_speed):
        self.exact_y += max(1.0, game_speed - 1.0)  # Player speed - 20km/h
        self.rect.y = int(self.exact_y)
        if self.rect.top > HEIGHT:
            self.kill()
            return

        # ── Easy mode: one-time single-lane shift ─────────────────────────────
        if self.mode == 1:
            if not self.has_moved and self.rect.top >= HEIGHT * 0.35:
                self.has_moved = True
                if self.lane_index < self.player.lane_index:
                    self.lane_index += 1
                elif self.lane_index > self.player.lane_index:
                    self.lane_index -= 1
                self.target_cx = float(RoadSystem.get_lane_x(self.lane_index))

        # ── Hard / Endless: continuous tracking while behind the player ───────
        else:
            if self.rect.top >= 0 and self.rect.top < self.player.rect.top:
                # Only re-evaluate lane after cooldown expires
                if self.track_cooldown <= 0:
                    if self.lane_index < self.player.lane_index:
                        self.lane_index += 1  # Move one lane at a time
                        self.track_cooldown = REDCAR_TRACK_COOLDOWN
                    elif self.lane_index > self.player.lane_index:
                        self.lane_index -= 1
                        self.track_cooldown = REDCAR_TRACK_COOLDOWN
                    self.target_cx = float(RoadSystem.get_lane_x(self.lane_index))
                else:
                    self.track_cooldown -= 1

        # ── Smooth cinematic slide ────────────────────────────────────────────
        diff = self.target_cx - self.current_cx
        if abs(diff) < 0.5:
            self.current_cx = self.target_cx
        else:
            self.current_cx += diff * REDCAR_LERP
        self.rect.centerx = int(self.current_cx)


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
        self.rect.centerx = RoadSystem.get_lane_x(self.lane_index)
        self.exact_y = float(y_pos)
        self.rect.y = int(self.exact_y)

    def update(self, game_speed):
        self.exact_y += game_speed
        self.rect.y = int(self.exact_y)
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
        self.rect.centerx = RoadSystem.get_lane_x(lane_index)
        self.exact_y = float(y_pos)
        self.rect.y = int(self.exact_y)
        self.lane_index = lane_index
        self._angle = 0  # for animation

    def update(self, game_speed):
        self.exact_y += game_speed
        self.rect.y = int(self.exact_y)
        if self.rect.top > HEIGHT:
            self.kill()


# ─────────────────────────────────────────────────────────────────────────────
# Collectible – Heart Pickup (Endless mode only)
# ─────────────────────────────────────────────────────────────────────────────
class HeartPickup(pygame.sprite.Sprite):
    def __init__(self, lane_index, y_pos):
        super().__init__()
        size = 30
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        # Draw a heart shape
        color = (255, 80, 100)
        pygame.draw.circle(self.image, color, (8, 10), 7)
        pygame.draw.circle(self.image, color, (22, 10), 7)
        pts = [(1, 14), (15, 28), (29, 14)]
        pygame.draw.polygon(self.image, color, pts)
        # White highlight
        pygame.draw.circle(self.image, (255, 200, 200), (8, 8), 3)

        self.rect = self.image.get_rect()
        self.lane_index = lane_index
        self.rect.centerx = RoadSystem.get_lane_x(lane_index)
        self.exact_y = float(y_pos)
        self.rect.y = int(self.exact_y)

    def update(self, game_speed):
        self.exact_y += game_speed
        self.rect.y = int(self.exact_y)
        if self.rect.top > HEIGHT:
            self.kill()
