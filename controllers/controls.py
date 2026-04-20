import pygame

class InputHandler:
    @staticmethod
    def handle_player_input(event, player):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a): player.move_left(); return True
            if event.key in (pygame.K_RIGHT, pygame.K_d): player.move_right(); return True
        elif event.type == pygame.FINGERDOWN:
            if event.x < 0.5: player.move_left()
            else: player.move_right()
            return True
        return False

    @staticmethod
    def is_menu_advance_event(event):
        return event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN)

    @staticmethod
    def get_mode_selection(event, screen_width, screen_height):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: return 1
            if event.key == pygame.K_2: return 2
            if event.key == pygame.K_3: return 3
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            btn_w, btn_h = 240, 60
            y_cursors = [screen_height//2 - 60, screen_height//2 + 30, screen_height//2 + 120]
            
            for i in range(3):
                rect = pygame.Rect(screen_width//2 - btn_w//2, y_cursors[i], btn_w, btn_h)
                if rect.collidepoint(mouse_pos):
                    return i + 1
        return None

    @staticmethod
    def is_quit_to_menu(event):
        return event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE

    @staticmethod
    def get_pause_interaction(event, screen_width, screen_height):
        # Allow pressing ESC again to instantly resume
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "RESUME"
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            btn_w, btn_h = 240, 60
            resume_rect = pygame.Rect(screen_width//2 - btn_w//2, screen_height//2 - 20, btn_w, btn_h)
            quit_rect = pygame.Rect(screen_width//2 - btn_w//2, screen_height//2 + 70, btn_w, btn_h)
            
            if resume_rect.collidepoint(mouse_pos):
                return "RESUME"
            elif quit_rect.collidepoint(mouse_pos):
                return "QUIT"
        return None