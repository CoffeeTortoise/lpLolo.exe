from constants import ct_size, ct_wndSize, ct_black, ct_white
from blockpaths import bs_yel_brown_circle, bs_smash_snd
from blockpaths import bs_masher_col, bs_red_circle
from othermuspaths import mu_crash_death
from deathscene import DeathScene
from baseclasses import Block
from timer import Timer
import pygame as pg


class Crush(DeathScene):
    def __init__(self, surface):
        super().__init__(surface)
        c_x, c_y = ct_size*20.85, ct_wndSize[1]-ct_size*11
        c_w, c_h = ct_size*6.3, ct_size*3
        self.circle = Block(c_w, c_h, (c_x, c_y), bs_yel_brown_circle)
        self.red_puddle = Block(c_w, c_h, (c_x, c_y), bs_red_circle)
        self.surface2 = pg.surface.Surface((ct_size*6, ct_size*14.5))
        self.s_pos = (ct_size*21, 0)
        m_w, m_h = ct_size*6, ct_size*10
        m_x, m_y = ct_size*21, ct_wndSize[1]-ct_size*30
        self.masher = Block(m_w, m_h, (m_x, m_y), bs_masher_col)
        self.timer_mash = Timer()
        self.smash_snd = pg.mixer.Sound(bs_smash_snd)
        self.sound = pg.mixer.Sound(mu_crash_death)
        self.time_mus_co = 3

    def behaviour(self):
        if not self.ended:
            self.refresh()
            self.start_mus()
            self.drawings()

    def drawings(self):
        self.surface.fill(ct_black)
        self.glitch()
        self.surface2.fill(ct_white)
        self.surface.blit(self.surface2, self.s_pos)
        self.circle.update(self.surface)
        self.penguin.update(self.surface)
        self.draw_opts()
        self.execution()
        self.delay_executed()

    def execution(self):
        if self.state == 2:
            pos = self.masher.rect.top + self.masher.height
            target = ct_wndSize[1]-ct_size*12.5 + self.penguin.height
            time = self.timer_mash.get_time()
            self.timer_mash.restart()
            speed = ct_size*time*10
            if pos <= target:
                self.masher.rect.move_ip(0, speed)
            else:
                if not self.executed:
                    self.smash_snd.play()
                    self.executed = True
                self.red_puddle.update(self.surface)
        self.masher.update(self.surface)

    def __del__(self):
        pass
