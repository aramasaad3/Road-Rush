import pygame

class DifficultySettings:
    MODE_EASY = 1
    MODE_HARD = 2
    MODE_ENDLESS = 3

class ProgressionSystem:
    SPEED_INCREASE_INTERVAL = 10000 

    def __init__(self, mode):
        self.mode = mode
        if mode == DifficultySettings.MODE_EASY:
            self.INITIAL_SPEED = 2.5
            self.MAX_SPEED = 7.0
            self.SPEED_INCREASE_AMOUNT = 0.5
        else: # Hard or Endless are much faster and steeper
            self.INITIAL_SPEED = 3.5
            self.MAX_SPEED = 16.5
            self.SPEED_INCREASE_AMOUNT = 0.8

        self.speed = self.INITIAL_SPEED
        self.last_increase_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_increase_time > self.SPEED_INCREASE_INTERVAL:
            self.speed = min(self.speed + self.SPEED_INCREASE_AMOUNT, self.MAX_SPEED)
            self.last_increase_time = current_time
