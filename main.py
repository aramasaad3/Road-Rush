"""
Road Rush  –  main.py
A 4-lane endless highway dodger, built with Pygame.
Controls: LEFT / RIGHT arrow keys to change lanes.
Objective: Collect 10 coins per Star, earn 3 Stars to win.
          You have 3 Hearts. Don't lose them all!
"""

import pygame
import sys
import random
from settings import *
from sprites import Player, YellowCar, RedCar, Blocker, Coin


# ─────────────────────────────────────────────────────────────────────────────
# UI helpers
# ─────────────────────────────────────────────────────────────────────────────
def draw_heart(surf, x, y, filled=True):
    """Draw a ♥ heart icon at (x, y)."""
    color = RED if filled else (80, 40, 40)
    # Two circles + triangle approximation
    pygame.draw.circle(surf, color, (x + 6,  y + 6),  7)
    pygame.draw.circle(surf, color, (x + 18, y + 6),  7)
    pts = [(x, y + 10), (x + 12, y + 26), (x + 24, y + 10)]
    pygame.draw.polygon(surf, color, pts)


def draw_star(surf, x, y, filled=True):
    """Draw a ★ star outline at (x, y)."""
    color = GOLD if filled else (80, 70, 20)
    cx, cy = x + 13, y + 13
    pts = []
    for i in range(5):
        outer_a = -90 + 72 * i
        inner_a =  outer_a + 36
        ox = cx + 13 * pygame.math.Vector2(1, 0).rotate(outer_a).x
        oy = cy + 13 * pygame.math.Vector2(1, 0).rotate(outer_a).y
        ix = cx +  6 * pygame.math.Vector2(1, 0).rotate(inner_a).x
        iy = cy +  6 * pygame.math.Vector2(1, 0).rotate(inner_a).y
        pts.extend([(ox, oy), (ix, iy)])
    pygame.draw.polygon(surf, color, pts)


def load_font(size):
    try:
        return pygame.font.SysFont("Segoe UI", size, bold=True)
    except Exception:
        return pygame.font.SysFont("Arial", size, bold=True)


# ─────────────────────────────────────────────────────────────────────────────
# SFX stub  – replace file paths with real .wav/.ogg files if you have them
# ─────────────────────────────────────────────────────────────────────────────
class SoundManager:
    def __init__(self):
        self.enabled = pygame.mixer.get_init() is not None
        self._sounds = {}

    def load(self, name, path):
        if not self.enabled:
            return
        try:
            snd = pygame.mixer.Sound(path)
            self._sounds[name] = snd
        except Exception:
            pass  # file missing → silence

    def play(self, name):
        snd = self._sounds.get(name)
        if snd:
            snd.play()

    def play_music(self, path, loops=-1):
        if not self.enabled:
            return
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(loops)
        except Exception:
            pass

    def stop_music(self):
        if self.enabled:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass


# ─────────────────────────────────────────────────────────────────────────────
# Road background renderer
# ─────────────────────────────────────────────────────────────────────────────
class RoadRenderer:
    def __init__(self):
        self.scroll = 0.0
        # Pre-render one tile of the road (2× screen height to allow seamless loop)
        self.tile_h = HEIGHT
        self._tile  = self._make_tile()

    def _make_tile(self):
        surf = pygame.Surface((WIDTH, self.tile_h))
        surf.fill(ROAD_COLOR)
        # Grass strips
        pygame.draw.rect(surf, GRASS_LEFT,  (0,           0, GRASS_W, self.tile_h))
        pygame.draw.rect(surf, GRASS_RIGHT, (ROAD_RIGHT,  0, GRASS_W, self.tile_h))
        # Curb lines
        pygame.draw.rect(surf, WHITE, (GRASS_W - 2, 0, 4, self.tile_h))
        pygame.draw.rect(surf, WHITE, (ROAD_RIGHT - 2, 0, 4, self.tile_h))
        # Lane dashes
        dash_step = DASH_HEIGHT + DASH_GAP
        for lane in range(1, LANE_COUNT):
            lx = ROAD_LEFT + lane * LANE_WIDTH - DASH_WIDTH // 2
            for dy in range(0, self.tile_h + dash_step, dash_step):
                pygame.draw.rect(surf, LANE_LINE, (lx, dy, DASH_WIDTH, DASH_HEIGHT))
        return surf

    def update(self, speed):
        self.scroll += speed
        if self.scroll >= self.tile_h:
            self.scroll -= self.tile_h

    def draw(self, screen):
        offset = int(self.scroll)
        screen.blit(self._tile, (0, offset - self.tile_h))
        screen.blit(self._tile, (0, offset))


# ─────────────────────────────────────────────────────────────────────────────
# Main Game class
# ─────────────────────────────────────────────────────────────────────────────
class Game:
    # ── States ────────────────────────────────────────────────────────────────
    STATE_START    = "START"
    STATE_PLAYING  = "PLAYING"
    STATE_GAMEOVER = "GAMEOVER"
    STATE_VICTORY  = "VICTORY"

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock  = pygame.time.Clock()
        self.running = True

        # Fonts
        self.font_title  = load_font(64)
        self.font_big    = load_font(46)
        self.font_medium = load_font(28)
        self.font_small  = load_font(20)

        # Custom events
        self.EV_SPAWN_OBSTACLE = pygame.USEREVENT + 1
        self.EV_SPAWN_COIN     = pygame.USEREVENT + 2

        # Sound
        self.sfx = SoundManager()
        # Uncomment and add file paths when you have assets:
        # self.sfx.load("crash", "assets/sounds/crash.wav")
        # self.sfx.load("coin",  "assets/sounds/coin.wav")
        # self.sfx.load("star",  "assets/sounds/star.wav")
        # self.sfx.play_music("assets/sounds/bgm.ogg")

        # Road
        self.road = RoadRenderer()

        # State
        self.state = self.STATE_START

        # Placeholders so draw() never crashes before new_game()
        self.player = Player()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.enemies     = pygame.sprite.Group()
        self.blockers    = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()
        self.speed = INITIAL_SPEED
        self.tutorial_timer = 180  # frames to show tutorial

    # ── New / restart game ────────────────────────────────────────────────────
    def new_game(self):
        self.speed = INITIAL_SPEED
        self.last_speed_tick = pygame.time.get_ticks()

        self.all_sprites = pygame.sprite.Group()
        self.enemies     = pygame.sprite.Group()
        self.blockers    = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.tutorial_timer = 180

        pygame.time.set_timer(self.EV_SPAWN_OBSTACLE, OBSTACLE_SPAWN_INIT_MS)
        pygame.time.set_timer(self.EV_SPAWN_COIN,     COIN_SPAWN_MS)

    # ── Spawning ──────────────────────────────────────────────────────────────
    def _spawn_obstacle(self):
        lane = random.randint(0, LANE_COUNT - 1)
        r    = random.random()
        if r < 0.20:
            obj = Blocker(lane, -CAR_H)
            self.blockers.add(obj)
        elif r < 0.65:
            obj = YellowCar(lane, -CAR_H)
            self.enemies.add(obj)
        else:
            obj = RedCar(-CAR_H, self.player)
            self.enemies.add(obj)
        self.all_sprites.add(obj)

    def _spawn_coins(self):
        lane  = random.randint(0, LANE_COUNT - 1)
        count = random.randint(1, 4)
        for i in range(count):
            c = Coin(lane, -40 - i * 40)
            self.coins_group.add(c)
            self.all_sprites.add(c)

    # ── Event handling ────────────────────────────────────────────────────────
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # ── START screen ──────────────────────────────────────────────────
            elif self.state == self.STATE_START:
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                    self.state = self.STATE_PLAYING
                    self.new_game()

            # ── GAMEOVER / VICTORY screen ─────────────────────────────────────
            elif self.state in (self.STATE_GAMEOVER, self.STATE_VICTORY):
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                    self.state = self.STATE_START

            # ── PLAYING ───────────────────────────────────────────────────────
            if self.state == self.STATE_PLAYING:
                if event.type == self.EV_SPAWN_OBSTACLE:
                    self._spawn_obstacle()
                    # Tighten interval as speed grows
                    interval = max(
                        OBSTACLE_SPAWN_MIN_MS,
                        int(OBSTACLE_SPAWN_INIT_MS - (self.speed - INITIAL_SPEED) * 150)
                    )
                    pygame.time.set_timer(self.EV_SPAWN_OBSTACLE, interval)

                elif event.type == self.EV_SPAWN_COIN:
                    self._spawn_coins()

                # ── Keyboard (PC) ─────────────────────────────────────────────
                elif event.type == pygame.KEYDOWN:
                    if   event.key == pygame.K_LEFT:
                        self.player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.player.move_right()
                    elif event.key == pygame.K_a:
                        self.player.move_left()
                    elif event.key == pygame.K_d:
                        self.player.move_right()

                # ── Touch (Android) ───────────────────────────────────────────
                # event.x is normalised 0.0–1.0 across screen width
                elif event.type == pygame.FINGERDOWN:
                    if event.x < 0.5:
                        self.player.move_left()
                    else:
                        self.player.move_right()

    # ── Update ────────────────────────────────────────────────────────────────
    def update(self):
        if self.state != self.STATE_PLAYING:
            return

        # Speed ramp
        now = pygame.time.get_ticks()
        if now - self.last_speed_tick >= SPEED_INCREASE_MS:
            self.speed = min(self.speed + SPEED_INCREMENT, MAX_SPEED)
            self.last_speed_tick = now

        # Tutorial countdown
        if self.tutorial_timer > 0:
            self.tutorial_timer -= 1

        # Road scroll
        self.road.update(self.speed)

        # Sprites
        self.player.update()
        self.enemies.update(self.speed)
        self.blockers.update(self.speed)
        self.coins_group.update(self.speed)

        # ── Collision: enemy / blocker → damage ───────────────────────────────
        hit_enemy   = pygame.sprite.spritecollideany(self.player, self.enemies,   pygame.sprite.collide_rect_ratio(0.75))
        hit_blocker = pygame.sprite.spritecollideany(self.player, self.blockers,  pygame.sprite.collide_rect_ratio(0.75))

        if hit_enemy or hit_blocker:
            took_damage = self.player.take_hit()
            if took_damage:
                self.sfx.play("crash")
                # Remove the specific object that hit
                for obj in list(self.enemies) + list(self.blockers):
                    if obj.rect.colliderect(self.player.rect):
                        obj.kill()
                if self.player.health <= 0:
                    self.state = self.STATE_GAMEOVER
                    pygame.time.set_timer(self.EV_SPAWN_OBSTACLE, 0)
                    pygame.time.set_timer(self.EV_SPAWN_COIN,     0)

        # ── Collision: coins ──────────────────────────────────────────────────
        collected = pygame.sprite.spritecollide(self.player, self.coins_group, True, pygame.sprite.collide_circle)
        for _ in collected:
            self.player.coins += 1
            self.sfx.play("coin")
            if self.player.coins >= COINS_PER_STAR:
                self.player.coins -= COINS_PER_STAR
                self.player.stars += 1
                self.sfx.play("star")
            if self.player.stars >= STARS_TO_WIN:
                self.state = self.STATE_VICTORY
                pygame.time.set_timer(self.EV_SPAWN_OBSTACLE, 0)
                pygame.time.set_timer(self.EV_SPAWN_COIN,     0)

    # ── Draw ──────────────────────────────────────────────────────────────────
    def draw(self):
        # ── START ─────────────────────────────────────────────────────────────
        if self.state == self.STATE_START:
            self.screen.fill((15, 15, 25))
            # Animated road in background (draw road but no player shown)
            self.road.draw(self.screen)
            # Dark translucent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))

            title = self.font_title.render("ROAD RUSH", True, GOLD)
            sub   = self.font_medium.render("Dodge traffic. Collect Stars. Survive.", True, GRAY)
            hint  = self.font_small.render("← → Arrow Keys  (or A / D)  to steer", True, GRAY)
            tap   = self.font_big.render("TAP TO START", True, WHITE)

            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4 - 20))
            self.screen.blit(sub,   (WIDTH//2 - sub.get_width()//2,   HEIGHT//4 + 70))
            self.screen.blit(hint,  (WIDTH//2 - hint.get_width()//2,  HEIGHT//4 + 110))

            # Pulsate "TAP TO START"
            alpha = int(155 + 100 * abs(pygame.time.get_ticks() % 1000 / 500 - 1))
            tap_surf = pygame.Surface(tap.get_size(), pygame.SRCALPHA)
            tap_surf.blit(tap, (0, 0))
            tap_surf.set_alpha(alpha)
            self.screen.blit(tap_surf, (WIDTH//2 - tap.get_width()//2, HEIGHT * 2 // 3))

        # ── PLAYING ───────────────────────────────────────────────────────────
        elif self.state == self.STATE_PLAYING:
            self.road.draw(self.screen)

            # Critical mode vignette
            if self.player.health == 1:
                vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                vignette.fill((180, 0, 0, 40))
                self.screen.blit(vignette, (0, 0))

            # Sprites
            self.all_sprites.draw(self.screen)

            # ── HUD: Hearts (top-left) ────────────────────────────────────────
            for i in range(MAX_HEALTH):
                draw_heart(self.screen, 14 + i * 32, 14, filled=(i < self.player.health))

            # ── HUD: Stars (top-right) ────────────────────────────────────────
            for i in range(STARS_TO_WIN):
                sx = WIDTH - 14 - (STARS_TO_WIN - i) * 34
                draw_star(self.screen, sx, 12, filled=(i < self.player.stars))

            # ── HUD: Coin counter (below stars) ───────────────────────────────
            coin_txt = self.font_small.render(f"Coins: {self.player.coins}/{COINS_PER_STAR}", True, GOLD)
            self.screen.blit(coin_txt, (WIDTH - coin_txt.get_width() - 14, 50))

            # ── HUD: Speed indicator (bottom-left) ────────────────────────────
            spd_pct = (self.speed - INITIAL_SPEED) / (MAX_SPEED - INITIAL_SPEED)
            spd_txt = self.font_small.render(f"Speed  {int(self.speed * 20)} km/h", True, GRAY)
            self.screen.blit(spd_txt, (14, HEIGHT - 36))
            bar_w = int(160 * spd_pct)
            pygame.draw.rect(self.screen, DARK_GRAY, (14, HEIGHT - 16, 160, 8), border_radius=4)
            bar_color = GREEN if spd_pct < 0.6 else (ORANGE if spd_pct < 0.85 else RED)
            if bar_w > 0:
                pygame.draw.rect(self.screen, bar_color, (14, HEIGHT - 16, bar_w, 8), border_radius=4)

            # ── Tutorial banner ───────────────────────────────────────────────
            if self.tutorial_timer > 0:
                alpha = min(255, self.tutorial_timer * 4)
                tut_bg = pygame.Surface((WIDTH - 40, 44), pygame.SRCALPHA)
                tut_bg.fill((0, 0, 0, int(alpha * 0.7)))
                self.screen.blit(tut_bg, (20, HEIGHT // 2 + 80))
                tut = self.font_small.render("← → Tap to Steer  |  Avoid traffic  |  Collect Coins!", True, WHITE)
                tut.set_alpha(alpha)
                self.screen.blit(tut, (WIDTH//2 - tut.get_width()//2, HEIGHT // 2 + 90))

        # ── GAME OVER ─────────────────────────────────────────────────────────
        elif self.state == self.STATE_GAMEOVER:
            self.screen.fill((10, 5, 5))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((80, 0, 0, 120))
            self.screen.blit(overlay, (0, 0))

            go  = self.font_big.render("GAME OVER", True, RED)
            sub = self.font_medium.render(f"You collected {self.player.stars} / {STARS_TO_WIN} Stars", True, GRAY)
            tap = self.font_small.render("Tap anywhere to return to menu", True, GRAY)

            self.screen.blit(go,  (WIDTH//2 - go.get_width()//2,  HEIGHT//3 - 30))
            self.screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//3 + 40))
            # Show how many hearts were lost
            for i in range(MAX_HEALTH):
                draw_heart(self.screen, WIDTH//2 - 48 + i * 32, HEIGHT//3 + 100, filled=False)
            self.screen.blit(tap, (WIDTH//2 - tap.get_width()//2, HEIGHT * 2 // 3))

        # ── VICTORY ───────────────────────────────────────────────────────────
        elif self.state == self.STATE_VICTORY:
            self.screen.fill((5, 15, 5))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 120, 0, 80))
            self.screen.blit(overlay, (0, 0))

            vic  = self.font_big.render("VICTORY!", True, GOLD)
            sub  = self.font_medium.render("You collected all 3 Stars!", True, GREEN)
            tap  = self.font_small.render("Tap anywhere to return to menu", True, GRAY)

            self.screen.blit(vic, (WIDTH//2 - vic.get_width()//2, HEIGHT//3 - 30))
            self.screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//3 + 40))
            for i in range(STARS_TO_WIN):
                draw_star(self.screen, WIDTH//2 - 52 + i * 38, HEIGHT//3 + 100, filled=True)
            self.screen.blit(tap, (WIDTH//2 - tap.get_width()//2, HEIGHT * 2 // 3))

        pygame.display.flip()

    # ── Game loop ─────────────────────────────────────────────────────────────
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    game = Game()
    game.run()
