
from settings import WIDTH, HEIGHT, GOLD, GRAY, WHITE, RED, GREEN
from models.resources import HealthSystem, ScoreSystem
from views.hud import draw_heart, draw_star

import pygame

class FeedbackScreens:
    def __init__(self, font_title, font_big, font_medium, font_small):
        self.font_title  = font_title
        self.font_big    = font_big
        self.font_medium = font_medium
        self.font_small  = font_small

    def draw_start_screen(self, screen, road):
        from settings import WIDTH, HEIGHT, WHITE, DARK_GRAY, RED, ORANGE, GREEN
        screen.fill((15, 15, 25))
        road.draw(screen)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = self.font_title.render("ROAD RUSH", True, (255,200,30))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//6 - 20))

        y_cursors = [HEIGHT//2 - 60, HEIGHT//2 + 30, HEIGHT//2 + 120]
        colors = [(80,220,100), (255,140,0), (220,50,50)]
        texts = ["EASY MODE", "HARD MODE", "ENDLESS MODE"]
        
        btn_w, btn_h = 240, 60

        for i in range(3):
            rect = pygame.Rect(WIDTH//2 - btn_w//2, y_cursors[i], btn_w, btn_h)
            mouse_pos = pygame.mouse.get_pos()
            hover = rect.collidepoint(mouse_pos)
            color = (255, 255, 255) if hover else colors[i]
            
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (30, 30, 40), rect, width=4, border_radius=10)
            
            txt = self.font_small.render(texts[i], True, (15, 15, 20))
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, y_cursors[i] + btn_h//2 - txt.get_height()//2))

    def draw_gameover_screen(self, screen, score_system, record=None, is_new_record=False):
        from settings import WIDTH, HEIGHT, GOLD
        screen.fill((10, 5, 5))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((80, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        go  = self.font_big.render("GAME OVER", True, (220,50,50))
        if score_system.mode == 3:
            sub = self.font_medium.render(f"Distance: {int(score_system.distance)}m", True, (130,130,140))
        else:
            sub = self.font_medium.render(f"Collected {score_system.stars} / {score_system.STARS_TO_WIN} Stars", True, (130,130,140))
        tap = self.font_small.render("Tap anywhere to return to menu", True, (130,130,140))

        screen.blit(go,  (WIDTH//2 - go.get_width()//2,  HEIGHT//3 - 30))
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//3 + 40))
        
        if score_system.mode == 3 and record is not None:
            if is_new_record:
                rec_txt = self.font_medium.render("★ NEW RECORD! ★", True, GOLD)
                screen.blit(rec_txt, (WIDTH//2 - rec_txt.get_width()//2, HEIGHT//3 + 80))
            best_txt = self.font_small.render(f"Best: {int(record.best_distance)}m", True, GOLD)
            screen.blit(best_txt, (WIDTH//2 - best_txt.get_width()//2, HEIGHT//3 + 120))
        else:
            for i in range(3):
                screen.blit(self.font_medium.render("<3", True, (220, 50, 50)), (WIDTH//2 - 48 + i * 32, HEIGHT//3 + 100))
        
        screen.blit(tap, (WIDTH//2 - tap.get_width()//2, HEIGHT * 2 // 3))

    def draw_victory_screen(self, screen, score_system):
        screen.fill((5, 15, 5))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 120, 0, 80))
        screen.blit(overlay, (0, 0))

        vic  = self.font_big.render("VICTORY!", True, GOLD)
        sub  = self.font_medium.render("You collected all 3 Stars!", True, GREEN)
        tap  = self.font_small.render("Tap anywhere to return to menu", True, GRAY)

        screen.blit(vic, (WIDTH//2 - vic.get_width()//2, HEIGHT//3 - 30))
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//3 + 40))
        for i in range(score_system.STARS_TO_WIN):
            draw_star(screen, WIDTH//2 - 52 + i * 38, HEIGHT//3 + 100, filled=True)
        screen.blit(tap, (WIDTH//2 - tap.get_width()//2, HEIGHT * 2 // 3))

    def draw_tutorial(self, screen, tutorial_timer):
        if tutorial_timer > 0:
            alpha = min(255, tutorial_timer * 4)
            tut_bg = pygame.Surface((WIDTH - 40, 44), pygame.SRCALPHA)
            tut_bg.fill((0, 0, 0, int(alpha * 0.7)))
            screen.blit(tut_bg, (20, HEIGHT // 2 + 80))
            tut = self.font_small.render("← → Tap to Steer  |  Avoid traffic  |  Collect Coins!", True, WHITE)
            tut.set_alpha(alpha)
            screen.blit(tut, (WIDTH//2 - tut.get_width()//2, HEIGHT // 2 + 90))

    def draw_pause_screen(self, surface):
        from settings import WIDTH, HEIGHT, WHITE, GREEN, RED
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        title = self.font_title.render("PAUSED", True, WHITE)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3 - 50))

        btn_w, btn_h = 240, 60
        resume_rect = pygame.Rect(WIDTH//2 - btn_w//2, HEIGHT//2 - 20, btn_w, btn_h)
        quit_rect = pygame.Rect(WIDTH//2 - btn_w//2, HEIGHT//2 + 70, btn_w, btn_h)

        pygame.draw.rect(surface, GREEN, resume_rect, border_radius=10)
        pygame.draw.rect(surface, RED, quit_rect, border_radius=10)

        r_txt = self.font_medium.render("Resume", True, WHITE)
        q_txt = self.font_medium.render("Quit", True, WHITE)

        surface.blit(r_txt, (resume_rect.centerx - r_txt.get_width()//2, resume_rect.centery - r_txt.get_height()//2))
        surface.blit(q_txt, (quit_rect.centerx - q_txt.get_width()//2, quit_rect.centery - q_txt.get_height()//2))