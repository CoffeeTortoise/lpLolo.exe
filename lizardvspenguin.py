from constants import ct_size, ct_wndSize, ct_black, ct_white, ct_warning
from lizardspaths import lp_death1, lp_death2, lp_wait, lp_pushing
from lizardspaths import lp_pdeath1, lp_pdeath2
from othersoundpaths import so_explosion, so_liz_eat, so_scary
from baseclasses import Block, ScreamScene
from othermuspaths import mu_drum, mu_sad
from blockpaths import bs_yellow_block
from circleentity import CircleEntity
from rectentity import RectEntity
from penguinpaths import ps_stay
from timer import Timer
import pygame as pg


class LizardBattle(ScreamScene):
    def __init__(self, surface):
        super().__init__(surface)
        p_w, p_h = ct_size * 4, ct_size * 6
        p_x, p_y = ct_size * 12, ct_wndSize[1] - ct_size * 13
        self.penguin = Block(p_w, p_h, (p_x, p_y), ps_stay)
        l_w, l_h = ct_size * 10, ct_size * 12
        l_x, l_y = ct_size * 21, ct_wndSize[1] - ct_size * 19
        self.l_pushing = Block(l_w, l_h, (l_x, l_y), lp_pushing)
        w_w, w_h = ct_size * 2, ct_size * 13
        w_x, w_y = l_x - w_w * .9, l_y - ct_size
        self.wall = Block(w_w, w_h, (w_x, w_y), bs_yellow_block)
        c_x, c_y, c_rad = ct_wndSize[0] * .5, ct_wndSize[1] - ct_size * 6, ct_wndSize[0] * .4
        self.circle = CircleEntity(c_rad, ct_white, (c_x, c_y))
        r_x, r_y = -ct_size, ct_wndSize[1] - ct_size * 7
        r_w, r_h = ct_wndSize[0] + ct_size * 3, ct_size * 5
        self.rect = RectEntity(r_w, r_h, ct_black, r_x, r_y)

    def __del__(self):
        pass


class PenguinWin(LizardBattle):
    def __init__(self, surface):
        super().__init__(surface)
        l_w, l_h = ct_size * 10, ct_size * 12
        l_x, l_tar, l_y = ct_size * 21, ct_size * 32, ct_wndSize[1] - ct_size * 19
        p_x, p_y = ct_size * 12, ct_wndSize[1] - ct_size * 13
        self.l_wait = Block(l_w, l_h, (l_tar, l_y), lp_wait)
        self.l_death1 = Block(l_w, l_h*.5, (l_tar, l_y + l_h*.5), lp_death1)
        self.l_death2 = Block(l_w*1.2, l_h*.25, (l_tar, l_y + l_h*.75), lp_death2)
        b_x, b_y, b_r = p_x + ct_size*8, p_y - ct_size*4, ct_size*.5
        self.bullet = CircleEntity(b_r, ct_warning, (b_x, b_y))
        self.timer_w, self.timer_l, self.timer_s = Timer(), Timer(), Timer()
        self.timer_fall, self.sound = Timer(), pg.mixer.Sound(mu_drum)
        self.time_period = 110
        self.pushed, self.l_dead, self.charged = False, False, False
        self.exploded = False
        self.explosion = pg.mixer.Sound(so_explosion)

    def behaviour(self):
        if not self.ended:
            self.play_mus()
            self.push_wall()
            self.pin_wall_to_lizard()
            self.drawings()
        else:
            self.set_mute()

    def set_mute(self):
        if not self.mute:
            self.sound.stop()
            self.mute = True

    def drawings(self):
        self.surface.fill(ct_black)
        self.circle.draw(self.surface)
        self.rect.draw(self.surface)
        self.penguin.update(self.surface)
        self.timed_draw()

    def timed_draw(self):
        self.part_one()
        self.part_two()
        self.part_three()

    def part_one(self):
        if not self.pushed:
            self.l_pushing.update(self.surface)
            self.wall.update(self.surface)

    def part_two(self):
        if self.pushed and not self.l_dead:
            self.l_wait.update(self.surface)
            self.shoot_bullet()
            self.bullet.draw(self.surface)

    def part_three(self):
        if self.l_dead:
            time = self.timer_fall.get_time()
            if time < 2:
                self.l_death1.update(self.surface)
            elif (time > 2) and (time < 5):
                self.l_death2.update(self.surface)
            else:
                self.ended = True

    def shoot_bullet(self):
        if not self.charged:
            time, rad = self.timer_l.get_time(), self.bullet.radius
            self.bullet.radius += time
            if rad >= ct_size*5:
                self.charged = True
        else:
            time, x = self.timer_s.get_time(), self.bullet.center[0]
            self.timer_s.restart()
            speed, y = ct_size*time*36, self.bullet.center[1]
            self.bullet.center = (x + speed, y)
            if x >= ct_size*35:
                self.l_dead = True
                self.boom()

    def boom(self):
        if not self.exploded:
            self.explosion.play()
            self.exploded = True

    def push_wall(self):
        time = self.timer_w.get_time()
        self.timer_w.restart()
        speed, x_w = ct_size*time*24, self.wall.rect.left
        if x_w <= ct_size*30:
            self.wall.rect.move_ip(speed, 0)
        else:
            self.pushed = True

    def pin_wall_to_lizard(self):
        x_w, w_w = self.wall.rect.left, self.wall.rect.width
        self.l_pushing.rect.left = x_w + w_w

    def __del__(self):
        pass


class LizardWin(LizardBattle):
    def __init__(self, surface):
        super().__init__(surface)
        l_w, l_h = self.l_pushing.width*1.25, self.l_pushing.height
        l_x, l_y = self.l_pushing.rect.left-ct_size*2, self.l_pushing.rect.top
        self.killer = Block(l_w, l_h, (l_x, l_y), lp_pdeath1)
        k_w, k_h = ct_wndSize
        k_x, k_y = -ct_size, -ct_size
        self.l_killer = Block(k_w, k_h, (k_x, k_y), lp_pdeath2)
        self.time_a, self.killed = Timer(), False
        self.eat, self.ate = pg.mixer.Sound(so_liz_eat), False
        self.scary, self.scared = pg.mixer.Sound(so_scary), False
        self.sound, self.time_period = pg.mixer.Sound(mu_sad), 60

    def behaviour(self):
        if not self.ended:
            self.play_mus()
            self.drawings()

    def drawings(self):
        self.surface.fill(ct_black)
        if not self.killed:
            self.circle.draw(self.surface)
            self.rect.draw(self.surface)
        self.timed_draw()

    def timed_draw(self):
        time = self.time_a.get_time()
        if time < 2:
            self.act_one()
        elif (time >= 2) and (time < 4):
            self.act_two()
        elif (time >= 4) and (time < 6):
            self.act_three()
        elif (time >= 6) and (time < 15):
            if not self.ate:
                self.eat.play()
                self.ate = True
        else:
            self.eat.stop()
            self.scary.stop()
            self.ended = True

    def act_one(self):
        self.penguin.update(self.surface)
        self.wall.update(self.surface)
        self.l_pushing.update(self.surface)

    def act_two(self):
        if not self.scared:
            self.scary.play()
            self.scared = True
        self.killer.update(self.surface)

    def act_three(self):
        self.surface.fill(ct_white)
        self.sound.stop()
        self.killed = True
        self.l_killer.update(self.surface)

    def __del__(self):
        pass
