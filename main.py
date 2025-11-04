import pygame
import sys
from settings import *
from themap import Map
from theplayer import Player
from raycaster import Raycaster

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
map = Map()
player = Player(map)  # Pass map to player for collision detection
clock = pygame.time.Clock()
raycaster = Raycaster(player, map)
#supposed to be ceiling and floor
#background_image = pygame.image.load("texture/ceiling and floor/cobblestone.jpg").convert()
while True:
    #fps runs at 120
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    screen.fill((86, 90, 102))
    #this is supposed to be ceiling and floor
    # screen.blit(background_image, (0, 0))
    #map.render(screen)
    raycaster.castAllRays()
    raycaster.render(screen)
    player.update()
    #player.render(screen)
    pygame.display.update()
