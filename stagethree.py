from turtlepaths import tp_stg1, tp_stg2, tp_stg3, tp_stg4, tp_stg5, tp_stg6
from blockpaths import bs_gray25_block, bs_col_laser_snd, bs_bld_puddle
from bgpaths import bp_cryst_tree, bp_rack
from constants import ct_size, ct_wndSize
from solidblocks import SolidBlock
from torturepaths import ts_var7
from layoutsone import ls1_road
from baseclasses import Block
from devoured import Devoured
from glitter import Glitter
from random import randint
from candle import Candle
from timer import Timer
from stage import Stage
import pygame as pg


class StageThree(Stage):
    def __init__(self, surface, penguin):
        super().__init__(surface, penguin)
        for row_index, row in enumerate(ls1_road):
            for col_index, cell in enumerate(row):
                x, y = col_index*ct_size, row_index*ct_size
                if cell == 'G':
                    block = SolidBlock(ct_size, ct_size, (x, y), bs_gray25_block,
                                       True, bs_col_laser_snd)
                    self.ground.append(block)
        self.busy = True
        tr_x, tr_y = -ct_size, ct_wndSize[1] - ct_size * 17
        tr_w, tr_h = ct_size * 6, ct_size * 15
        for i in range(7):
            x = tr_x + (tr_w + ct_size * 2) * i
            tree = Block(tr_w, tr_h, (x, tr_y), bp_cryst_tree)
            self.phone.append(tree)
        self.cemetery = []
        p_x, p_y = -ct_size, ct_wndSize[1]-ct_size*3
        p_w, p_h = ct_size*1.5, ct_size*.4
        for i in range(40):
            x = p_x + p_w*i*.8
            puddle = Block(p_w, p_h, (x, p_y), bs_bld_puddle)
            self.cemetery.append(puddle)
        dd_x, dd_y = -ct_size, ct_wndSize[1]-ct_size*4.5
        dd_w, dd_h = ct_size*2, ct_size*1.5
        for i in range(15):
            x = dd_x + dd_w*i*2
            dead = Block(dd_w, dd_h, (x, dd_y), ts_var7)
            n = randint(0, 1)
            if n == 1:
                dead.image = pg.transform.flip(dead.image, True, False)
            self.cemetery.append(dead)
        self.sanctuary = []
        fire_paths = [tp_stg1, tp_stg2, tp_stg3, tp_stg4, tp_stg5, tp_stg6]
        r_w, r_h = ct_size*2, ct_size
        r_x, r_y = -ct_size, ct_wndSize[1]-ct_size*10
        for i in range(13):
            x = r_x + r_w*i*2
            candle = Candle(bp_rack, fire_paths, r_w, r_h, (x, r_y))
            self.sanctuary.append(candle)
        self.candle_timer = Timer()
        length, m_speed = 200, .5
        top, bottom, begin, end = -ct_size, ct_size*6, -ct_size, ct_size*50
        self.glitter = []
        for i in range(length):
            speed = m_speed + i/(length*10)
            glit = Glitter(speed, ct_size, top, bottom, begin, end)
            self.glitter.append(glit)
        self.devour = Devoured(self.surface)

    def behaviour(self):
        if self.active:
            if self.penguin.alive:
                self.mainloop()
            else:
                self.dead_loop()

    def mainloop(self):
        self.refresh_data()
        self.set_background()
        self.place()
        self.set_glitter()
        self.p_pos = self.penguin.rect.left
        self.devour.ended = False
        self.points()
        self.collide_place()
        self.set_cemetery()
        self.set_sanctuary()
        self.cond_end()

    def dead_loop(self):
        self.busy = True
        self.devour.behaviour()
        self.state = self.devour.choice()
        if self.state == 2:
            self.dead = self.devour.ended
        elif self.state == 1:
            self.devour.reset()
            self.devour.defined = False
            self.penguin.alive = True
            self.devour.state = 0

    def cond_end(self):
        if self.p_pos >= ct_size*35:
            self.finished = True

    def set_sanctuary(self):
        off_cntr = 0
        time = self.candle_timer.get_time()
        for i, stuff in enumerate(self.sanctuary):
            stuff.update(self.surface)
            if time >= i:
                stuff.burning = False
                off_cntr += 1
        if off_cntr >= len(self.sanctuary):
            self.penguin.alive = False

    def reset_sanctuary(self):
        self.candle_timer.restart()
        for stuff in self.sanctuary:
            stuff.burning = True

    def set_cemetery(self):
        for thing in self.cemetery:
            thing.update(self.surface)

    def set_glitter(self):
        for glit in self.glitter:
            glit.behaviour(self.surface)

    def __del__(self):
        pass
