import pygame
import sys
import os
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

# load textures (place your PNG/JPG in a "textures" folder next to main.py)
base_dir = os.path.dirname(__file__)
wall_tex = pygame.image.load(os.path.join(base_dir, "textures", "wall.png")).convert()
ceiling_tex = pygame.image.load(os.path.join(base_dir, "textures", "ceiling.png")).convert()
floor_tex = pygame.image.load(os.path.join(base_dir, "textures", "floor.png")).convert()

raycaster = Raycaster(player, map, wall_tex, floor_tex, ceiling_tex)  # pass floor & ceiling textures too


def start_menu():
    title_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 30)
    title_text = title_font.render("Raycasting by Esfandiary, Hisu-an, Judaya, and Perez", True, (255, 255, 255))
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


def pause_menu():
    paused = True
    title_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 30)
    paused_text = title_font.render("Paused", True, (255, 255, 255))
    resume_button_text = button_font.render("Resume", True, (255, 255, 255))
    quit_button_text = button_font.render("Quit", True, (255, 255, 255))

    paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    resume_button_rect = resume_button_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    quit_button_rect = quit_button_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False # Resume game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button_rect.collidepoint(event.pos):
                    paused = False # Resume game
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.blit(paused_text, paused_rect)
        screen.blit(resume_button_text, resume_button_rect)
        screen.blit(quit_button_text, quit_button_rect)
        pygame.display.update()

start_menu()

while True:
    #fps runs at 60
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_menu()

    screen.fill((86, 90, 102))
    # draw ceiling and floor by stretching textures to halves of screen
    # ceiling_s = pygame.transform.scale(ceiling_tex, (WINDOW_WIDTH, WINDOW_HEIGHT // 2))
    # floor_s = pygame.transform.scale(floor_tex, (WINDOW_WIDTH, WINDOW_HEIGHT // 2))
    # screen.blit(ceiling_s, (0, 0))
    # screen.blit(floor_s, (0, WINDOW_HEIGHT // 2))

    raycaster.castAllRays()
    raycaster.render(screen)
    player.update()
    #player.render(screen)
    pygame.display.update()
