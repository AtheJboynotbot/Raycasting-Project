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

# View mode: "3D" for raycasting, "2D" for top-down map
view_mode = "3D"


def start_menu():
    title_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 30)
    title_text1 = title_font.render("Pseudo 3D Environment using Raycasting", True, (255, 255, 255))
    title_text05 = title_font.render("by", True, (255, 255, 255))
    title_text2 = title_font.render("Esfandiary, Hisu-an, Judaya, and Perez", True, (255, 255, 255))
    start_button_text = button_font.render("Start", True, (255, 255, 255))
    title_rect1 = title_text1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    title_rect05 = title_text05.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 60))
    title_rect2 = title_text2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 120))
    start_button_rect = start_button_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 240))

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
        screen.blit(title_text1, title_rect1)
        screen.blit(title_text2, title_rect2)
        screen.blit(title_text05, title_rect05)
        pygame.draw.rect(screen, (50, 50, 50), start_button_rect.inflate(20, 10))  # Button background
        screen.blit(start_button_text, start_button_rect)
        pygame.display.update()


def pause_menu():
    global view_mode  # Access global view mode variable
    paused = True
    title_font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 30)
    
    while paused:
        # Update text based on current view mode
        paused_text = title_font.render("Paused", True, (255, 255, 255))
        resume_button_text = button_font.render("Resume", True, (255, 255, 255))
        toggle_text = f"View: {view_mode}"
        toggle_button_text = button_font.render(toggle_text, True, (255, 255, 255))
        quit_button_text = button_font.render("Quit", True, (255, 255, 255))

        paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        resume_button_rect = resume_button_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        toggle_button_rect = toggle_button_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        quit_button_rect = quit_button_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))

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
                if toggle_button_rect.collidepoint(event.pos):
                    # Toggle between 2D and 3D views
                    view_mode = "2D" if view_mode == "3D" else "3D"
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Draw pause menu with semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        screen.blit(paused_text, paused_rect)
        pygame.draw.rect(screen, (50, 50, 50), resume_button_rect.inflate(20, 10))
        screen.blit(resume_button_text, resume_button_rect)
        pygame.draw.rect(screen, (70, 70, 70), toggle_button_rect.inflate(20, 10))
        screen.blit(toggle_button_text, toggle_button_rect)
        pygame.draw.rect(screen, (50, 50, 50), quit_button_rect.inflate(20, 10))
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

    player.update()
    
    if view_mode == "3D":
        # 3D view
        screen.fill((86, 90, 102))
        raycaster.castAllRays()
        raycaster.render(screen)
    else:
        # 2D Tview
        screen.fill((0, 0, 0))
        map.render(screen)
        
        #this will render rays in 2D
        raycaster.castAllRays()
        for ray in raycaster.rays:
            ray.render(screen)
        
        player.render(screen)
    
    pygame.display.update()
