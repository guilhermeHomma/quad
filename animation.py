import pygame

class Animation():
    def __init__(self,):
        self.finished = False
        pass

    def start(self, frame_time, frame_qty, loop : bool = False, call_on_finish = None):
        self.last_tick = pygame.time.get_ticks()

        self.frame_time = frame_time

        self.frame_qty = frame_qty

        self.current_frame = 1

        self.loop = loop

        self.finished = False

        self.call_on_finish = call_on_finish
        pass

    def update(self):
        if self.finished:
            return
        
        _current_tick = pygame.time.get_ticks()
        if self.last_tick + self.frame_time > _current_tick:
            return
        
        self.last_tick = _current_tick

        self.current_frame += 1

        if self.current_frame > self.frame_qty:
            
            if self.call_on_finish != None:
                self.call_on_finish()

            if not self.loop:
                self.finished = True
                return
            
            self.current_frame = 1


