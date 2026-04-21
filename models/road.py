from settings import WIDTH, HEIGHT

class RoadSystem:
    GRASS_W    = 50
    ROAD_W     = WIDTH - 2 * GRASS_W
    LANE_COUNT = 4
    LANE_WIDTH = ROAD_W // LANE_COUNT
    ROAD_LEFT  = GRASS_W
    ROAD_RIGHT = WIDTH - GRASS_W
    
    LANES = [
        ROAD_LEFT + LANE_WIDTH * 0 + LANE_WIDTH // 2,
        ROAD_LEFT + LANE_WIDTH * 1 + LANE_WIDTH // 2,
        ROAD_LEFT + LANE_WIDTH * 2 + LANE_WIDTH // 2,
        ROAD_LEFT + LANE_WIDTH * 3 + LANE_WIDTH // 2,
    ]
    
    def __init__(self):
        self.scroll = 0.0
        self.tile_h = HEIGHT
        
    def update(self, speed):
        self.scroll += speed
        if self.scroll >= self.tile_h:
            self.scroll -= self.tile_h

    @classmethod
    def get_lane_x(cls, lane_index):
        if 0 <= lane_index < cls.LANE_COUNT:
            return cls.LANES[lane_index]
        return cls.LANES[0]