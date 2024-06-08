from rectentity import RectEntity
from timer import Timer
import pygame as pg


class ScreamerBar:
    def __init__(self, total_width, height, color1, color2, pos):
        self.width1, self.width2 = total_width*.5, total_width*.5
        self.color1, self.color2 = color1, color2
        self.height, self.width, self.pos = height, total_width, pos
        self.bar1 = RectEntity(self.width1, self.height, self.color1, pos[0], pos[1])
        self.bar = RectEntity(self.width, self.height, self.color2, pos[0], pos[1])
        self.timer, self.k = Timer(), 1
        self.full, self.burst = False, False

    def behaviour(self, surface):
        if not self.full:
            time = self.timer.get_time()
            self.timer.restart()
            self.k -= time*.8
            self.keys(time)
            self.bar1.width *= self.k
            self.last_stand()
            self.drawings(surface)
            self.bar1.width = self.width1

    def last_stand(self):
        if self.k >= 1.8 and not self.burst:
            self.k = .3
            self.burst = True

    def drawings(self, surface):
        self.bar.draw(surface)
        self.bar1.draw(surface)

    def keys(self, time):
        key = pg.key.get_pressed()
        if key[pg.K_SPACE]:
            if self.k <= 2:
                self.k += time
            else:
                self.full = True

    def reset(self):
        self.bar1.width, self.k = self.width1, 1
        self.full, self.burst = False, False

    def __del__(self):
        pass
