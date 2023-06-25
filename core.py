import pygame, sys

from settings import *
from scene import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((720,720), pygame.RESIZABLE)

game_scene : Scene = Scene()

IS_RUNNING : bool = True
while IS_RUNNING:
    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #pygame.quit()
            IS_RUNNING = False
    
    screen.fill(BACKGROUND_COLOR)

    game_viewport, pos_x, pos_y = game_scene.update()

    screen.blit(game_viewport, (pos_x, pos_y))

    pygame.display.update()
    pass