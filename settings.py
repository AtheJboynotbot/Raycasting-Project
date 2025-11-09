import math
TILESIZE = 64  # Size for screen

ROWS = 10
COLS = 16

#Dimensions
WINDOW_WIDTH = COLS * TILESIZE
WINDOW_HEIGHT = ROWS * TILESIZE

#Field of View
FOV = 60 * (math.pi / 180)

RES = 12                # this will increase performance if tilesize is increased but makes textures choppier
NUM_RAYS = WINDOW_WIDTH // RES