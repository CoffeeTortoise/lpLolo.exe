from blockpaths import bs_gray25_block, bs_col_laser_snd, bs_bld_puddle
from bgpaths import bp_spikes, bp_dstone, bp_crystal
from constants import ct_size, ct_wndSize
from solidblocks import SolidBlock, Spike
from torturepaths import ts_var8, ts_var9
from lizarddemon import LizardDemon
from lizardspaths import lp_death2
from layoutsone import ls1_ground
from baseclasses import Block
from stage import Stage
from sys import exit
from egg import Egg


class StageFour(Stage):
    def __init__(self, surface, penguin):
        super().__init__(surface, penguin)
        self.r_pos = (ct_size * 39, ct_wndSize[1] - ct_size * 8)
        for row_index, row in enumerate(ls1_ground):
            for col_index, cell in enumerate(row):
                if (cell == 'G') or (cell == 'D'):
                    x, y = col_index * ct_size, row_index * ct_size
                    block = SolidBlock(ct_size, ct_size, (x, y),
                                       bs_gray25_block, True, bs_col_laser_snd)
                    self.ground.append(block)
                else:
                    continue
        self.spikes = []
        s_w, s_h = ct_size*6, ct_size*3
        s_x, s_y = ct_wndSize[0]-ct_size*21, ct_wndSize[1]-ct_size*6
        for i in range(2):
            x = s_x + s_w*i
            spike = Spike(s_w, s_h, (x, s_y), bp_spikes, True, bs_col_laser_snd)
            self.spikes.append(spike)
        l_w, l_h = ct_size*2.5, ct_size*3
        l_x, l_y = s_x - ct_size*10, ct_wndSize[1]
        speed, jump = ct_size*13, ct_size*300
        self.lizard_d = LizardDemon(speed, jump, l_w, l_h, 333, 333,
                                    (l_x, l_y), self.surface)
        cr_w, cr_h = ct_size*3, ct_size*2
        cr_x, cr_y = 0, ct_wndSize[1]-ct_size*5
        for i in range(6):
            x = cr_x + cr_w*i
            crystal = Block(cr_w, cr_h, (x, cr_y), bp_crystal)
            self.phone.append(crystal)
        p_w1, p_w2, p_h = ct_size*1.5, ct_size, ct_size
        p_x1, p_x2, p_y = ct_size*10, ct_size*13, ct_wndSize[1]-ct_size*4
        up_part = Block(p_w1, p_h*1.2, (p_x1, p_y-p_h*.2), ts_var9)
        down_part = Block(p_w2, p_h, (p_x2, p_y), ts_var8)
        pl_w, pl_h = ct_size*1.5, ct_size*.4
        pl_x, pl_y = ct_size*8, ct_wndSize[1]-ct_size*3
        self.phone.append(up_part)
        self.phone.append(down_part)
        for i in range(7):
            x = pl_x + pl_w*i*.8
            puddle = Block(pl_w, pl_h, (x, pl_y), bs_bld_puddle)
            self.phone.append(puddle)
        d_w, d_h = ct_size*6, ct_size*7
        d_x, d_y = ct_size*20, ct_wndSize[1]-ct_size*11
        stone = Block(d_w, d_h, (d_x, d_y), bp_dstone)
        self.phone.append(stone)
        eg_w, eg_h = ct_size * 15, ct_size * 15
        eg_x, eg_y = ct_size * 17, ct_size
        self.egg = Egg(eg_w, eg_h, (eg_x, eg_y))
        dl_w, dl_h = ct_size*2.5, ct_size
        dl_x, dl_y = ct_size*7, ct_wndSize[1]-ct_size*4
        self.dead_l = Block(dl_w, dl_h, (dl_x, dl_y), lp_death2)
        self.busy, self.liz_app = True, False

    def behaviour(self):
        if self.active:
            if self.penguin.alive:
                self.mainloop()

    def mainloop(self):
        self.refresh_data()
        self.place()
        self.set_background()
        self.set_spikes()
        self.p_pos = self.penguin.rect.left
        self.points()
        self.collide_place()
        self.lizard_attack()
        self.cond_end()
        if self.penguin.hp <= 0:
            self.penguin.alive = False
        if not self.penguin.alive:
            exit(1)

    def set_spikes(self):
        for spike in self.spikes:
            spike.update(self.surface)
            self.penguin = spike.react(self.penguin, self.spikes)
            self.penguin = spike.hit_penguin(self.penguin)
            self.penguin.bullet = spike.collide_ammo(self.penguin.bullet)

    def lizard_attack(self):
        self.fix_lizard()
        if self.lizard_d.alive:
            self.egg.update(self.surface)
            self.lizard_d.update(self.surface)
            self.lizard_d.greeting()
            self.penguin_gotcha()
            self.lizard_d.attack_penguin(self.penguin)
            self.penguin.bullet = self.lizard_d.collide_bullet(self.penguin.bullet)
        else:
            self.dead_l.update(self.surface)
            self.mute_level = False
            self.penguin_stopped = False

    def penguin_gotcha(self):
        penguin, lizard = self.penguin.rect, self.lizard_d.rect
        if penguin.colliderect(lizard):
            self.mute_level = True
            self.penguin_stopped = True
        else:
            self.mute_level = False
            self.penguin_stopped = False

    def fix_lizard(self):
        if not self.liz_app:
            l_x, l_y = ct_size * 16, ct_wndSize[1] - ct_size*6
            self.lizard_d.pos = l_x, l_y
            self.liz_app = True

    def cond_end(self):
        if self.p_pos >= ct_size*35:
            self.finished = True

    def __del__(self):
        pass
