from blockpaths import bs_gray25_block, bs_col_laser_snd, bs_bld_puddle
from solidblocks import SolidBlock, DestroyableBlock
from torturepaths import ts_var5, ts_sh_bleeding
from constants import ct_size, ct_wndSize
from vector import Point, Vector
from layoutsone import ls1_road
from baseclasses import Block
from bgpaths import bp_meat
from random import randint
from stage import Stage
import pygame as pg


class StageOne(Stage):
    def __init__(self, surface, penguin):
        super().__init__(surface, penguin)
        for row_index, row in enumerate(ls1_road):
            for col_index, cell in enumerate(row):
                x, y = col_index*ct_size, row_index*ct_size
                if cell == 'G':
                    block = SolidBlock(ct_size, ct_size, (x, y), bs_gray25_block,
                                       True, bs_col_laser_snd)
                    self.ground.append(block)
        self.wall = []
        x_w, y_w = ct_size*23, ct_wndSize[1]-ct_size*4
        for i in range(7):
            w_y = y_w - ct_size*i*.8
            for j in range(10):
                w_x = x_w + ct_size*j*1.2
                phys = DestroyableBlock(ct_size*1.5, ct_size, (w_x, w_y),
                                        ts_var5, True, True,
                                        ts_sh_bleeding)
                n = randint(0, 1)
                if n == 0:
                    phys.image = pg.transform.flip(phys.image, True, False)
                self.wall.append(phys)
        self.trash = []
        m_x1, m_y = ct_size * 17, ct_wndSize[1] - ct_size*4
        for i in range(12):
            y_m = m_y - ct_size*i
            for j in range(29 - i*2):
                x_m = m_x1 + ct_size*j + ct_size*i
                meat = Block(ct_size, ct_size, (x_m, y_m), bp_meat)
                self.trash.append(meat)
        self.puddles = []
        for i in range(30):
            x_m = m_x1 + ct_size*i
            puddle = Block(ct_size*1.5, ct_size*.4, (x_m, m_y + ct_size),
                           bs_bld_puddle)
            self.puddles.append(puddle)

    def behaviour(self):
        if self.active:
            self.refresh_data()
            self.background()
            self.place()
            self.collide_wall()
            self.bld_puddle()
            self.p_pos = self.penguin.rect.left
            self.termine_end()
            self.points()
            self.collide_place()

    def termine_end(self):
        pos = self.penguin.rect.left
        if pos >= ct_size*30:
            self.finished = True

    def background(self):
        for meat in self.trash:
            meat.update(self.surface)

    def bld_puddle(self):
        for puddle in self.puddles:
            puddle.update(self.surface)

    def collide_wall(self):
        p_x, p_y = self.penguin.rect.left, self.penguin.rect.top
        pen_pos = Point((p_x, p_y))
        for dead in self.wall:
            d_x, d_y = dead.rect.left, dead.rect.top
            ded_pos = Point((d_x, d_y))
            v = Vector(pen_pos, ded_pos)
            m = v.modulus()
            if (m <= ct_size*2) and (not dead.destroyed):
                self.penguin = dead.react(self.penguin, self.wall)
            self.penguin.bullet = dead.collide_ammo(self.penguin.bullet)
            dead.behaviour(self.surface)

    def __del__(self):
        pass
