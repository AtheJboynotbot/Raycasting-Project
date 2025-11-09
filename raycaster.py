import math
import pygame
from settings import *
from ray import Ray


class Raycaster:
    def __init__(self, player, themap, wall_texture, floor_texture, ceiling_texture):
        self.rays = []
        self.player = player
        self.themap = themap
        self.wall_texture = wall_texture.convert()
        self.floor_texture = floor_texture.convert()
        self.ceiling_texture = ceiling_texture.convert()
        self.tex_w, self.tex_h = self.wall_texture.get_size()
        self.floor_w, self.floor_h = self.floor_texture.get_size()
        self.ceil_w, self.ceil_h = self.ceiling_texture.get_size()

        # distance from player to projection plane (used for correct perspective)
        self.dist_proj_plane = (WINDOW_WIDTH / 2) / math.tan(FOV / 2)
        self.camera_height = TILESIZE / 2.0  # eye height above floor (tweak if needed)


    def castAllRays(self):
        self.rays = []
        ray_angle = self.player.rotationAngle - FOV / 2
        for _ in range(NUM_RAYS):
            ray = Ray(ray_angle, self.player, self.themap)
            ray.cast()
            self.rays.append(ray)
            ray_angle += FOV / NUM_RAYS
    
    def render(self, screen):
        counter = 0
        center_y = WINDOW_HEIGHT // 2

        # vertical sampling step for floor/ceiling (larger -> faster, blurrier)
        floor_step = 4  # try 2..8, increase if still slow

        for ray in self.rays:
            if ray.distance <= 0:
                counter += 1
                continue

            # compute correct projected wall height
            line_height = (TILESIZE / ray.distance) * self.dist_proj_plane
            draw_begin = int(center_y - (line_height / 2))
            draw_height = int(line_height)

            # compute texture X in texture pixels (same as before)
            tex_x = int((ray.texture_x / TILESIZE) * self.tex_w) % self.tex_w
            slice_rect = pygame.Rect(tex_x, 0, 1, self.tex_h)
            column = self.wall_texture.subsurface(slice_rect)
            column = pygame.transform.scale(column, (RES, max(1, draw_height)))
            screen_x = counter * RES

            # draw wall column
            screen.blit(column, (screen_x, draw_begin))

            # simple darkening for wall based on distance (optional)
            dark_alpha = min(200, int((ray.distance / 300) * 255))
            if dark_alpha > 0:
                dark_surf = pygame.Surface((RES, draw_height)).convert_alpha()
                dark_surf.fill((0, 0, 0, dark_alpha))
                screen.blit(dark_surf, (screen_x, draw_begin))

            # FLOOR & CEILING CASTING (stepped / block sampling)
            ray_dir_x = math.cos(ray.ray_angle)
            ray_dir_y = math.sin(ray.ray_angle)

            start_y = draw_begin + draw_height
            if start_y < center_y:
                start_y = center_y

            # sample every 'floor_step' pixels and draw a filled rect of that height
            y = start_y
            while y < WINDOW_HEIGHT:
                p = y - center_y
                if p == 0:
                    y += floor_step
                    continue
                current_dist = (self.camera_height * self.dist_proj_plane) / p

                world_x = self.player.x + current_dist * ray_dir_x
                world_y = self.player.y + current_dist * ray_dir_y

                tx = int(world_x) % self.floor_w
                ty = int(world_y) % self.floor_h

                # single sample per block (faster than per-pixel get_at)
                floor_color = self.floor_texture.get_at((tx, ty))

                block_h = min(floor_step, WINDOW_HEIGHT - y)
                screen.fill(floor_color, rect=pygame.Rect(screen_x, y, RES, block_h))

                # ceiling symmetric
                ceil_y = WINDOW_HEIGHT - (y + block_h - 1)
                if 0 <= ceil_y < WINDOW_HEIGHT:
                    cx = int(world_x) % self.ceil_w
                    cy = int(world_y) % self.ceil_h
                    ceil_color = self.ceiling_texture.get_at((cx, cy))
                    screen.fill(ceil_color, rect=pygame.Rect(screen_x, ceil_y - block_h + 1, RES, block_h))

                y += floor_step

            counter += 1
