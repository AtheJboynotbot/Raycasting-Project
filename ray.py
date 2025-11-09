import math
import pygame
from settings import *

def _normalize_angle(angle):
    angle %= 2 * math.pi
    if angle < 0:
        angle += 2 * math.pi
    return angle

def distance_between(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

class Ray:
    def __init__(self, ray_angle, player, map):
        self.player = player
        self.map = map
        self.ray_angle = _normalize_angle(ray_angle)
        self.distance = 0
        self.color = (198, 162, 126)
        self.is_facing_down = 0 < self.ray_angle < math.pi
        self.is_facing_up = not self.is_facing_down
        self.is_facing_right = (self.ray_angle < 0.5 * math.pi) or (self.ray_angle > 1.5 * math.pi)
        self.is_facing_left = not self.is_facing_right

        self.horizontal_hit_x = 0
        self.horizontal_hit_y = 0
        self.vertical_hit_x = 0
        self.vertical_hit_y = 0

        self.wall_hit_x = 0
        self.wall_hit_y = 0
        self.texture_x = 0
        self.was_hit_vertical = False

    def cast(self):
        # HORIZONTAL INTERSECTION CHECK
        found_horizontal = False
        hor_hit_x = hor_hit_y = 0

        # avoid tan = 0 (ray exactly horizontal)
        tan_angle = math.tan(self.ray_angle)
        if abs(tan_angle) > 1e-6:
            if self.is_facing_down:
                y_intercept = math.floor(self.player.y / TILESIZE) * TILESIZE + TILESIZE
                y_step = TILESIZE
            else:
                y_intercept = math.floor(self.player.y / TILESIZE) * TILESIZE - 1e-6
                y_step = -TILESIZE

            x_intercept = self.player.x + (y_intercept - self.player.y) / tan_angle
            x_step = y_step / tan_angle

            next_x = x_intercept
            next_y = y_intercept

            while 0 <= next_x < WINDOW_WIDTH and 0 <= next_y < WINDOW_HEIGHT:
                # when checking horizontal intersections, sample a tiny bit toward the ray direction:
                check_y = next_y + (1 if self.is_facing_down else -1)
                if self.map.has_wall_at(next_x, check_y):
                    found_horizontal = True
                    hor_hit_x = next_x
                    hor_hit_y = next_y
                    break
                next_x += x_step
                next_y += y_step

        # VERTICAL INTERSECTION CHECK
        found_vertical = False
        ver_hit_x = ver_hit_y = 0

        # avoid extremely large tan (ray exactly vertical) by using cotangent step
        if abs(1 / (math.tan(self.ray_angle) if abs(math.tan(self.ray_angle)) > 1e-6 else 1e6)) > 0:
            if self.is_facing_right:
                x_intercept = math.floor(self.player.x / TILESIZE) * TILESIZE + TILESIZE
                x_step = TILESIZE
            else:
                x_intercept = math.floor(self.player.x / TILESIZE) * TILESIZE - 1e-6
                x_step = -TILESIZE

            y_intercept = self.player.y + (x_intercept - self.player.x) * math.tan(self.ray_angle)
            y_step = x_step * math.tan(self.ray_angle)

            next_x = x_intercept
            next_y = y_intercept

            while 0 <= next_x < WINDOW_WIDTH and 0 <= next_y < WINDOW_HEIGHT:
                # sample a tiny bit toward the ray direction for vertical check
                check_x = next_x + ( -1 if self.is_facing_left else 1 )
                if self.map.has_wall_at(check_x, next_y):
                    found_vertical = True
                    ver_hit_x = next_x
                    ver_hit_y = next_y
                    break
                next_x += x_step
                next_y += y_step

        # Distances
        horiz_dist = distance_between(self.player.x, self.player.y, hor_hit_x, hor_hit_y) if found_horizontal else float('inf')
        vert_dist = distance_between(self.player.x, self.player.y, ver_hit_x, ver_hit_y) if found_vertical else float('inf')

        # choose closer hit
        if vert_dist < horiz_dist:
            self.wall_hit_x = ver_hit_x
            self.wall_hit_y = ver_hit_y
            raw_distance = vert_dist
            self.was_hit_vertical = True
            # texture X from Y coord for vertical wall
            self.texture_x = int(ver_hit_y) % TILESIZE
        else:
            self.wall_hit_x = hor_hit_x
            self.wall_hit_y = hor_hit_y
            raw_distance = horiz_dist
            self.was_hit_vertical = False
            # texture X from X coord for horizontal wall
            self.texture_x = int(hor_hit_x) % TILESIZE

        # Fish-eye correction and set final distance
        self.distance = raw_distance * math.cos(self.player.rotationAngle - self.ray_angle) if raw_distance != float('inf') else 0.0001

        # Lighting: scale base color by distance (keep some minimal brightness)
        brightness_factor = max(0.15, min(1.0, 60.0 / (self.distance if self.distance > 0 else 1)))
        r, g, b = self.color
        r = int(r * brightness_factor)
        g = int(g * brightness_factor)
        b = int(b * brightness_factor)
        self.color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

    def render(self, screen):
        pygame.draw.line(screen, (255, 0, 0), (self.player.x, self.player.y), (self.wall_hit_x, self.wall_hit_y))
