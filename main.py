import pygame
import sys
from settings import *
from themap import Map
from theplayer import Player
from raycaster import Raycaster

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
map = Map()
player = Player(map)  # Pass map to player for collision detection
clock = pygame.time.Clock()
raycaster = Raycaster(player, map)
#supposed to be ceiling and floor
#background_image = pygame.image.load("texture/ceiling and floor/cobblestone.jpg").convert()


def start_menu():
    title_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 30)
    title_text = title_font.render("Raycasting by Demol, Esfandiary, Judaya, and Roldan", True, (255, 255, 255))
    start_button_text = button_font.render("Start", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    start_button_rect = start_button_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return  # Start the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))  # Black background
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, (50, 50, 50), start_button_rect.inflate(20, 10))  # Button background
        screen.blit(start_button_text, start_button_rect)
        pygame.display.update()


start_menu()

while True:
    #fps runs at 120
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
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
