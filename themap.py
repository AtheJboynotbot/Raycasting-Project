import pygame
from settings import *


class Map:
    def __init__(self):
        #vector array map
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1,],
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1,],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1,],
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1,],
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1,],
            [1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1,],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1,],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
        ]
    #wall checker
    def has_wall_at(self, x, y):
        # Convert to grid coordinates
        grid_x = int(x // TILESIZE)
        grid_y = int(y // TILESIZE)
        
        # Check if coordinates are within grid bounds
        if 0 <= grid_y < len(self.grid) and 0 <= grid_x < len(self.grid[0]):
            return self.grid[grid_y][grid_x] == 1
        return True  # Consider out of bounds as wall 
    def render(self, screen):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                #coordinates for pixels
                tile_x = j * TILESIZE #this is columns
                tile_y = i * TILESIZE #this is rows
                #coloring
                if self.grid[i][j] == 1: #this is for walls
                    tile_rect = pygame.Rect(tile_x, tile_y, TILESIZE - 1, TILESIZE - 1)
                    pygame.draw.rect(screen, (198, 162, 126), tile_rect)
                else: #this is for floors
                    tile_rect = pygame.Rect(tile_x, tile_y, TILESIZE - 1, TILESIZE - 1)
                    pygame.draw.rect(screen, (86, 90, 102), tile_rect)