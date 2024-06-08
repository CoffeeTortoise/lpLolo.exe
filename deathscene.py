from constants import ct_size, ct_wndSize, ct_white, ct_red, ct_carmine
from baseclasses import Block, ShortScene
from blockpaths import bs_ubuntu_logo
from lizardspaths import lp_boss_stay
from turtlepaths import tp_boss_stay
from constants import ct_scarlett
from penguinpaths import ps_face
from timer import Timer
import pygame as pg


class DeathScene(ShortScene):
    def __init__(self, surface):
        super().__init__(surface)
        p_x, p_y = ct_size * 23, ct_wndSize[1] - ct_size * 12.5
        p_w, p_h = ct_size * 2, ct_size * 3
        self.penguin = Block(p_w, p_h, (p_x, p_y), ps_face)
        txt1, txt2 = 'Use 1        for resurrection?', 'Y/N'
        if self.ru == 1:
            txt1 = 'Использовать 1        для воскрешения?'
        self.t_pos = (ct_size * 7, ct_wndSize[1] - ct_size * 6)
        self.text1 = self.base_fnt.render(txt1, 1, ct_red, ct_white)
        self.t2_pos = (ct_size * 36, ct_wndSize[1] - ct_size * 6)
        self.text2 = self.base_fnt.render(txt2, 1, ct_white, ct_scarlett)
        ub_w, ub_h = ct_size * 2, ct_size * 2
        ub_pos = (ct_size * 12.5, ct_wndSize[1] - ct_size * 6)
        self.ubuntu = Block(ub_w, ub_h, ub_pos, bs_ubuntu_logo)
        t_w, t_h = ct_size*3, ct_size*5
        t_x, t_y = ct_size*10, ct_wndSize[1]-ct_size*14.5
        self.turtle = Block(t_w, t_h, (t_x, t_y), tp_boss_stay)
        l_w, l_h = ct_size*4, ct_size*5
        l_x, l_y = ct_size*35, ct_wndSize[1]-ct_size*14.5
        self.lizard = Block(l_w, l_h, (l_x, l_y), lp_boss_stay)
        self.lizard.image = pg.transform.flip(self.lizard.image, True, False)
        self.state, self.defined = 0, False
        self.executed, self.merci = False, False
        self.timer_end = Timer()
        self.timer_mus, self.timer_glit = Timer(), Timer()
        self.time_mus_co = 8
        self.sound = None

    def refresh(self):
        if not self.fresh:
            self.refresh_data()
            txt1 = 'Use 1        for resurrection?'
            if self.ru == 1:
                self.t_pos = (ct_size * 6, ct_wndSize[1] - ct_size * 6)
                self.t2_pos = (ct_size * 41, ct_wndSize[1] - ct_size * 6)
                self.ubuntu.rect.left = ct_size*21
                txt1 = 'Использовать 1        для воскрешения?'
            self.text1 = self.base_fnt.render(txt1, 1, ct_red, ct_white)

    def start_mus(self):
        time = self.timer_mus.get_time()
        if ((time == 0) or (time >= self.time_mus_co)) and not self.executed:
            if not self.merci:
                self.sound.play()
                self.timer_mus.restart()

    def glitch(self):
        if not self.executed:
            time = self.timer_glit.get_time()
            if (time >= .5) and (time < 1.5):
                self.lil_screamer()
            if time >= 1.5:
                self.timer_glit.restart()
        else:
            self.lil_screamer()

    def lil_screamer(self):
        self.surface.fill(ct_carmine)
        self.turtle.update(self.surface)
        self.lizard.update(self.surface)

    def delay_executed(self):
        if self.executed:
            time = self.timer_end.get_time()
            if time >= 3:
                self.ended = True

    def choice(self):
        """Returns 0 if nothing happened, 1 if pressed Y, and 2 if N"""
        if not self.defined:
            self.state = 0
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_y:
                        self.state = 1
                        self.merci = True
                    elif event.key == pg.K_n:
                        self.state = 2
                    else:
                        self.state = 0
            if (self.state == 1) or (self.state == 2):
                self.defined = True
        return self.state

    def draw_opts(self):
        if not self.defined:
            self.surface.blit(self.text1, self.t_pos)
            self.surface.blit(self.text2, self.t2_pos)
            self.ubuntu.update(self.surface)

    def __del__(self):
        pass
