from penguinpaths import ps_stay, ps_step1, ps_step2
from characters import Shooter
from animator import Animator
from constants import ct_frT
from timer import Timer
import pygame as pg


class Penguin(Shooter):
    def __init__(self, m_speed, m_jump, width, height, hp, attack, pos, ammo_path,
                 ammo_w, ammo_h, snd_path):
        super().__init__(m_speed, m_jump, width, height, hp, attack, pos, ammo_path,
                         ammo_w, ammo_h, snd_path)
        paths = [ps_stay, ps_step1, ps_step2]
        raws = []
        for pth in paths:
            image = pg.image.load(pth).convert_alpha()
            raws.append(image)
        self.frames_r = []
        for img in raws:
            sprite = pg.transform.scale(img, (self.width, self.height))
            self.frames_r.append(sprite)
        self.frames_l = []
        for sprite in self.frames_r:
            flipped = pg.transform.flip(sprite, True, False)
            self.frames_l.append(flipped)
        self.animator_r = Animator(self.frames_r, ct_frT)
        self.animator_l = Animator(self.frames_l, ct_frT)
        self.input = False
        self.onGround = False
        self.mg = self.m_jump/30
        self.image = self.frames_r[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos[0], pos[1]
        self.timer_jump = Timer()
        self.timer_fall = Timer()

    def update(self, surface, begin, end, top):
        self.speed, self.jump = 0, 0
        self.input, self.fire = False, False
        self.moving()
        self.animator()
        self.gravity()
        self.jumping()
        self.shooting(surface)
        self.hor_bounds(begin, end)
        self.vert_bounds(top)
        self.rect.move_ip(self.speed, self.jump)
        surface.blit(self.image, self.rect)

    def moving(self):
        keys = pg.key.get_pressed()
        time = self.timer.get_time()
        self.timer.restart()
        if self.movable:
            if keys[pg.K_RIGHT]:
                self.speed = self.m_speed * time
                self.right = True
                self.input = True
            if keys[pg.K_LEFT]:
                self.speed = -self.m_speed * time
                self.right = False
                self.input = True

    def jumping(self):
        keys = pg.key.get_pressed()
        time = self.timer_jump.get_time()
        self.timer_jump.restart()
        if keys[pg.K_UP] and self.movable:
            if self.onGround:
                self.jump = -self.m_jump*time
                self.onGround = False

    def shooting(self, surface):
        keys = pg.key.get_pressed()
        if not self.bullet.exist:
            self.bullet.rect.left = self.rect.left
            self.bullet.rect.top = self.rect.top
        if keys[pg.K_SPACE] and self.movable:
            self.fire = True
        super().shoot(surface)

    def gravity(self):
        time = self.timer_fall.get_time()
        self.timer_fall.restart()
        if not self.onGround and self.movable:
            self.jump = self.mg*time

    def animator(self):
        if self.input:
            if self.right:
                self.image = self.animator_r.animate()
            else:
                self.image = self.animator_l.animate()
        else:
            if self.right:
                self.image = self.frames_r[0]
            else:
                self.image = self.frames_l[0]

    def hor_bounds(self, begin, end):
        pos_x = self.rect.left + self.speed
        if pos_x <= begin:
            self.rect.left -= self.speed
            self.speed = 0
        if pos_x >= end:
            self.rect.left -= self.speed
            self.speed = 0

    def vert_bounds(self, top):
        pos_y = self.rect.top + self.jump
        if pos_y < top:
            self.rect.top -= self.jump
            self.jump = 0

    def __del__(self):
        pass
