from constants import ct_sulfur, ct_size, ct_wndSize, ct_frT
from constants import ct_black
from demonspaths import dp_star, dp_s_stay
from bgpaths import bp_meat, bp_h_tree
from demonbomber import DemonBomber
from hellisheye import HellishEye
from layoutsone import ls1_road
from baseclasses import Block
from randpos import RandPos
from timer import Timer
import pygame as pg


class DemonScene:
    def __init__(self):
        pg.mouse.set_visible(False)
        self.surface_c = ct_sulfur
        self.ended, self.came = False, False
        self.ground = []
        for row_index, row in enumerate(ls1_road):
            for col_index, cell in enumerate(row):
                x, y = ct_size*col_index, ct_size*row_index
                if cell == 'G':
                    block = Block(ct_size, ct_size, (x, y), bp_meat)
                    self.ground.append(block)
        self.trees = []
        x_tre, y_tre = 0, ct_wndSize[1]-ct_size*6.7
        for i in range(10):
            x = ct_size*i*10
            tree = Block(ct_size*3, ct_size*4, (x, y_tre), bp_h_tree)
            self.trees.append(tree)
        self.d_bombers = []
        x_d, y_d = -ct_size*40, ct_wndSize[1]-ct_size*5
        for i in range(15):
            x = x_d+ct_size*i*2
            d_bomber = DemonBomber(ct_size*5, ct_size*300, ct_size*1.5, ct_size*2,
                                   20, 60, (x, y_d))
            self.d_bombers.append(d_bomber)
        self.h_eyes = []
        for i in range(15):
            x = x_d+ct_size*i*3
            eye = HellishEye(ct_size*6, ct_size*350, ct_size*2, ct_size*2,
                             13, 13, (x, ct_size*13))
            self.h_eyes.append(eye)
        begin, end = -ct_size*5, ct_wndSize[0]+ct_size*5
        top, bottom = -ct_size*5, ct_wndSize[1]+ct_size*5
        self.stars = []
        for i in range(1000):
            pos = RandPos.rand_cords(top, bottom, begin, end)
            star = Block(ct_size*2, ct_size*2, pos, dp_star)
            self.stars.append(star)
        s_pos = (ct_size * 35, y_tre - ct_size * 3)
        self.satan = Block(ct_size*3, ct_size*7, s_pos, dp_s_stay)
        self.satan.image = pg.transform.flip(self.satan.image, True, False)
        self.timer_bombers = Timer()
        self.timer_eyes = Timer()
        self.timer_stars = Timer()

    def behaviour(self, surface):
        surface.fill(self.surface_c)
        if not self.ended:
            self.place(surface)
            self.bombers_stream(surface)
            self.eyes_stream(surface)
            self.satan.update(surface)
            if self.came:
                self.pin_star(surface)
        pg.display.flip()

    def pin_star(self, surface):
        time = self.timer_stars.get_time()
        for i, star in enumerate(self.stars):
            if time >= ct_frT*i*.02:
                self.stars[i].update(surface)
            if time > 2:
                self.ended = True
                self.surface_c = ct_black

    def eyes_stream(self, surface):
        time = self.timer_eyes.get_time()
        for eye in self.h_eyes:
            if time < 5:
                eye.moving(ct_size*30)
            eye.update(surface)

    def bombers_stream(self, surface):
        time = self.timer_bombers.get_time()
        for bomber in self.d_bombers:
            if time < 10:
                bomber.moving(ct_size * 30)
            else:
                self.came = True
            bomber.update(surface)

    def place(self, surface):
        for tree in self.trees:
            tree.update(surface)
        for block in self.ground:
            block.update(surface)

    def __del__(self):
        pass
