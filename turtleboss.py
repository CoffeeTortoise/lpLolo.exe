from turtlepaths import tp_boss_hand, tp_boss_prayer, tp_boss_portal
from turtlepaths import tp_boss_stay, tp_boss_step1, tp_boss_step2
from turtlepaths import tp_tp_snd
from constants import ct_frT, ct_size
from animator import Animator
from monster import Monster
from timer import Timer
import pygame as pg


class TBoss(Monster):
    def __init__(self, m_speed, m_jump, width, height, hp, attack, pos):
        super().__init__(m_speed, m_jump, width, height, hp, attack)
        paths = [tp_boss_stay, tp_boss_step1, tp_boss_step2]
        origs = []
        for dirs in paths:
            image = pg.image.load(dirs).convert_alpha()
            origs.append(image)
        self.frames_r = []
        for image in origs:
            sprite = pg.transform.scale(image, (width, height))
            self.frames_r.append(sprite)
        self.frames_l = []
        for sprite in self.frames_r:
            flip = pg.transform.flip(sprite, True, False)
            self.frames_l.append(flip)
        or_hand = pg.image.load(tp_boss_hand).convert_alpha()
        or_prayer = pg.image.load(tp_boss_prayer).convert_alpha()
        or_portal = pg.image.load(tp_boss_portal).convert_alpha()
        self.hand_r = pg.transform.scale(or_hand, (width*1.3, height))
        self.hand_l = pg.transform.flip(self.hand_r, True, False)
        self.prayer = pg.transform.scale(or_prayer, (width*2, height))
        self.portal = pg.transform.scale(or_portal, (width*.5, height*2))
        self.tp_rect = self.portal.get_rect()
        self.tp_rect.left, self.tp_rect.top = pos[0], pos[1]
        self.animate_r = Animator(self.frames_r, ct_frT)
        self.animate_l = Animator(self.frames_l, ct_frT)
        self.image = self.frames_r[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos[0], pos[1]
        self.width, self.height = width, height
        self.timer_run = Timer()
        self.timer_up = Timer()
        self.block = False
        self.sound = pg.mixer.Sound(tp_tp_snd)

    def update(self, surface):
        if self.alive:
            self.define_pos()
            if not self.block:
                self.define_right()
                self.animate()
            self.speed, self.jump = 0, 0
            surface.blit(self.image, self.rect)
            if self.block:
                surface.blit(self.portal, self.tp_rect)
            if self.hp <= 0:
                self.alive = False

    def defend(self, penguin):
        pos_x, pos_y = self.rect.left, self.rect.top
        self.right = True if (pos_x-penguin.rect.left < 0) else False
        self.tp_rect.top = pos_y-ct_size
        self.block = False
        if penguin.bullet.exist:
            self.block = True
            if self.right:
                self.tp_rect.left = pos_x+self.width*2
                self.image = self.hand_r
            else:
                self.tp_rect.left = pos_x-self.width
                self.image = self.hand_l
            if self.tp_rect.colliderect(penguin.bullet.rect) and self.block:
                self.sound.play()
                penguin.bullet.exist = False
                self.block = False
        else:
            self.block = False
            self.tp_rect.left = pos_x
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos_x, pos_y
        return penguin

    def __del__(self):
        pass
