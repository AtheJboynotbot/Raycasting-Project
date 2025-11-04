import math
import pygame
from settings import *
from themap import *

def _normalize_angle(angle):
        angle %= 2 * math.pi
        if angle < 0:
            angle += 2 * math.pi
        return angle
def distance_between(x1, y1, x2, y2):
    #distance between two points
    return math.sqrt((x2 - x1) *(x2 - x1) + (y2 - y1) *(y2 - y1))
class Ray:
    def __init__(self, ray_angle, player, map):
        self.player = player
        self.map = map
        self.ray_angle = _normalize_angle(ray_angle)
        self.distance = 1
        self.color = 255
        self.is_facing_down = self.ray_angle > 0 and self.ray_angle < math.pi
        self.is_facing_up = not self.is_facing_down
        self.is_facing_right = self.ray_angle < 0.5 * math.pi or self.ray_angle > 1.5 * math.pi
        self.is_facing_left = not self.is_facing_right
        self.horizontal_hit_x = 0
        self.horizontal_hit_y = 0
        self.distance = 0
        self.color = (198, 162, 126)

    def cast(self):
        #HORIZONTAL WALL CHECK
        found_horizontal_wall = False
        horizontal_hit_x = 0
        horizontal_hit_y = 0

        first_intersection_x = None
        first_intersection_y = None

        # Only check horizontal walls if not looking exactly left/right
        tan_angle = math.tan(self.ray_angle)
        if abs(tan_angle) > 0.0001:  # Not exactly horizontal
            if self.is_facing_up:
                first_intersection_y = ((self.player.y // TILESIZE)) * TILESIZE - 0.001
            elif self.is_facing_down:
                first_intersection_y = ((self.player.y // TILESIZE) * TILESIZE) + TILESIZE

            first_intersection_x = self.player.x + (first_intersection_y - self.player.y) / tan_angle
            next_horizontal_x = first_intersection_x
            next_horizontal_y = first_intersection_y

            if self.is_facing_up:
                ya = -TILESIZE
            elif self.is_facing_down:
                ya = TILESIZE
            xa = ya / tan_angle

            while (next_horizontal_x <= WINDOW_WIDTH and next_horizontal_x >= 0 and next_horizontal_y <= WINDOW_HEIGHT and next_horizontal_y >= 0):
                if self.map.has_wall_at(next_horizontal_x, next_horizontal_y):
                    found_horizontal_wall = True
                    horizontal_hit_x = next_horizontal_x
                    horizontal_hit_y = next_horizontal_y
                    break
                else:
                    next_horizontal_x += xa
                    next_horizontal_y += ya
        
        #VERTICAL WALL CHECK
        found_vertical_wall = False
        vertical_hit_x = 0
        vertical_hit_y = 0
        # Only check vertical walls if not looking exactly up/down
        tan_angle = math.tan(self.ray_angle)
        if abs(tan_angle) < 10000:  # Not exactly vertical
            if self.is_facing_right:
                first_intersection_x = ((self.player.x // TILESIZE) * TILESIZE) + TILESIZE 
            elif self.is_facing_left:
                first_intersection_x = (self.player.x // TILESIZE) * TILESIZE -0.001

            first_intersection_y = self.player.y + (first_intersection_x - self.player.x) * tan_angle
            next_vertical_x = first_intersection_x
            next_vertical_y = first_intersection_y

            if self.is_facing_right:
                xa = TILESIZE
            elif self.is_facing_left:
                xa = -TILESIZE
            ya = xa * tan_angle

            while (next_vertical_x <= WINDOW_WIDTH and next_vertical_x >= 0 and next_vertical_y <= WINDOW_HEIGHT and next_vertical_y >= 0):
                if self.map.has_wall_at(next_vertical_x, next_vertical_y):
                    found_vertical_wall = True
                    vertical_hit_x = next_vertical_x
                    vertical_hit_y = next_vertical_y
                    break
                else:
                    next_vertical_x += xa
                    next_vertical_y += ya

        #distance calculation
        horizontal_distance = 0
        vertical_distance = 0

        if found_horizontal_wall:
            horizontal_distance = distance_between(self.player.x, self.player.y, horizontal_hit_x, horizontal_hit_y)
        else:
            horizontal_distance = 999999

        if found_vertical_wall:
            vertical_distance = distance_between(self.player.x, self.player.y, vertical_hit_x, vertical_hit_y)
        else:
            vertical_distance = 999999

        if horizontal_distance < vertical_distance:
            self.wall_hit_x = horizontal_hit_x
            self.wall_hit_y = horizontal_hit_y
            self.distance = horizontal_distance
            self.color = (128, 105, 82)
        else:
            self.wall_hit_x = vertical_hit_x
            self.wall_hit_y = vertical_hit_y     
            self.distance = vertical_distance
            self.color = (198, 162, 126)
        self.distance *= math.cos(self.player.rotationAngle - self.ray_angle)
        
        # Lighting Effect the farther the darker
        brightness_factor = 60 / self.distance
        r, g, b = self.color
        r = int(r * brightness_factor)
        g = int(g * brightness_factor)
        b = int(b * brightness_factor)
        
        # Clamp values to 0-255 range
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        self.color = (r, g, b)


    def render(self, screen):
        pygame.draw.line(screen, (255, 0, 0), (self.player.x, self.player.y), (self.wall_hit_x, self.wall_hit_y))
