from constants import ct_red, ct_green, ct_blue
from colormaker import ColorMaker
from randpos import RandPos
import pygame as pg


class Glitter:
    def __init__(self, speed, r, top, bottom, begin, end):
        self.color = (0, 0, 0)
        self.pos = RandPos.rand_cords(top, bottom, begin, end)
        self.speed = speed
        self.r = r
        self.stage = 0
        self.cnt = 0
        self.maker = ColorMaker(self.speed)

    def behaviour(self, surface):
        if self.stage == 0:
            self.first_cycle()
        elif self.stage == 1:
            self.second_cycle()
        elif self.stage == 2:
            self.third_cycle()
        elif self.stage == 3:
            self.fourth_cycle()
        elif self.stage == 4:
            self.fifth_cycle()
        elif self.stage == 5:
            self.sixth_cycle()
        else:
            pass
        pg.draw.circle(surface, self.color, self.pos, self.r)

    def first_cycle(self):
        if self.cnt == 0:
            self.color = self.maker.make_red()
        elif self.cnt == 1:
            self.color = self.maker.make_green()
        elif self.cnt == 2:
            self.color = self.maker.make_blue()
        else:
            pass
        if self.color == ct_red:
            self.cnt = 1
        elif self.color == ct_green:
            self.cnt = 2
        elif self.color == ct_blue:
            self.cnt = 0
            self.stage = 1
        else:
            pass

    def second_cycle(self):
        if self.cnt == 0:
            self.color = self.maker.make_green()
        elif self.cnt == 1:
            self.color = self.maker.make_blue()
        elif self.cnt == 2:
            self.color = self.maker.make_red()
        else:
            pass
        if self.color == ct_green:
            self.cnt = 1
        elif self.color == ct_blue:
            self.cnt = 2
        elif self.color == ct_red:
            self.cnt = 0
            self.stage = 2
        else:
            pass

    def third_cycle(self):
        if self.cnt == 0:
            self.color = self.maker.make_blue()
        elif self.cnt == 1:
            self.color = self.maker.make_red()
        elif self.cnt == 2:
            self.color = self.maker.make_green()
        else:
            pass
        if self.color == ct_blue:
            self.cnt = 1
        elif self.color == ct_red:
            self.cnt = 2
        elif self.color == ct_green:
            self.cnt = 0
            self.stage = 3
        else:
            pass

    def fourth_cycle(self):
        if self.cnt == 0:
            self.color = self.maker.make_blue()
        elif self.cnt == 1:
            self.color = self.maker.make_green()
        elif self.cnt == 2:
            self.color = self.maker.make_red()
        else:
            pass
        if self.color == ct_blue:
            self.cnt = 1
        elif self.color == ct_green:
            self.cnt = 2
        elif self.color == ct_red:
            self.cnt = 0
            self.stage = 4
        else:
            pass

    def fifth_cycle(self):
        if self.cnt == 0:
            self.color = self.maker.make_green()
        elif self.cnt == 1:
            self.color = self.maker.make_red()
        elif self.cnt == 2:
            self.color = self.maker.make_blue()
        else:
            pass
        if self.color == ct_green:
            self.cnt = 1
        elif self.color == ct_red:
            self.cnt = 2
        elif self.color == ct_blue:
            self.cnt = 0
            self.stage = 5
        else:
            pass

    def sixth_cycle(self):
        if self.cnt == 0:
            self.color = self.maker.make_red()
        elif self.cnt == 1:
            self.color = self.maker.make_blue()
        elif self.cnt == 2:
            self.color = self.maker.make_green()
        else:
            pass
        if self.color == ct_red:
            self.cnt = 1
        elif self.color == ct_blue:
            self.cnt = 2
        elif self.color == ct_green:
            self.cnt = 0
            self.stage = 0
        else:
            pass

    def __del__(self):
        pass
