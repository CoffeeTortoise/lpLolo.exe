from lizardspaths import lp_d_stay, lp_d_step1, lp_d_step2
from othersoundpaths import so_liz_hoy
from lizardfight import LizardFight
from animator import Animator
from constants import ct_frT
from lizard import Lizard
from sys import exit
import pygame as pg


class LizardDemon(Lizard):
    def __init__(self, m_speed, m_jump, width, height, hp, attack, pos, surf):
        super().__init__(m_speed, m_jump, width, height, hp, attack, pos, False)
        paths = [lp_d_stay, lp_d_step1, lp_d_step2]
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
            flipped = pg.transform.flip(sprite, True, False)
            self.frames_l.append(flipped)
        self.animate_r = Animator(self.frames_r, ct_frT)
        self.animate_l = Animator(self.frames_l, ct_frT)
        self.image = self.frames_r[0]
        self.rect = self.image.get_rect()
        self.hoy, self.sound = False, pg.mixer.Sound(so_liz_hoy)
        self.fight, self.res = LizardFight(surf), 0

    def greeting(self):
        if not self.hoy:
            self.sound.play()
            self.hoy = True

    def attack_penguin(self, penguin):
        if self.alive:
            pos = penguin.pos[0]
            self.moving(pos)
            if self.rect.colliderect(penguin.rect):
                self.fight.behaviour()
                self.res = self.fight.choice()
                self.summarize_attack()

    def collide_bullet(self, bullet):
        if self.rect.colliderect(bullet.rect):
            bullet.exist = False
        return bullet

    def summarize_attack(self):
        if self.res == 2:
            exit(0)
        elif self.res == 1:
            self.alive = False
        else:
            pass

    def __del__(self):
        pass
