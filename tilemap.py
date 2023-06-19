

import pygame, json, settings
from settings import *


class Tilemap():
    def __init__(self, level_path : str):
        self.tile_level : list = json.load(open(f'levels/{level_path}/tilemap_level.json'))
        self.surface = self.get_surface()
        pass

    def get_surface(self) -> pygame.Surface:
        surf : pygame.Surface = pygame.Surface((GAME_SIZE, GAME_SIZE), pygame.SRCALPHA, 32)
        surf = surf.convert_alpha()

        for y, list_x in enumerate(self.tile_level):
            for x, tile in enumerate(list_x):
                if tile == NULL_TILE:
                    continue
                if tile == GROUND_TILE:
                    self._draw_ground(surf, x, y, len(list_x), len(self.tile_level))
                if tile == END_TILE:
                    self._draw_end(surf, x, y)

                if tile == FIRE_TILE:
                    self._draw_fire(surf, x, y)
        return surf

    def _draw_ground(self, surf, x, y, len_x, len_y):
        if x < len_x -1:
            if self.tile_level[y][x + 1] != 1:
                start_pos = (x * TILE_SIZE + TILE_SIZE -1, y * TILE_SIZE )
                end_pos = (x * TILE_SIZE + TILE_SIZE -1, y * TILE_SIZE + TILE_SIZE -1)
                pygame.draw.line(surf, TILE_COLOR , start_pos, end_pos)
        if x != 0:
            if self.tile_level[y][x - 1] != 1:
                start_pos = (x * TILE_SIZE, y * TILE_SIZE )
                end_pos = (x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE -1)
                pygame.draw.line(surf, TILE_COLOR , start_pos, end_pos)
        if y < len_y -1:
            if self.tile_level[y + 1][x] != 1:
                start_pos = (x * TILE_SIZE , y * TILE_SIZE + TILE_SIZE -1)
                end_pos = (x * TILE_SIZE + TILE_SIZE -1, y * TILE_SIZE  + TILE_SIZE -1)
                pygame.draw.line(surf, TILE_COLOR , start_pos, end_pos)
        if y != 0:
            if self.tile_level[y - 1][x] != 1:
                start_pos = (x * TILE_SIZE, y * TILE_SIZE )
                end_pos = (x * TILE_SIZE  + TILE_SIZE - 1, y * TILE_SIZE)
                pygame.draw.line(surf, TILE_COLOR , start_pos, end_pos)

    def _draw_end(self, surf, x, y):
        pygame.draw.rect(surf, END_COLOR[0], (x*TILE_SIZE + 2, y*TILE_SIZE+2, 4,4))
        pygame.draw.rect(surf, END_COLOR[1], (x*TILE_SIZE + 3, y*TILE_SIZE+3, 2,2))

    def _draw_fire(self, surf, x, y):
        start_pos = (x * TILE_SIZE , y * TILE_SIZE + TILE_SIZE -1)
        end_pos = (x * TILE_SIZE + TILE_SIZE -1, y * TILE_SIZE  + TILE_SIZE -1)
        pygame.draw.line(surf, FIRE_COLOR , start_pos, end_pos)
