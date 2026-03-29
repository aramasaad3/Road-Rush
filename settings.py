import pygame

# ─── Screen ───────────────────────────────────────────────────────────────────
WIDTH  = 480
HEIGHT = 800
FPS    = 60
TITLE  = "Road Rush"

# ─── Colors ───────────────────────────────────────────────────────────────────
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0  )
RED        = (220, 50,  50 )
DARK_RED   = (120, 0,   0  )
BLUE       = (50,  120, 230)
BLUE_LIGHT = (100, 170, 255)
YELLOW     = (255, 220, 30 )
YELLOW_DK  = (200, 160, 0  )
GRAY       = (130, 130, 140)
DARK_GRAY  = (40,  42,  54 )
ROAD_COLOR = (55,  57,  68 )
GRASS_LEFT = (40,  80,  40 )
GRASS_RIGHT= (40,  80,  40 )
LANE_LINE  = (220, 220, 220)
GOLD       = (255, 200, 30 )
ORANGE     = (255, 140, 0  )
GREEN      = (80,  220, 100)
SHADOW     = (0,   0,   0,  90)  # RGBA for a semi-transparent shadow

# ─── Layout ───────────────────────────────────────────────────────────────────
GRASS_W    = 50          # width of each grass strip on the sides
ROAD_W     = WIDTH - 2 * GRASS_W   # 380 px
LANE_COUNT = 4
LANE_WIDTH = ROAD_W // LANE_COUNT  # ~95 px
ROAD_LEFT  = GRASS_W
ROAD_RIGHT = WIDTH - GRASS_W

# Lane centre x-positions (inside the road area)
LANES = [
    ROAD_LEFT + LANE_WIDTH * i + LANE_WIDTH // 2
    for i in range(LANE_COUNT)
]

# ─── Entity sizes ─────────────────────────────────────────────────────────────
CAR_W   = 54
CAR_H   = 90
COIN_R  = 12

# ─── Speed / spawning ─────────────────────────────────────────────────────────
INITIAL_SPEED          = 5.0
SPEED_INCREMENT        = 0.4
SPEED_INCREASE_MS      = 10_000   # every 10 s
MAX_SPEED              = 18.0

OBSTACLE_SPAWN_INIT_MS = 1600
OBSTACLE_SPAWN_MIN_MS  = 500
COIN_SPAWN_MS          = 2200

# ─── Game rules ───────────────────────────────────────────────────────────────
MAX_HEALTH             = 3
COINS_PER_STAR         = 10
STARS_TO_WIN           = 3
INVINCIBILITY_FRAMES   = 90       # frames of invincibility after a hit
RED_CAR_TRACK_FRAMES   = 50       # frames between Red Car lane adjustments

# ─── Lane markings ────────────────────────────────────────────────────────────
DASH_HEIGHT = 30
DASH_GAP    = 30
DASH_WIDTH  = 6
