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
from models.entities import Player, YellowCar, RedCar, Blocker, Coin, HeartPickup
from models.resources import HealthSystem, ScoreSystem, RecordSystem
from views.sound import SoundManager
from views.graphics import RoadRenderer
from controllers.collision import CollisionSystem
from models.road import RoadSystem
from models.difficulty import ProgressionSystem
from controllers.traffic import Spawner
from controllers.controls import InputHandler
from views.hud import HUD, load_font
from views.feedback import FeedbackScreens

class Game:

    STATE_START    = "START"
    STATE_PLAYING  = "PLAYING"
    STATE_GAMEOVER = "GAMEOVER"
    STATE_VICTORY  = "VICTORY"
    STATE_PAUSED   = "PAUSED"

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock  = pygame.time.Clock()
        self.running = True

        self.font_title  = load_font(64)
        self.font_big    = load_font(46)
        self.font_medium = load_font(28)
        self.font_small  = load_font(20)
        self.hud = HUD(self.font_small)
        self.feedback = FeedbackScreens(self.font_title, self.font_big, self.font_medium, self.font_small)

        self.EV_SPAWN_OBSTACLE = pygame.USEREVENT + 1
        self.EV_SPAWN_COIN     = pygame.USEREVENT + 2

        self.sfx = SoundManager()
        import os, sys
        def r_path(p):
            return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), p)
        self.r_path_func = r_path

        self.sfx.load("crash", r_path("assets/sounds/crash.wav"))
        self.sfx.load("coin",  r_path("assets/sounds/coin.wav"))
        self.sfx.load("star",  r_path("assets/sounds/star.wav"))
        self.sfx.load("win",   r_path("assets/sounds/win.wav"))
        self.sfx.load("lose",  r_path("assets/sounds/lose.wav"))
        self.sfx.play_music(r_path("assets/sounds/spinopel-speed-race-344521.mp3"))
        
        self.collision_system = CollisionSystem(self.sfx)

        self.road_system = RoadSystem()
        self.road = RoadRenderer(self.road_system)

        self.state = self.STATE_START

        self.record = RecordSystem()

        self.player = Player()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.enemies     = pygame.sprite.Group()
        self.blockers    = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()
        self.progression = ProgressionSystem(1)
        self.health_system = HealthSystem()
        self.score_system = ScoreSystem(1)
        self.tutorial_timer = 180

    def new_game(self, mode):
        self.current_mode = mode
        self.progression = ProgressionSystem(mode)

        self.all_sprites = pygame.sprite.Group()
        self.enemies     = pygame.sprite.Group()
        self.blockers    = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.health_system = HealthSystem()
        self.score_system = ScoreSystem(mode)
        self.tutorial_timer = 180
        self.boost_timer = 0
        self.boost_speed_bonus = 3.0
        self.spawner = Spawner(self.player, self.all_sprites, self.enemies, self.blockers, self.coins_group, mode)
        self.hearts_group = pygame.sprite.Group()
        self.next_heart_distance = 500

        pygame.time.set_timer(self.EV_SPAWN_OBSTACLE, Spawner.OBSTACLE_SPAWN_INIT_MS)
        pygame.time.set_timer(self.EV_SPAWN_COIN,     Spawner.COIN_SPAWN_MS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if InputHandler.is_quit_to_menu(event):
                if self.state == self.STATE_PLAYING:
                    pygame.mixer.music.pause()
                    self.state = self.STATE_PAUSED

            elif self.state == self.STATE_START:
                mode = InputHandler.get_mode_selection(event, WIDTH, HEIGHT)
                if mode is not None:
                    self.state = self.STATE_PLAYING
                    if getattr(self, 'r_path_func', None):
                        self.sfx.play_music(self.r_path_func("assets/sounds/lnplusmusic-racing-speed-driving-music-416549.mp3"))
                    self.new_game(mode)

            elif self.state == self.STATE_PAUSED:
                action = InputHandler.get_pause_interaction(event, WIDTH, HEIGHT)
                if action == "RESUME":
                    pygame.mixer.music.unpause()
                    self.state = self.STATE_PLAYING
                elif action == "QUIT":
                    self.state = self.STATE_START
                    if getattr(self, 'r_path_func', None):
                        self.sfx.play_music(self.r_path_func("assets/sounds/spinopel-speed-race-344521.mp3"))

            elif self.state in (self.STATE_GAMEOVER, self.STATE_VICTORY):
                if InputHandler.is_menu_advance_event(event):
                    self.state = self.STATE_START
                    if getattr(self, 'r_path_func', None):
                        self.sfx.play_music(self.r_path_func("assets/sounds/spinopel-speed-race-344521.mp3"))

            if self.state == self.STATE_PLAYING:
                if event.type == self.EV_SPAWN_OBSTACLE:
                    self.spawner.spawn_obstacle()

                    interval = max(
                        Spawner.OBSTACLE_SPAWN_MIN_MS,
                        int(Spawner.OBSTACLE_SPAWN_INIT_MS - (self.progression.speed - self.progression.INITIAL_SPEED) * 150)
                    )
                    pygame.time.set_timer(self.EV_SPAWN_OBSTACLE, interval)

                elif event.type == self.EV_SPAWN_COIN:
                    self.spawner.spawn_coins()

                else:
                    InputHandler.handle_player_input(event, self.player)

    def update(self):
        if self.state != self.STATE_PLAYING:
            return

        self.progression.update()
        
        if self.boost_timer > 0:
            self.boost_timer -= 1
            effective_speed = self.progression.speed + self.boost_speed_bonus

            self.player.inv_frames = max(self.player.inv_frames, 2)
            if self.boost_timer == 0:

                self.player.inv_frames = 0
        else:
            effective_speed = self.progression.speed
        
        self.score_system.add_distance(effective_speed)

        if self.tutorial_timer > 0:
            self.tutorial_timer -= 1

        self.road_system.update(effective_speed)

        self.player.update()
        self.enemies.update(effective_speed)
        self.blockers.update(effective_speed)
        self.coins_group.update(effective_speed)
        self.hearts_group.update(effective_speed)

        if self.score_system.mode == 3 and self.score_system.distance >= self.next_heart_distance:
            self.next_heart_distance += 500
            import random
            occupied = {s.lane_index for s in self.enemies} | {s.lane_index for s in self.blockers}
            free_lanes = [l for l in range(RoadSystem.LANE_COUNT) if l not in occupied]
            if free_lanes:
                lane = random.choice(free_lanes)
                h = HeartPickup(lane, -40)
                self.hearts_group.add(h)
                self.all_sprites.add(h)

        collected_hearts = pygame.sprite.spritecollide(self.player, self.hearts_group, True)
        for _ in collected_hearts:
            if self.health_system.current < self.health_system.MAX_HEALTH:
                self.health_system.current += 1
            self.sfx.play("star")

        new_state = self.collision_system.process_interactions(
            self.player, self.enemies, self.blockers, self.coins_group, 
            self.health_system, self.score_system
        )
        
        if self.score_system.just_earned_star:
            self.score_system.just_earned_star = False
            self.boost_timer = 600 if self.score_system.mode == 3 else 300

            for enemy in list(self.enemies):
                enemy.kill()
            for blocker in list(self.blockers):
                blocker.kill()
            self.sfx.play("star")
        
        if new_state == "GAMEOVER":
            self.state = self.STATE_GAMEOVER

            if self.score_system.mode == 3:
                self.is_new_record = self.record.check_and_update(self.score_system.distance)
            else:
                self.is_new_record = False
            self.sfx.play("lose")
            self.sfx.stop_music()
            pygame.time.set_timer(self.EV_SPAWN_OBSTACLE, 0)
            pygame.time.set_timer(self.EV_SPAWN_COIN,     0)
        elif new_state == "VICTORY":
            self.state = self.STATE_VICTORY
            self.sfx.play("win")
            self.sfx.stop_music()
            pygame.time.set_timer(self.EV_SPAWN_OBSTACLE, 0)
            pygame.time.set_timer(self.EV_SPAWN_COIN,     0)

    def draw(self):
        if self.state == self.STATE_START:
            self.feedback.draw_start_screen(self.screen, self.road)
            
        elif self.state == self.STATE_PLAYING:
            self.road.draw(self.screen)
            if self.health_system.current == 1:
                vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                vignette.fill((180, 0, 0, 40))
                self.screen.blit(vignette, (0, 0))
            self.all_sprites.draw(self.screen)
            self.hud.draw(self.screen, self.health_system, self.score_system, self.progression, self.record, getattr(self, 'boost_timer', 0))
            self.feedback.draw_tutorial(self.screen, self.tutorial_timer)

        elif self.state == self.STATE_PAUSED:
            self.road.draw(self.screen)
            if self.health_system.current == 1:
                vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                vignette.fill((180, 0, 0, 40))
                self.screen.blit(vignette, (0, 0))
            self.all_sprites.draw(self.screen)
            self.hud.draw(self.screen, self.health_system, self.score_system, self.progression)
            
            self.feedback.draw_pause_screen(self.screen)

        elif self.state == self.STATE_GAMEOVER:
            self.feedback.draw_gameover_screen(self.screen, self.score_system, self.record, getattr(self, 'is_new_record', False))

        elif self.state == self.STATE_VICTORY:
            self.feedback.draw_victory_screen(self.screen, self.score_system)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()