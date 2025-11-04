import pygame
import math
from settings import *

class Player:
    def __init__(self, map=None):
        #making sure player is in the middle of the map->
        self.x = (COLS * TILESIZE) / 2 + TILESIZE / 2
        self.y = (ROWS * TILESIZE) / 2 + TILESIZE / 2
        #<-
        self.radius = 3
        self.turnDirection = 0
        self.moveDirection = 0
        self.rotationAngle = 0
        self.moveSpeed = 2.5
        self.rotationSpeed = 2 * (math.pi / 180)
        self.map = map  # Store reference to map for collision detection
    
    #function for movement and looking
    def update(self):

        keys = pygame.key.get_pressed()

        self.turnDirection = 0
        self.moveDirection = 0

        if keys[pygame.K_d]:
            self.turnDirection = 1
        if keys[pygame.K_a]:
            self.turnDirection = -1
        if keys[pygame.K_w]:
            self.moveDirection = 1
        if keys[pygame.K_s]:
            self.moveDirection = -1
        if keys[pygame.K_RIGHT]:
            self.turnDirection = 1
        if keys[pygame.K_LEFT]:
            self.turnDirection = -1
        if keys[pygame.K_UP]:
            self.moveDirection = 1
        if keys[pygame.K_DOWN]:
            self.moveDirection = -1

        self.rotationAngle += self.turnDirection * self.rotationSpeed

        # Calculate new position
        moveStep = self.moveDirection * self.moveSpeed
        new_x = self.x + math.cos(self.rotationAngle) * moveStep
        new_y = self.y + math.sin(self.rotationAngle) * moveStep
        
        # Collision detection - only move if map exists and new position is not a wall
        if self.map:
            # Check multiple points around the player for smoother collision
            collision_buffer = 5  # Small buffer around player
            if not self.map.has_wall_at(new_x + collision_buffer, new_y) and \
               not self.map.has_wall_at(new_x - collision_buffer, new_y) and \
               not self.map.has_wall_at(new_x, new_y + collision_buffer) and \
               not self.map.has_wall_at(new_x, new_y - collision_buffer):
                self.x = new_x
                self.y = new_y
        else:
            # No collision detection if map not provided
            self.x = new_x
            self.y = new_y

        if self.rotationAngle < 0:
            self.rotationAngle += 2 * math.pi
        if self.rotationAngle > 2 * math.pi:
            self.rotationAngle -= 2 * math.pi
    
    def render(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)

        pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x + math.cos(self.rotationAngle) * 50, self.y + math.sin(self.rotationAngle) * 50))