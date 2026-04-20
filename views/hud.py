import pygame
from settings import WHITE, RED, GOLD, GRAY, GREEN, ORANGE, DARK_GRAY, WIDTH, HEIGHT
from models.resources import HealthSystem, ScoreSystem
from models.difficulty import ProgressionSystem

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

class HUD:
    def __init__(self, font_small):
        self.font_small = font_small

    def draw(self, screen, health_system, score_system, progression, record=None, boost_timer=0):
        from settings import WIDTH, HEIGHT, WHITE, GREEN, ORANGE, RED, GRAY, DARK_GRAY, GOLD
        for i in range(health_system.MAX_HEALTH):
            draw_heart(screen, 14 + i * 32, 14, filled=(i < health_system.current))

        if score_system.mode == 3:
            dist_txt = self.font_small.render(f"{int(score_system.distance)} M", True, WHITE)
            screen.blit(dist_txt, (WIDTH - dist_txt.get_width() - 14, 14))
            if record is not None:
                best_txt = self.font_small.render(f"Record: {int(record.best_distance)} M", True, GOLD)
                screen.blit(best_txt, (WIDTH - best_txt.get_width() - 14, 34))
        else:
            for i in range(score_system.STARS_TO_WIN):
                sx = WIDTH - 14 - (score_system.STARS_TO_WIN - i) * 34
                draw_star(screen, sx, 12, filled=(i < score_system.stars))

        coin_txt = self.font_small.render(f"Coins: {score_system.coins}/{score_system.COINS_PER_STAR}", True, GOLD)
        screen.blit(coin_txt, (WIDTH - coin_txt.get_width() - 14, 56 if score_system.mode == 3 else 50))

        # Boost indicator
        if boost_timer > 0:
            boost_secs = boost_timer / 60
            boost_txt = self.font_small.render(f"⚡ BOOST {boost_secs:.1f}s", True, (0, 255, 255))
            screen.blit(boost_txt, (WIDTH//2 - boost_txt.get_width()//2, 14))

        spd_pct = (progression.speed - progression.INITIAL_SPEED) / max(0.1, (progression.MAX_SPEED - progression.INITIAL_SPEED))
        spd_txt = self.font_small.render(f"Speed  {int(progression.speed * 20)} km/h", True, GRAY)
        screen.blit(spd_txt, (14, HEIGHT - 36))
        bar_w = int(160 * spd_pct)
        pygame.draw.rect(screen, DARK_GRAY, (14, HEIGHT - 16, 160, 8), border_radius=4)
        bar_color = GREEN if spd_pct < 0.6 else (ORANGE if spd_pct < 0.85 else RED)
        if bar_w > 0:
            pygame.draw.rect(screen, bar_color, (14, HEIGHT - 16, bar_w, 8), border_radius=4)
        
        esc_txt = self.font_small.render("ESC to Menu", True, GRAY)
        screen.blit(esc_txt, (WIDTH - esc_txt.get_width() - 14, HEIGHT - 36))
