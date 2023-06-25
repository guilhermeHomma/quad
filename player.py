import pygame
from settings import *
class Player():
    def __init__(self, tile_level):
        self.collider = PLAYER_SIZE
        self.size = self.collider
        self.position = [0, 0]
        self.color = PLAYER_COLOR
        self.velocity = [0, 0]
        self.rect = (self.position[0], self.position[1], self.size[0], self.size[1])
        self.surface = pygame.Surface(self.size)
        self.is_on_ground : bool = False
        
        self.state : str = 'SPAWN'

        self.jump_sound = pygame.mixer.Sound('assets/sounds/jumpSound.mp3')
        
        self.death_sound = pygame.mixer.Sound('assets/sounds/deathSound.mp3')

        pass

    def update(self, tile_level : list):
        match self.state:
            case 'PLAY':
                self.gravity()

                self.move(tile_level=tile_level)

            case "DEATH":
                finished_anim = self.death_anim()
                if finished_anim:
                    self.state = 'SPAWN'
            case "WIN":
                pass

            case 'SPAWN':
                finished_anim = self.player_spawn(tile_level)
                if finished_anim:
                    self.state = "PLAY"
        pass

    def move(self, tile_level) -> None:
        self.velocity[0] = 0

        if pygame.key.get_pressed()[pygame.K_a]:
            self.velocity[0] = -PLAYER_SPEED
        if pygame.key.get_pressed()[pygame.K_d]:
            self.velocity[0] = PLAYER_SPEED

        if pygame.key.get_pressed()[pygame.K_SPACE] and self.is_on_ground:
            self.velocity[1] = -JUMP_FORCE
            #print(pygame.mixer.get_num_channels())
            self.jump_sound.play()
        
        if pygame.key.get_pressed()[pygame.K_TAB]:
            self.player_spawn(tile_level=tile_level)
        self.is_on_ground = False

        self.canvas_collision()
        self.tile_collision(tile_level)

        self.position[0] += int(self.velocity[0])
        self.position[1] += int(self.velocity[1])

        if self.velocity[1] <= -3.0:
            self.size = [2, 5]
            self.rect = (self.position[0] + 1, self.position[1] -1, self.size[0], self.size[1])
        else:
            self.size = [4, 4]
            self.rect = (self.position[0], self.position[1], self.size[0], self.size[1])
        
        pass

    def tile_collision(self, tile_level) -> None:

        for y, list_x in enumerate(tile_level):
            for x, tile in enumerate(list_x):
                if tile in [NULL_TILE, PLAYER_TILE]:
                    continue
                if tile == GROUND_TILE:
                    self.ground_collision(x, y)

                if tile == END_TILE:
                    self.end_collision(x, y)

                if tile == FIRE_TILE:
                    self.fire_collision(x, y)

    def player_spawn(self, tile_level) -> None:
        for y, list_x in enumerate(tile_level):
            for x, tile in enumerate(list_x):
                if tile == PLAYER_TILE:
                    center_tile_pos : list = [x*TILE_SIZE + TILE_SIZE/2 +1 , y*TILE_SIZE+TILE_SIZE/2 + 1]
                    self.position[0] = center_tile_pos[0] - self.size[0] / 2
                    self.position[1] = center_tile_pos[1] - self.size[1] / 2
                    self.velocity = [0, 0]
                    self.rect = (self.position[0], self.position[1], self.size[0], self.size[1])
        return True
    
    def death_anim(self):
        self.death_sound.play()
        return True
                    
    def gravity(self) -> None:
        self.velocity[1] += GRAVITY

        if self.velocity[1] > 2: 
            self.velocity[1] = 2

    def canvas_collision(self) -> None:
        bottom = self.position[1] + self.collider[1] 
        if bottom  > GAME_SIZE + 1: 
            self.state = "DEATH"
        pass

    def on_win(self):
        self.state = "WIN"
        pygame.mixer.Sound('assets/sounds/spawnSound.mp3').play()
        self.velocity[0] = 0
        self.gravity()
        pass

    def end_collision(self, x, y) -> None:
        tile_pos = (x * TILE_SIZE + 1, y * TILE_SIZE + 1)

        tile_rect = pygame.Rect(tile_pos, (TILE_SIZE, TILE_SIZE))

        collision = pygame.Rect((self.position[0], self.position[1]), (self.collider[0], self.collider[1])).colliderect(tile_rect)
        if not collision:
            return

        self.on_win()
        


    def fire_collision(self, x, y) -> None:
        tile_pos = (x * TILE_SIZE + 1, y * TILE_SIZE + 8)

        tile_rect = pygame.Rect(tile_pos, (TILE_SIZE, 1))

        collision = pygame.Rect((self.position[0] + int(self.velocity[0]), self.position[1] + int(self.velocity[1])), (self.collider[0], self.collider[1])).colliderect(tile_rect)
        if not collision:
            return
        self.state = "DEATH"

    def ground_collision(self, x, y) -> None:
        tile_pos = (x * TILE_SIZE + 1, y * TILE_SIZE + 1)

        tile_rect = pygame.Rect(tile_pos, (TILE_SIZE, TILE_SIZE))

        collision = pygame.Rect((self.position[0] + int(self.velocity[0]), self.position[1] + int(self.velocity[1])), (self.collider[0], self.collider[1])).colliderect(tile_rect)
        if not collision:
            return

        p_bottom_after = self.position[1] + self.collider[1] + int(self.velocity[1])
        p_bottom_current = self.position[1] + self.collider[1]
        if p_bottom_after >= tile_pos[1] and p_bottom_current <= tile_pos[1]:
            self.velocity[1] = tile_pos[1] - p_bottom_current
            self.is_on_ground = True
            return
            
        p_right_after = self.position[0] + self.collider[0] + int(self.velocity[0])
        p_right_current = self.position[0] + self.collider[0]
        if p_right_after >= tile_pos[0] and p_right_current <= tile_pos[0]:
            self.velocity[0] = tile_pos[0] - p_right_current
            return
        p_left_after = self.position[0] + int(self.velocity[0])
        p_left_current = self.position[0]
        if p_left_after <= tile_pos[0] + TILE_SIZE and p_left_current >= tile_pos[0] + TILE_SIZE:
            self.velocity[0] = tile_pos[0] + TILE_SIZE - p_left_current
            return

        p_ceil_after = self.position[1] + int(self.velocity[1])
        p_ceil_current = self.position[1]
        if p_ceil_after <= tile_pos[1] + TILE_SIZE and p_ceil_current >= tile_pos[1] + TILE_SIZE:
            self.velocity[1] = tile_pos[1] + TILE_SIZE - p_ceil_current


    