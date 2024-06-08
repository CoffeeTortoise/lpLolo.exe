from blockpaths import bs_stg1, bs_stg2, bs_stg3, bs_stg4, bs_stg5, bs_stg6
from blockpaths import bs_ice_block, bs_bld_stain1, bs_ubuntu_logo
from constants import ct_fps1, ct_size, ct_wndSize
from constants import ct_red, ct_white, ct_black
from constants import ct_fnt_path, ct_fnt_size
from torturepaths import ts_iglu, ts_var1
from othermuspaths import mu_intro_mus
from baseclasses import Block, Scene
from penguinpaths import ps_stay
from layoutsone import ls1_road
from glitter import Glitter
from timer import Timer
from fire import Fire
import pygame as pg


class Introduction(Scene):
    def __init__(self, surface):
        super().__init__(ct_fps1, surface)
        self.ground = []
        for row_index, row in enumerate(ls1_road):
            for col_index, cell in enumerate(row):
                if cell == 'G':
                    x = col_index*ct_size
                    y = row_index*ct_size
                    block = Block(ct_size, ct_size, (x, y), bs_ice_block)
                    self.ground.append(block)
        self.glitter = []
        top, bottom, begin, end = 0, ct_size*5, 0, ct_wndSize[0]
        len_glit, speed = 150, .5
        for i in range(len_glit):
            boost = speed + i/(len_glit*10)
            circle = Glitter(boost, ct_size, top, bottom, begin, end)
            self.glitter.append(circle)
        self.fire = []
        fire_paths = [bs_stg1, bs_stg2, bs_stg3, bs_stg4, bs_stg5, bs_stg6]
        beg_x, y = ct_size, ct_wndSize[1]-ct_size*4.5
        for i in range(20):
            x = beg_x + ct_size*i*2
            bonfire = Fire(fire_paths, ct_size*1.5, ct_size*1.5, (x, y))
            bonfire.sound_on = False
            self.fire.append(bonfire)
        self.blood = []
        for i in range(37):
            x = beg_x + ct_size*i*2
            puddle = Block(ct_size*3, ct_size*.5,
                           (x, y+ct_size*1.5), bs_bld_stain1)
            self.blood.append(puddle)
        self.iglu = Block(ct_size*11, ct_size*7,
                          (ct_size*34, y-ct_size*5.5), ts_iglu)
        self.deadman = Block(ct_size*2, ct_size*2,
                             (ct_size*33, y-ct_size*.25), ts_var1)
        self.penguin = Block(ct_size, ct_size*1.5,
                             (ct_size*15, y), ps_stay)
        self.ubuntu = Block(ct_size*2, ct_size*2,
                            (ct_size*15, y-ct_size*.5), bs_ubuntu_logo)
        self.timer = Timer()
        self.font = pg.font.Font(ct_fnt_path, ct_fnt_size)
        txt1 = 'What happened here?' if (self.ru == 0) else 'Что здесь произошло?'
        txt2 = 'Demons...' if (self.ru == 0) else 'Демоны...'
        txt3 = '...'
        self.t_pos1, self.t_pos2 = (ct_size*16, y-ct_size), (ct_size*30, y-ct_size)
        self.text1 = self.font.render(txt1, 1, ct_red)
        self.text2 = self.font.render(txt2, 1, ct_white)
        self.text3 = self.font.render(txt3, 1, ct_red)
        self.scened = False
        self.music = pg.mixer.music
        self.mus_path = mu_intro_mus

    def behaviour(self):
        self.start_mus()
        self.refresh_data()
        self.surface.fill(ct_black)
        self.drawings()
        self.tempo_draw()
        pg.display.flip()
        self.quit_opts()

    def refresh_data(self):
        if not self.got_data:
            self.get_data()
            txt1 = 'What happened here?' if (self.ru == 0) else 'Что здесь произошло?'
            txt2 = 'Demons...' if (self.ru == 0) else 'Демоны...'
            txt3 = '...'
            self.text1 = self.font.render(txt1, 1, ct_red)
            self.text2 = self.font.render(txt2, 1, ct_white)
            self.text3 = self.font.render(txt3, 1, ct_red)

    def drawings(self):
        for block in self.ground:
            self.surface.blit(block.image, block.rect)
        for circle in self.glitter:
            circle.behaviour(self.surface)
        for bonfire in self.fire:
            bonfire.update(self.surface)
        for puddle in self.blood:
            self.surface.blit(puddle.image, puddle.rect)
        self.surface.blit(self.iglu.image, self.iglu.rect)
        self.surface.blit(self.deadman.image, self.deadman.rect)
        self.penguin.update(self.surface)

    def tempo_draw(self):
        time = self.timer.get_time()
        if (time < 3) and not self.scened:
            self.surface.blit(self.text1, self.t_pos1)
        if ((time > 3) and (time < 6)) and not self.scened:
            self.surface.blit(self.text2, self.t_pos2)
        if (time > 6) and not self.scened:
            self.que = 2
            self.ended = True
        if self.scened:
            if time < 3:
                self.surface.blit(self.text3, self.t_pos1)
            if (time > 3) and (time < 9):
                self.ubuntu.update(self.surface)
            if time > 6:
                self.que = 4
                self.ended = True

    def __del__(self):
        pass
