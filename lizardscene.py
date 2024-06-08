from blockpaths import bs_grass_block, bs_dark_red_block, bs_brown_block
from blockpaths import bs_magma_block
from constants import ct_size, ct_wndSize, ct_blue, ct_red, ct_black
from lizardspaths import lp_d_stay, lp_boss_stay, lp_patron_stay
from bgpaths import bp_tree, bp_bush, bp_gidnora, bp_octopus
from layoutsone import ls1_meeting
from baseclasses import Block
from lizard import Lizard
from timer import Timer
import random as rd
import pygame as pg


class LizardScene:
    def __init__(self):
        self.ground1, self.ground2 = [], []
        for row_index, row in enumerate(ls1_meeting):
            for col_index, cell in enumerate(row):
                x = col_index*ct_size
                y = row_index*ct_size
                if cell == 'G':
                    block1 = Block(ct_size, ct_size, (x, y), bs_grass_block)
                    block2 = Block(ct_size, ct_size, (x, y), bs_dark_red_block)
                    self.ground1.append(block1)
                    self.ground2.append(block2)
                elif cell == 'D':
                    block1 = Block(ct_size, ct_size, (x, y), bs_brown_block)
                    block2 = Block(ct_size, ct_size, (x, y), bs_magma_block)
                    self.ground1.append(block1)
                    self.ground2.append(block2)
                else:
                    continue
        self.prepared = False
        self.ended = False
        self.surface_color = ct_blue
        liz_y = ct_wndSize[1]-ct_size*7
        self.lizards, self.liz_demons = [], []
        self.trees, self.bushes = [], []
        self.gidnora, self.octopus = [], []
        tre_x = ct_size*17
        for i in range(30):
            n = rd.randint(0, 1)
            female = True if (n == 1) else False
            liz_x = ct_size*50 + ct_size*4*i
            lizard = Lizard(ct_size*7, ct_size*350, ct_size*3, ct_size*4,
                            100, 30, (liz_x, liz_y), female)
            lizard.right = False
            self.lizards.append(lizard)
            x_tre = tre_x + ct_size*7*i
            tree = Block(ct_size*6, ct_size*15, (x_tre, liz_y-ct_size*10), bp_tree)
            x_bus = tre_x + ct_size + ct_size*6*i
            bush = Block(ct_size*5, ct_size*4, (x_bus, liz_y), bp_bush)
            self.bushes.append(bush)
            self.trees.append(tree)
            liz_d_raw = pg.image.load(lp_d_stay).convert_alpha()
            liz_d = pg.transform.scale(liz_d_raw, (ct_size*3, ct_size*4))
            lizard_demon = pg.transform.flip(liz_d, True, False)
            liz_d_rect = lizard_demon.get_rect()
            liz_d_rect.left = tre_x + ct_size * 5 + ct_size * 4 * i
            liz_d_rect.top = liz_y
            self.liz_demons.append((lizard_demon, liz_d_rect))
            gid_x = tre_x + ct_size*i*9
            gidnora = Block(ct_size*8, ct_size*10, (gid_x, liz_y-ct_size*6), bp_gidnora)
            self.gidnora.append(gidnora)
            oc_x = tre_x + ct_size*7*i
            octopus = Block(ct_size*6, ct_size*5, (oc_x, liz_y-ct_size), bp_octopus)
            self.octopus.append(octopus)
        liz_b_raw = pg.image.load(lp_boss_stay).convert_alpha()
        liz_b = pg.transform.scale(liz_b_raw, (ct_size*3, ct_size*4))
        liz_boss = pg.transform.flip(liz_b, True, False)
        liz_b_rect = liz_boss.get_rect()
        liz_b_rect.left = ct_size*15
        liz_b_rect.top = liz_y
        self.lizard_boss = (liz_boss, liz_b_rect)
        pat_pos = (ct_size*8, liz_y-ct_size*2)
        self.lizards_patron = Block(ct_size*3, ct_size*5, pat_pos, lp_patron_stay)
        self.rect_w, self.rect_h = ct_wndSize[0], ct_size*2
        self.line_w = ct_size*.5
        self.timer = Timer()
        self.timer_lack = Timer()
        self.timer_end = Timer()
        pg.mouse.set_visible(False)

    def behaviour(self, surface):
        if not self.ended:
            surface.fill(self.surface_color)
            self.drawing(surface)
            pg.display.flip()

    def drawing(self, surface):
        if not self.prepared:
            self.draw_one(surface)
        else:
            self.draw_two(surface)

    def draw_one(self, surface):
        self.surface_color = ct_blue
        for tree in self.trees:
            tree.update(surface)
        for bush in self.bushes:
            bush.update(surface)
        for block in self.ground1:
            block.update(surface)
        self.lizards_patron.update(surface)
        for lizard in self.lizards:
            lizard.update(surface)
        self.liz_stream_one(surface)

    def liz_stream_one(self, surface):
        time = self.timer.get_time()
        if time < 5.4:
            for lizard in self.lizards:
                lizard.moving(ct_size*15)
        if time > 6:
            self.lack_red(surface)

    def draw_two(self, surface):
        self.surface_color = ct_red
        for block in self.ground2:
            block.update(surface)
        for gidnora in self.gidnora:
            gidnora.update(surface)
        for octopus in self.octopus:
            octopus.update(surface)
        for demon in self.liz_demons:
            surface.blit(demon[0], demon[1])
        surface.blit(self.lizard_boss[0], self.lizard_boss[1])
        self.lizards_patron.update(surface)
        self.bedaub(surface)
        if self.line_w >= ct_wndSize[1]*.6:
            self.ended = True

    def bedaub(self, surface):
        time = self.timer_end.get_time()
        self.timer_end.restart()
        pg.draw.rect(surface, ct_black, (0, 0, ct_wndSize[0], ct_wndSize[1]), int(self.line_w))
        self.line_w += ct_size*time

    def lack_red(self, surface):
        pg.draw.rect(surface, ct_red, (0, 0, self.rect_w, self.rect_h))
        time = self.timer_lack.get_time()
        self.rect_h += ct_size * time * 4
        self.timer_lack.restart()
        if self.rect_h >= ct_wndSize[1]:
            self.prepared = True

    def __del__(self):
        pass
