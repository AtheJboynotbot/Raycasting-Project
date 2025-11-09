import math
TILESIZE = 64

ROWS = 10
COLS = 16

#Dimensions
WINDOW_WIDTH = COLS * TILESIZE
WINDOW_HEIGHT = ROWS * TILESIZE

#Field of View
FOV = 60 * (math.pi / 180)

RES = 1

NUM_RAYS = WINDOW_WIDTH // RES