from turtlepaths import tp_stg1, tp_stg2, tp_stg3, tp_stg4, tp_stg5, tp_stg6
from turtlepaths import tp_p_img, tp_boss_stay, tp_boss_prayer, tp_c_stay
from constants import ct_size, ct_wndSize, ct_black, ct_blue, ct_green
from constants import ct_red
from blockpaths import bs_grass_block, bs_gray25_block, bs_brown_block
from blockpaths import bs_emerald_block, bs_bld_drip
from bgpaths import bp_ap_tree, bp_cryst_tree
from layoutsone import ls1_pedestal
from rectentity import RectEntity
from baseclasses import Block
from turtle import Turtle
from timer import Timer
from drip import Drip
from fire import Fire
import random as rd
import pygame as pg


class TurtleScene:
    def __init__(self):
        self.ground1, self.ground2 = [], []
        for row_index, row in enumerate(ls1_pedestal):
            for col_index, cell in enumerate(row):
                x = col_index * ct_size
                y = row_index * ct_size
                if cell == 'G':
                    block1 = Block(ct_size, ct_size, (x, y), bs_grass_block)
                    block2 = Block(ct_size, ct_size, (x, y), bs_gray25_block)
                    self.ground1.append(block1)
                    self.ground2.append(block2)
                elif cell == 'D':
                    block1 = Block(ct_size, ct_size, (x, y), bs_brown_block)
                    block2 = Block(ct_size, ct_size, (x, y), bs_emerald_block)
                    self.ground1.append(block1)
                    self.ground2.append(block2)
                else:
                    continue
        pg.mouse.set_visible(False)
        self.rect = RectEntity(ct_wndSize[0], ct_wndSize[1], ct_black, 0, 0)
        self.timer_rect = Timer()
        self.surf_color = ct_blue
        fire_pths = [tp_stg1, tp_stg2, tp_stg3, tp_stg4, tp_stg5, tp_stg6]
        fire_y = ct_wndSize[1]
        self.fire = []
        for i in range(55):
            x = ct_size*i
            bonfire = Fire(fire_pths, ct_size*1.5, ct_size*1.5, (x, fire_y))
            bonfire.sound_on = False
            self.fire.append(bonfire)
        self.turtles1, self.turtles2 = [], []
        t_y = ct_wndSize[1]-ct_size*5.5
        self.t_timer1 = Timer()
        self.t_timer2 = Timer()
        self.draw_timer = Timer()
        for i in range(10):
            x = -ct_size*20+ct_size*i*1.5
            num = rd.randint(0, 1)
            female = True if (num == 1) else False
            turtle = Turtle(ct_size*3, ct_size*250, ct_size*1.5, ct_size*2.5, 200, 15,
                            (x, t_y), female)
            self.turtles1.append(turtle)
        for i in range(10):
            x = ct_wndSize[0]+ct_size*i*1.5
            num = rd.randint(0, 1)
            female = True if (num == 1) else False
            turtle = Turtle(ct_size*3, ct_size*250, ct_size*1.5, ct_size*2.5, 200, 15,
                            (x, t_y), female)
            self.turtles2.append(turtle)
        self.t_patron = Block(ct_size*6, ct_size*4, (ct_size*26, t_y-ct_size*4.5), tp_p_img)
        b_stay_raw = pg.image.load(tp_boss_stay)
        b_stay = pg.transform.scale(b_stay_raw, (ct_size*1.5, ct_size*2.5))
        boss_stay = pg.transform.flip(b_stay, True, False)
        boss_stay_rect = boss_stay.get_rect()
        boss_stay_rect.left = ct_size*20
        boss_stay_rect.top = t_y - ct_size
        self.boss_stay = (boss_stay, boss_stay_rect)
        self.boss_prayer = Block(ct_size*3, ct_size*2.5, (ct_size*24.5, ct_size*4), tp_boss_prayer)
        self.apple_trees, self.crystal_trees = [], []
        x_tre, y_tre1, y_tre2 = 0, t_y-ct_size*7.5, t_y-ct_size*8.5
        for i in range(30):
            x = x_tre + ct_size*i*5
            x_c = x_tre + ct_size*i*6
            y = y_tre2 if ((x >= ct_size*17) and (x <= ct_size*30)) else y_tre1
            tree = Block(ct_size*4, ct_size*10, (x, y), bp_ap_tree)
            crystal_tree = Block(ct_size*5, ct_size*10, (x_c, y+ct_size*1.3), bp_cryst_tree)
            self.apple_trees.append(tree)
            self.crystal_trees.append(crystal_tree)
        x_cult1, x_cult2 = ct_size*15, ct_size*36
        self.cultists = []
        for i in range(10):
            x1, x2 = x_cult1 - ct_size*1.5*i, x_cult2 + ct_size*1.5*i
            cultist1 = Block(ct_size*1.5, ct_size*2.5, (x1, t_y), tp_c_stay)
            cultist2 = Block(ct_size*1.5, ct_size*2.5, (x2, t_y), tp_c_stay)
            cultist2.image = pg.transform.flip(cultist2.image, True, False)
            self.cultists.append(cultist1)
            self.cultists.append(cultist2)
        top, line, bottom = -ct_size*50, 0, ct_wndSize[1]
        begin, end = -ct_size*5, ct_wndSize[0]+ct_size*5
        self.rain = []
        for i in range(1500):
            drip = Drip(ct_size*.2, ct_size*.4, bs_bld_drip, top, line, bottom,
                        begin, end, 0)
            self.rain.append(drip)
        self.timer_rain = Timer()
        self.timer_drip = Timer()
        self.came = False
        self.ended = False

    def behaviour(self, surface):
        surface.fill(self.surf_color)
        if not self.ended:
            if not self.came:
                self.drawings_one(surface)
            else:
                self.drawings_two(surface)
        pg.display.flip()

    def drawings_two(self, surface):
        time = self.draw_timer.get_time()
        if time < 1:
            self.surf_color = ct_green
        else:
            time = self.timer_rain.get_time()
            self.surf_color = ct_black
            self.place_two(surface)
            for cultist in self.cultists:
                cultist.update(surface)
            self.boss_prayer.update(surface)
            self.t_patron.rect.top = ct_size*8
            self.t_patron.rect.left = ct_size*23
            self.t_patron.update(surface)
            if time > 3:
                self.bloody_rain(surface)
            if time > 5:
                self.ended = True
                self.surf_color = ct_black

    def place_two(self, surface):
        for crystal_tree in self.crystal_trees:
            crystal_tree.update(surface)
        for block in self.ground2:
            block.update(surface)
        pg.draw.circle(surface, ct_red, (ct_size*26, ct_size*5), ct_size*5)

    def bloody_rain(self, surface):
        time = self.timer_drip.get_time()
        self.timer_drip.restart()
        speed = ct_size*time*1000
        for drip in self.rain:
            drip.speed = speed
            drip.update(surface)

    def drawings_one(self, surface):
        self.surf_color = ct_blue
        self.place_one(surface)
        self.t_stream_one(surface)
        self.t_stream_two(surface)
        self.t_patron.update(surface)
        surface.blit(self.boss_stay[0], self.boss_stay[1])
        self.burning_rect(surface)

    def t_stream_one(self, surface):
        time = self.t_timer1.get_time()
        for turtle in self.turtles1:
            if time < 10.5:
                turtle.moving(ct_size*17)
            else:
                self.came = True
            turtle.update(surface)

    def t_stream_two(self, surface):
        time = self.t_timer2.get_time()
        for turtle in self.turtles2:
            if time < 5.5:
                turtle.moving(ct_wndSize[0]-ct_size*13)
            turtle.update(surface)

    def place_one(self, surface):
        for block in self.ground1:
            block.update(surface)
        for tree in self.apple_trees:
            tree.update(surface)

    def burning_rect(self, surface):
        time = self.timer_rect.get_time()
        self.timer_rect.restart()
        speed = ct_size * time * 2
        self.rect.height -= speed
        self.rect.draw(surface)
        for bonfire in self.fire:
            bonfire.rect.top = self.rect.top + self.rect.height-ct_size
            bonfire.update(surface)

    def __del__(self):
        pass
