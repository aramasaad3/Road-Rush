import pygame
from settings import *
from models.road import RoadSystem

class RoadRenderer:
    def __init__(self, road_system: RoadSystem):
        self.road = road_system
        self._tile  = self._make_tile()

    def _make_tile(self):
        surf = pygame.Surface((WIDTH, self.road.tile_h))
        surf.fill(ROAD_COLOR)

        pygame.draw.rect(surf, GRASS_LEFT,  (0, 0, RoadSystem.GRASS_W, self.road.tile_h))
        pygame.draw.rect(surf, GRASS_RIGHT, (RoadSystem.ROAD_RIGHT, 0, RoadSystem.GRASS_W, self.road.tile_h))

        pygame.draw.rect(surf, WHITE, (RoadSystem.GRASS_W - 2, 0, 4, self.road.tile_h))
        pygame.draw.rect(surf, WHITE, (RoadSystem.ROAD_RIGHT - 2, 0, 4, self.road.tile_h))

        dash_step = DASH_HEIGHT + DASH_GAP
        for lane in range(1, RoadSystem.LANE_COUNT):
            lx = RoadSystem.ROAD_LEFT + lane * RoadSystem.LANE_WIDTH - DASH_WIDTH // 2
            for dy in range(0, self.road.tile_h + dash_step, dash_step):
                pygame.draw.rect(surf, LANE_LINE, (lx, dy, DASH_WIDTH, DASH_HEIGHT))
        return surf

    def draw(self, screen):
        offset = int(self.road.scroll)
        screen.blit(self._tile, (0, offset - self.road.tile_h))
        screen.blit(self._tile, (0, offset))