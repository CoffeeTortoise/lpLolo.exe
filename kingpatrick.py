from demonspaths import dp_p_stg1, dp_p_stg2, dp_p_stg3, dp_p_stg4, dp_p_stg5, dp_p_stg6
from demonspaths import dp_p_hand, dp_p_breath
from constants import ct_size, ct_wndSize
from animatedblock import AnimatedBlock
from baseclasses import Block
from starbar import StarBar
from timer import Timer
import pygame as pg


class KingPatrick:
    def __init__(self, pos):
        body_paths = [dp_p_stg1, dp_p_stg2, dp_p_stg3, dp_p_stg4, dp_p_stg5, dp_p_stg6]
        self.width, self.height = ct_wndSize
        self.body = AnimatedBlock(self.width, self.height, pos, body_paths)
        self.alive, self.angry, self.breathed = True, False, False
        self.hand_on1, self.hand_on2 = False, False
        h_w, h_h = ct_size*30, ct_size*8
        h_x1, h_x2, h_y = -ct_size*30, ct_size*40, ct_wndSize[1]-ct_size*12
        self.hand1 = Block(h_w, h_h, (h_x1, h_y), dp_p_hand)
        self.hand1.image = pg.transform.flip(self.hand1.image, True, False)
        self.hand2 = Block(h_w, h_h, (h_x2, h_y), dp_p_hand)
        self.breath, self.time = pg.mixer.Sound(dp_p_breath), 50
        self.timer_snd, self.timer_speed = Timer(), Timer()
        self.timer_go, self.timer_atck = Timer(), Timer()
        self.timer_hit = Timer()
        self.hp, self.max_hp = 3000, 3000
        b_x, b_y = ct_size*30, ct_size*3
        self.bar = StarBar((b_x, b_y))

    def update(self, surface):
        self.body.update(surface)
        if self.alive:
            self.breathing()
            self.my_bar(surface)
            if self.angry:
                self.attack(surface)

    def my_bar(self, surface):
        k = self.hp*1./self.max_hp
        self.bar.show_hp(k, surface)

    def combat(self, penguin):
        if self.alive:
            time = self.timer_hit.get_time()
            self.timer_hit.restart()
            bullet = penguin.bullet
            collision1 = penguin.rect.colliderect(self.hand1.rect) and self.hand_on1
            collision2 = penguin.rect.colliderect(self.hand2.rect) and self.hand_on2
            if bullet.exist:
                hit1 = bullet.rect.colliderect(self.hand1.rect) and self.hand_on1
                hit2 = bullet.rect.colliderect(self.hand2.rect) and self.hand_on2
                if hit1 or hit2:
                    self.hp -= penguin.attack
                    if self.hp <= 0:
                        self.alive = False
                    penguin.bullet.exist = False
            if collision1 or collision2:
                penguin.hp -= time*3
        return penguin

    def attack(self, surface):
        time = self.timer_atck.get_time()
        if (time > 1) and (time < 3):
            self.hand_on1 = True
            self.hand_on2 = False
            self.hand_atck(self.hand1, 0)
            self.hand1.update(surface)
        elif (time >= 3) and (time < 5):
            self.hand_on1 = False
            self.hand_on2 = True
            self.hand_atck(self.hand2, 1)
            self.hand2.update(surface)
        elif time >= 5:
            self.hand_on1 = False
            self.hand_on2 = False
            self.timer_atck.restart()

    def hand_atck(self, hand, num):
        time, go = self.timer_speed.get_time(), self.timer_go.get_time()
        self.timer_speed.restart()
        speed = time * ct_size*24
        speed = speed if (num == 0) else -speed
        if go < 1:
            hand.rect.move_ip(speed, 0)
        elif (go >= 1) and (go < 2):
            hand.rect.move_ip(-speed, 0)
        else:
            self.timer_go.restart()

    def breathing(self):
        time = self.timer_snd.get_time()
        if not self.breathed:
            self.breath.play()
            self.breathed = True
        else:
            if time >= self.time:
                self.timer_snd.restart()
                self.breathed = False

    @property
    def pos(self):
        return self.body.pos

    @pos.setter
    def pos(self, new):
        self.body.pos = new

    def __del__(self):
        pass
