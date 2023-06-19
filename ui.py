from settings import *
import pygame   
import json


class Ui():
    def __init__(self, level_path : str):
        self.ui_level : dict = json.load(open(f'levels/{level_path}/ui.json'))
        self.canvas = (0, 0, GAME_SIZE+2, GAME_SIZE+2)
        self.color = CANVAS_COLOR
        self.font = pygame.font.Font(("assets/pixelart.ttf"), 8)
        self.surface = self.get_surface()
        
        pass

    def get_surface(self) -> pygame.Surface:
        surf : pygame.Surface = pygame.Surface((GAME_SIZE + 2, GAME_SIZE+ 2), pygame.SRCALPHA, 32)
        surf = surf.convert_alpha()

        if self.ui_level['canvas']:
            pygame.draw.rect(surf, self.color, self.canvas, 1)

        for label in self.ui_level['label']:
            text = self.font.render(label['text'], False, CANVAS_COLOR)
            surf.blit(text, (label['position_x'],label['position_y']))
        return surf