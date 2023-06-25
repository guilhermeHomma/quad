from settings import *
import pygame   
import json

from enum import Enum
import animation


class Ui():
    def __init__(self, level_path : str):
        self.ui_level : dict = json.load(open(f'levels/{level_path}/ui.json'))
        self.canvas = (0, 0, GAME_SIZE+2, GAME_SIZE+2)
        self.color = CANVAS_COLOR
        self.font = pygame.font.Font(("assets/pixelart.ttf"), 8)
        self.surface = self.get_surface()
        
        self.animation = animation.Animation()
        self.run_start_anim()

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

    def run_start_anim(self):
        self.animation = animation.Animation()
        self.animation.start(80, 12, False, None)
        self.state = "START_ANIM"
        pass

    def run_finish_anim(self):
        if self.state == "FINISH_ANIM":
            return
        self.animation = animation.Animation()
        self.animation.start(80, 12, False, None)
        self.state = "FINISH_ANIM"
        pass
    
    def start_anim(self):
        pass

    def finish_anim(self):
        surf = self.get_surface()
        print("TIMES")
        pass

    def update(self):

        match self.state:
            case "FINISH_ANIM":
                self.animation.update()
                self.finish_anim()
                if self.animation.finished:
                    self.state = "FINISH"
            case "START_ANIM":
                self.animation.update()
                self.start_anim()
                if self.animation.finished:
                    self.state = "GAME"

        pass


    

