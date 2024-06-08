from constants import ct_size, ct_wndSize, ct_ru_path, ct_sulfur
from constants import ct_fnt_path, ct_fnt_size
from saveload import SaveLoad
import pygame as pg


# Use character and surface from level class, blocks only solid blocks
class Stage:
    def __init__(self, surface, penguin):
        self.ground, self.phone = [], []        # For background only blocks, not solid
        self.right, self.active = False, False
        self.first, self.last = True, False
        self.finished = False
        self.l_pos = (ct_size * 7, ct_wndSize[1] - ct_size * 6)
        self.r_pos = (ct_size * 39, ct_wndSize[1] - ct_size*6)
        self.ru = int(SaveLoad.load(ct_ru_path))
        self.font = pg.font.Font(ct_fnt_path, ct_fnt_size)
        self.penguin, self.surface = penguin, surface
        text = 'Enter' if (self.ru == 0) else 'Войти'
        self.msg = self.font.render(text, 1, ct_sulfur)
        self.can_cross, self.dead = False, False
        self.state = 0
        self.dir = 1    # 1 means current, 0 means previous, 2 means next
        self.p_pos = self.penguin.rect.left
        self.fresh, self.busy = False, False
        self.mute_level, self.penguin_stopped = False, False

    def refresh_data(self):
        if not self.fresh:
            if self.right:
                self.penguin.rect.left = self.r_pos[0]
                self.penguin.rect.top = self.r_pos[1]
            else:
                self.penguin.rect.left = self.l_pos[0]
                self.penguin.rect.top = self.l_pos[1]
            self.fresh = True

    def crossing(self):
        cond = 1
        if self.can_cross:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.can_cross = False
                        if self.dir == 0 and not self.first:
                            self.active = False
                            cond = 0
                        elif self.dir == 2 and not self.last:
                            self.active = False
                            cond = 2
                        else:
                            cond = 1
        return cond

    def points(self):
        self.dir = 1
        if self.finished:
            self.left_point()
            if not self.can_cross:
                self.right_point()
            self.show_msg()

    def show_msg(self):
        if self.can_cross:
            t_pos = (0, 0)
            cond = False
            if self.dir == 0:
                t_pos = (self.l_pos[0], self.l_pos[1] - self.penguin.height)
                cond = (not self.first)
            else:
                t_pos = (self.r_pos[0], self.r_pos[1] - self.penguin.height)
                cond = (not self.last)
            if cond:
                self.surface.blit(self.msg, t_pos)

    def right_point(self):
        border = (abs(self.p_pos - self.r_pos[0]) <= ct_size*5)
        if border:
            self.dir = 2
            self.can_cross = True
        else:
            self.can_cross = False

    def left_point(self):
        border = (abs(self.p_pos - self.l_pos[0]) <= ct_size*5)
        if border:
            self.dir = 0
            self.can_cross = True
        else:
            self.can_cross = False

    def collide_place(self):
        if not self.penguin_stopped:
            for block in self.ground:
                self.penguin = block.react(self.penguin, self.ground)
                self.penguin.bullet = block.collide_ammo(self.penguin.bullet)
            self.penguin.rect.clamp_ip(self.surface.get_rect())
            self.penguin.update(self.surface, ct_size * 5, ct_size * 43, 0)

    def set_background(self):
        for block in self.phone:
            block.update(self.surface)

    def place(self):
        for block in self.ground:
            block.update(self.surface)

    def __del__(self):
        pass
