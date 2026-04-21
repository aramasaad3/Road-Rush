import random
from settings import CAR_H
from models.entities import YellowCar, RedCar, Blocker, Coin
from models.road import RoadSystem

class Spawner:
    OBSTACLE_SPAWN_INIT_MS = 1600
    OBSTACLE_SPAWN_MIN_MS  = 500
    COIN_SPAWN_MS          = 2200

    def __init__(self, player, all_sprites, enemies, blockers, coins_group, mode=1):
        self.player      = player
        self.all_sprites = all_sprites
        self.enemies     = enemies
        self.blockers    = blockers
        self.coins_group = coins_group
        self.mode = mode
        
        if self.mode == 1:
            self.red_car_chance = 0.15
        else:
            self.red_car_chance = 0.35
        self.player = player
        self.all_sprites = all_sprites
        self.enemies = enemies
        self.blockers = blockers
        self.coins_group = coins_group

    def spawn_obstacle(self):
        occupied = {s.lane_index for s in self.enemies} | {s.lane_index for s in self.blockers}
        free_lanes = [l for l in range(RoadSystem.LANE_COUNT) if l not in occupied]
        
        if not free_lanes:
            return
            
        lane = random.choice(free_lanes)
        r    = random.random()
        if self.mode == 2:
            blocker_thresh = 0.10
            yellow_thresh  = 0.85  # Increased Yellow to 75% (was 65%)
        elif self.mode == 3:
            blocker_thresh = 0.15
            yellow_thresh  = 0.85  # Increased Yellow to 70% (was 45%)
        else:
            blocker_thresh = 0.20
            yellow_thresh  = 0.70
            
        if r < blocker_thresh:
            obj = Blocker(lane, -CAR_H)
            self.blockers.add(obj)
        elif r < yellow_thresh:
            obj = YellowCar(lane, -CAR_H)
            self.enemies.add(obj)
        else:
            obj = RedCar(-CAR_H, self.player, self.mode)
            self.enemies.add(obj)
        self.all_sprites.add(obj)

    def spawn_coins(self):
        occupied = {s.lane_index for s in self.enemies} | {s.lane_index for s in self.blockers}
        free_lanes = [l for l in range(RoadSystem.LANE_COUNT) if l not in occupied]
        
        if not free_lanes:
            return
            
        lane = random.choice(free_lanes)
        count = random.randint(1, 4)
        for i in range(count):
            c = Coin(lane, -40 - i * 40)
            self.coins_group.add(c)
            self.all_sprites.add(c)