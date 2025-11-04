import pygame
from settings import *
from ray import Ray


class Raycaster:
    def __init__(self, player, themap):
        self.rays = []
        self.player = player
        self.themap = themap


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
        for ray in self.rays:
            #ray.render(screen)
            line_height = (32 / ray.distance) * 415
            draw_begin = (WINDOW_HEIGHT / 2) - (line_height / 2)
            draw_end = line_height
            pygame.draw.rect(screen, (ray.color), (counter * RES, draw_begin, RES, draw_end))
            counter += 1
