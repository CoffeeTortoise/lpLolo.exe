from blockpaths import bs_masher_col, bs_col_block_bl_snd
from blockpaths import bs_gray25_block, bs_col_laser_snd
from constants import ct_size, ct_wndSize, ct_red
from solidblocks import SolidBlock, Masher
from circleentity import CircleEntity
from demonicslug import DemonicSlug
from bgpaths import bp_cryst_tree
from torturepaths import ts_var2
from layoutsone import ls1_road
from baseclasses import Block
from crush import Crush
from timer import Timer
from stage import Stage


class StageTwo(Stage):
    def __init__(self, surface, penguin):
        super().__init__(surface, penguin)
        for row_index, row in enumerate(ls1_road):
            for col_index, cell in enumerate(row):
                x, y = col_index*ct_size, row_index*ct_size
                if cell == 'G':
                    block = SolidBlock(ct_size, ct_size, (x, y), bs_gray25_block,
                                       True, bs_col_laser_snd)
                    self.ground.append(block)
        self.masher = []
        for i in range(10):
            x = ct_size*10 + ct_size*i*3
            masher = Masher(ct_size * 3, ct_size * 5, (x, 0),
                            bs_masher_col, True, bs_col_laser_snd,
                            ct_size * 10, ct_size, ct_wndSize[1] - ct_size * 7,
                            bs_col_block_bl_snd, True)
            masher.active = False
            self.masher.append(masher)
        bg_x, bg_y = -ct_size, ct_wndSize[1]-ct_size*17
        bg_w, bg_h = ct_size*6, ct_size*15
        for i in range(7):
            x = bg_x + (bg_w + ct_size*2)*i
            tree = Block(bg_w, bg_h, (x, bg_y), bp_cryst_tree)
            self.phone.append(tree)
        vic_x, vic_y = -ct_size + bg_w*.4, ct_wndSize[1]-ct_size*7
        vic_w, vic_h = ct_size*1.5, ct_size*2
        for i in range(7):
            x = vic_x + (bg_w + ct_size*2)*i
            victim = Block(vic_w, vic_h, (x, vic_y), ts_var2)
            self.phone.append(victim)
        self.mash_timer = Timer()
        self.crush = Crush(self.surface)
        sl_w, sl_h = ct_size, ct_size*3
        self.slug_x, slug_y = ct_wndSize[0]+ct_size*5, ct_size*5
        self.slug = DemonicSlug(ct_size*13, ct_size*300, sl_w, sl_h, 13, 13,
                                (self.slug_x, slug_y))
        self.slug_timer = Timer()
        c_x, c_y, c_r = ct_size*24, ct_size*6, ct_size*6
        self.circle = CircleEntity(c_r, ct_red, (c_x, c_y))
        self.busy, self.masher_loaded = True, False

    def behaviour(self):
        if self.active:
            if self.penguin.alive:
                self.mainloop()
            else:
                self.dead_loop()

    def mainloop(self):
        if not self.masher_loaded:
            self.reload_mash()
            self.masher_loaded = True
        self.refresh_data()
        self.set_background()
        self.slug_fly()
        self.collide_masher()
        self.place()
        self.p_pos = self.penguin.rect.left
        self.points()
        self.collide_place()
        self.define_finish()

    def define_finish(self):
        pos = self.penguin.rect.left
        x = pos if self.penguin.right else (pos + self.penguin.width)
        if x >= ct_size*30:
            self.finished = True

    def set_background(self):
        self.circle.draw(self.surface)
        super().set_background()

    def dead_loop(self):
        self.crush.behaviour()
        self.busy = True
        self.state = self.crush.choice()
        if self.state == 1:
            self.reload_mash()
            self.crush.defined = False
            self.penguin.alive = True
            self.crush.state = 0
        elif self.state == 2:
            self.dead = self.crush.ended

    def slug_fly(self):
        time = self.slug_timer.get_time()
        if time <= 6:
            self.slug.moving(-ct_size*3)
        else:
            self.slug.rect.left = self.slug_x
            self.slug_timer.restart()
        self.slug.update(self.surface)

    def reload_mash(self):
        self.mash_timer.restart()
        for i, masher in enumerate(self.masher):
            x = ct_size * 10 + ct_size * i * 3
            masher.rect.left, masher.rect.top = x, 0
            masher.active = False

    def collide_masher(self):
        time = self.mash_timer.get_time()
        for i, masher in enumerate(self.masher):
            if time > i:
                masher.active = True
            if self.penguin.movable:
                masher.on = True
            else:
                masher.on = False
            masher.rect.clamp_ip(self.surface.get_rect())
            self.penguin = masher.react(self.penguin, self.masher)
            self.penguin = masher.kill_penguin(self.penguin)
            self.penguin.bullet = masher.collide_ammo(self.penguin.bullet)
            masher.update(self.surface)

    def __del__(self):
        pass
