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

        # Pre-compute pixel arrays for faster texture access
        # Fallback implementation without NumPy (slower than surfarray but faster than repeated get_at)
        self.floor_array = self._create_pixel_array(self.floor_texture, self.floor_w, self.floor_h)
        self.ceiling_array = self._create_pixel_array(self.ceiling_texture, self.ceil_w, self.ceil_h)

        # distance from player to projection plane 
        self.dist_proj_plane = (WINDOW_WIDTH / 2) / math.tan(FOV / 2)
        self.camera_height = TILESIZE / 2.0  
        
        #this will control the size of floor and ceiling
        #the higher the value for these means tiles will be more but more stretched vise versa
        self.floor_texture_scale = 0.3  
        self.ceiling_texture_scale = 0.3
        
        # Cache for ray direction vectors (cos, sin pairs) - recomputed each frame
        self.ray_dirs = []

    def _create_pixel_array(self, surface, width, height):
        """Create a 2D list of pixel colors for fast access (NumPy-free alternative)"""
        pixel_array = []
        for x in range(width):
            column = []
            for y in range(height):
                column.append(surface.get_at((x, y))[:3]) 
            pixel_array.append(column)
        return pixel_array

    def castAllRays(self):
        self.rays = []
        self.ray_dirs = []  #this will clear and rebuild direction cache
        ray_angle = self.player.rotationAngle - FOV / 2
        for _ in range(NUM_RAYS):
            ray = Ray(ray_angle, self.player, self.themap)
            ray.cast()
            self.rays.append(ray)
            # Pre-compute direction vectors (affine transformation coefficients)
            # This avoids redundant cos/sin calls in the render loop
            self.ray_dirs.append((math.cos(ray_angle), math.sin(ray_angle)))
            ray_angle += FOV / NUM_RAYS
    
    def render(self, screen):
        counter = 0
        center_y = WINDOW_HEIGHT // 2
        #this will increase speed but lowers resolution when given a higher value
        floor_step = 6

        for idx, ray in enumerate(self.rays):
            if ray.distance <= 0:
                counter += 1
                continue

            # compute correct projected wall height
            line_height = (TILESIZE / ray.distance) * self.dist_proj_plane
            draw_begin = int(center_y - (line_height / 2))
            draw_height = int(line_height)

            # compute texture X in texture pixels like before
            tex_x = int((ray.texture_x / TILESIZE) * self.tex_w) % self.tex_w
            slice_rect = pygame.Rect(tex_x, 0, 1, self.tex_h)
            column = self.wall_texture.subsurface(slice_rect)
            column = pygame.transform.scale(column, (RES, max(1, draw_height)))
            screen_x = counter * RES

            # draw wall column
            screen.blit(column, (screen_x, draw_begin))

            # simple darkening for wall based on distance
            dark_alpha = min(200, int((ray.distance / 300) * 255))
            if dark_alpha > 0:
                dark_surf = pygame.Surface((RES, draw_height)).convert_alpha()
                dark_surf.fill((0, 0, 0, dark_alpha))
                screen.blit(dark_surf, (screen_x, draw_begin))

            ray_dir_x, ray_dir_y = self.ray_dirs[idx]

            start_y = draw_begin + draw_height
            if start_y < center_y:
                start_y = center_y

            #sample every floor_step pixels and draw a filled rect of that height
            y = start_y
            while y < WINDOW_HEIGHT:
                p = y - center_y
                if p == 0:
                    y += floor_step
                    continue
                current_dist = (self.camera_height * self.dist_proj_plane) / p

                world_x = self.player.x + current_dist * ray_dir_x
                world_y = self.player.y + current_dist * ray_dir_y


                tx = int(world_x / self.floor_texture_scale) % self.floor_w
                ty = int(world_y / self.floor_texture_scale) % self.floor_h

                # Array access (list lookup - slower than NumPy but faster than get_at)
                floor_color = self.floor_array[tx][ty]

                block_h = min(floor_step, WINDOW_HEIGHT - y)
                screen.fill(floor_color, rect=pygame.Rect(screen_x, y, RES, block_h))

                # ceiling symmetric 
                ceil_y = WINDOW_HEIGHT - (y + block_h - 1)
                if 0 <= ceil_y < WINDOW_HEIGHT:
                    cx = int(world_x / self.ceiling_texture_scale) % self.ceil_w
                    cy = int(world_y / self.ceiling_texture_scale) % self.ceil_h
                    ceil_color = self.ceiling_array[cx][cy]
                    screen.fill(ceil_color, rect=pygame.Rect(screen_x, ceil_y - block_h + 1, RES, block_h))

                y += floor_step

            counter += 1
