from demonspaths import dp_p_step1, dp_p_step2, dp_p_step3, dp_p_step4
from animator import Animator
from constants import ct_frT
from monster import Monster
from timer import Timer
import pygame as pg


class Patrick(Monster):
    def __init__(self, m_speed, m_jump, width, height, hp, attack, pos):
        super().__init__(m_speed, m_jump, width, height, hp, attack)
        dirs = [dp_p_step1, dp_p_step2, dp_p_step3, dp_p_step4]
        origs = []
        for path in dirs:
            raw = pg.image.load(path).convert_alpha()
            origs.append(raw)
        self.frames_r = []
        for image in origs:
            sprite = pg.transform.scale(image, (width, height))
            self.frames_r.append(sprite)
        self.frames_l = []
        for sprite in self.frames_r:
            flipped = pg.transform.flip(sprite, True, False)
            self.frames_l.append(flipped)
        self.animate_r = Animator(self.frames_r, ct_frT)
        self.animate_l = Animator(self.frames_l, ct_frT)
        self.image = self.frames_r[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos[0], pos[1]
        self.width, self.height = width, height
        self.timer_atck = Timer()

    def attacking(self, penguin):
        time = self.timer_atck.get_time()
        self.timer_atck.restart()
        if penguin.rect.colliderect(self.rect):
            penguin.hp -= time
        if penguin.bullet.rect.colliderect(self.rect) and penguin.bullet.exist:
            self.hp -= penguin.attack
            if self.hp <= 0:
                self.alive = False
            penguin.bullet.exist = False
        return penguin

    def __del__(self):
        pass
