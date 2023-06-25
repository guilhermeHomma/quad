
from player import *
from ui import * 
from tilemap import *
from settings import *

class Scene():
    def __init__(self):
        self.load_level(0)
        pass

    def update(self):
        game_viewport : pygame.Surface = pygame.Surface((GAME_SIZE+2,GAME_SIZE+2))
        game_viewport.fill(BACKGROUND_COLOR)

        if self.game_ui.state == "FINISH":
            self.load_level(self.level + 1)

        if self.game_ui.state == "GAME" and self.player == None:
            self.instance_player()
            
        if self.player:
            if self.player.state == "WIN":
                self.game_ui.run_finish_anim()
            self.player.update(self.tilemap.tile_level)

        self.game_ui.update()

        game_viewport.blit(self.tilemap.surface, (1,1))

        if self.player:
            pygame.draw.rect(game_viewport, self.player.color, self.player.rect)

        game_viewport.blit(self.game_ui.surface, (0, 0))

        return self.scaled_viewport(game_viewport)

    def load_level(self, new_level):
        if new_level >= LEVEL_QTY:
            new_level = 0

        self.level = new_level

        self.tilemap = Tilemap(f'level_{self.level}') 

        self.player = None

        self.game_ui : Ui = Ui(f'level_{self.level}')
        pass

    def instance_player(self,):
        self.player : Player = Player(tile_level=self.tilemap.tile_level)

    def scaled_viewport(self, game_viewport):
        display_size = pygame.display.get_window_size()

        if display_size[0] >= display_size[1]:
            viewport_size_y = display_size[1] if display_size[1] >= GAME_SIZE+2 else GAME_SIZE+2
            viewport_size_x = viewport_size_y
        else:
            viewport_size_x = display_size[0] if display_size[1] >= GAME_SIZE+2 else GAME_SIZE+2
            viewport_size_y = viewport_size_x

        game_viewport_scaled = pygame.transform.scale(game_viewport, (viewport_size_x, viewport_size_y))

        pos_x = display_size[0] / 2 - viewport_size_x / 2
        pos_y = display_size[1] / 2 - viewport_size_y / 2
        return game_viewport_scaled, pos_x , pos_y