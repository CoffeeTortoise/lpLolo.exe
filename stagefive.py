from blockpaths import bs_gray25_block, bs_col_laser_snd
from constants import ct_size, ct_wndSize, ct_orchid
from kingpatrick import KingPatrick
from solidblocks import SolidBlock
from layoutsone import ls1_bridge
from hellisheye import HellishEye
from stagesix import StageSix
from patrick import Patrick
from stage import Stage
from timer import Timer
from sys import exit


class StageFive(Stage):
    def __init__(self, surface, penguin):
        super().__init__(surface, penguin)
        self.l_pos = (ct_size * 7, ct_wndSize[1] - ct_size * 8)
        self.r_pos = (ct_size * 39, ct_wndSize[1] - ct_size * 8)
        self.busy = True
        text = 'Invasion!' if (self.ru == 0) else 'Вторжение!'
        self.text = self.font.render(text, 1, ct_orchid)
        t_x = ct_size*20 if (self.ru == 0) else ct_size*17
        t_y = ct_size*7
        self.t_pos = (t_x, t_y)
        for row_index, row in enumerate(ls1_bridge):
            for col_index, cell in enumerate(row):
                if cell == 'G':
                    x, y = col_index*ct_size, row_index*ct_size
                    block = SolidBlock(ct_size, ct_size, (x, y),
                                       bs_gray25_block, True, bs_col_laser_snd)
                    self.ground.append(block)
                else:
                    continue
        e_w, e_h = ct_size*4, ct_size*3
        e_x, e_y = ct_size*25, ct_size*7
        speed, jump, hp = ct_size*42, ct_size*250, 32
        self.eye = HellishEye(speed, jump, e_w, e_h, hp, 3, (e_x, e_y))
        self.eye.right, self.e_fixed = False, False
        self.hello, self.fight = False, False
        self.e_timer = Timer()
        pos = (-ct_size, ct_wndSize[1]+ct_size)
        self.timer_up, self.timer_ps = Timer(), Timer()
        self.king = KingPatrick(pos)
        pa_w, pa_h = ct_size*3, ct_size*6
        pa_x, pa_y = ct_size*60, ct_wndSize[1]-ct_size*11
        self.timer_down = Timer()
        self.patricks = []
        for i in range(13):
            x = pa_x + pa_w*i*3
            patrick = Patrick(ct_size*12, ct_size*300, pa_w, pa_h,
                              100, 33, (x, pa_y))
            self.patricks.append(patrick)
        self.stage = StageSix(self.surface, self.penguin)
        self.ending = False

    def behaviour(self):
        if self.penguin.alive and not self.ending:
            self.mainloop()
            self.end_cnt()
        else:
            self.stage.behaviour()

    def mainloop(self):
        self.fix_eye()
        self.refresh()
        self.boss()
        self.place()
        self.p_pos = self.penguin.rect.left
        self.collide_place()
        self.greet()
        self.cond_end()
        if self.penguin.hp <= 0:
            self.penguin.alive = False
        if not self.penguin.alive:
            exit(0)

    def boss(self):
        if self.hello:
            self.boss_up()
            self.king.update(self.surface)
            self.penguin = self.king.combat(self.penguin)
            if not self.king.alive:
                self.finished = True
                self.servants()
                time = self.timer_down.get_time()
                self.timer_down.restart()
                speed = time*ct_size*6
                left, top = self.king.pos
                self.king.pos = left, top+speed

    def servants(self):
        for patrick in self.patricks:
            if patrick.alive:
                self.penguin = patrick.attacking(self.penguin)
                patrick.moving(self.p_pos)
                patrick.update(self.surface)
            else:
                continue

    def boss_up(self):
        if not self.fight:
            left, top = self.king.pos
            if top >= ct_size * 5:
                time2 = self.timer_ps.get_time()
                self.timer_ps.restart()
                self.king.pos = left, top - time2 * ct_size * 12
            else:
                self.king.angry = True
                self.fight = True

    def greet(self):
        if not self.hello:
            self.penguin.movable = False
            time = self.e_timer.get_time()
            self.eye.update(self.surface)
            if time < 1.5:
                self.surface.blit(self.text, self.t_pos)
            elif (time >= 1.5) and (time < 3):
                self.eye.moving(ct_size*50)
            else:
                self.penguin.movable = True
                self.hello = True

    def fix_eye(self):
        if not self.e_fixed:
            self.eye.pos = ct_size*25, ct_size*7
            self.e_fixed = True

    def refresh(self):
        if not self.fresh:
            self.refresh_data()
            text = 'Invasion!' if (self.ru == 0) else 'Вторжение!'
            t_x = ct_size * 20 if (self.ru == 0) else ct_size * 17
            t_y = ct_size * 7
            self.t_pos = (t_x, t_y)
            self.text = self.font.render(text, 1, ct_orchid)

    def end_cnt(self):
        i = 0
        for patrick in self.patricks:
            if not patrick.alive:
                i += 1
        if i == len(self.patricks):
            self.ending = True

    def cond_end(self):
        if not self.king.alive:
            self.finished = True

    def __del__(self):
        pass
