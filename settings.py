import math
TILESIZE = 64

ROWS = 10
COLS = 16

#Dimensions
WINDOW_WIDTH = COLS * TILESIZE
WINDOW_HEIGHT = ROWS * TILESIZE

#Field of View
FOV = 60 * (math.pi / 180)

RES = 3                # changed from 1 -> draw every 3 pixels horizontally (big speed win)
NUM_RAYS = WINDOW_WIDTH // RES