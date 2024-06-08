from constants import ct_fnt_size, ct_fnt_path, ct_size, ct_malachite, ct_black
from stage import Stage
from timer import Timer
from sys import exit
import pygame as pg


class StageSix(Stage):
    def __init__(self, surface, penguin):
        super().__init__(surface, penguin)
        self.font1 = pg.font.Font(ct_fnt_path, ct_fnt_size*4)
        self.font2 = pg.font.Font(ct_fnt_path, ct_fnt_size*5)
        text1 = 'To be continued...' if (self.ru == 0) else 'Продолжение следует'
        text2 = '?'
        text3 = 'Depend\'s on you' if (self.ru == 0) else 'Зависит от вас'
        x1, x2, x3 = ct_size*4, ct_size*35, ct_size*6
        y1, y2, y3 = ct_size*4, ct_size*8, ct_size*12
        self.pos1, self.pos2, self.pos3 = (x1, y1), (x2, y2), (x3, y3)
        self.text1 = self.font1.render(text1, 1, ct_malachite)
        self.text2 = self.font2.render(text2, 1, ct_malachite)
        self.text3 = self.font1.render(text3, 1, ct_malachite)
        self.timer = Timer()

    def behaviour(self):
        self.surface.fill(ct_black)
        time = self.timer.get_time()
        self.surface.blit(self.text1, self.pos1)
        if time >= 1:
            self.surface.blit(self.text2, self.pos2)
        if time >= 2:
            self.surface.blit(self.text3, self.pos3)
        if time >= 3:
            exit(0)

    def refresh(self):
        self.refresh_data()
        text1 = 'To be continued...' if (self.ru == 0) else 'Продолжение следует'
        text2 = '?'
        text3 = 'Depend\'s on you' if (self.ru == 0) else 'Зависит от вас'
        x1, x2, x3 = ct_size, ct_size * 3, ct_size * 6
        y1, y2, y3 = ct_size * 4, ct_size * 8, ct_size * 12
        self.pos1, self.pos2, self.pos3 = (x1, y1), (x2, y2), (x3, y3)
        self.text1 = self.font1.render(text1, 1, ct_malachite)
        self.text2 = self.font2.render(text2, 1, ct_malachite)
        self.text3 = self.font1.render(text3, 1, ct_malachite)

    def __del__(self):
        pass
