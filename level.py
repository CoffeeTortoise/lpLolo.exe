from constants import ct_size, ct_wndSize, ct_fps2, ct_black
from penguinpaths import ps_bullet, ps_ammo_snd
from blockpaths import bs_ubuntu_logo
from healthbar import HealthBar
from baseclasses import Scene
from penguin import Penguin
from coinbar import CoinBar
import pygame as pg


# Use solid blocks as blocks
class Level(Scene):
    def __init__(self, surface):
        super().__init__(ct_fps2, surface)
        p_pos = (ct_size * 7, ct_wndSize[1] - ct_size * 6)
        self.health_bar = HealthBar((ct_size*5, ct_size*.5), self.surface)
        self.p_max_HP = 10
        self.coins = 0
        co_pos = (ct_size*15, ct_size*.5)
        self.coin_bar = CoinBar(ct_size, ct_size, co_pos, bs_ubuntu_logo,
                                self.coins, self.surface)
        self.penguin = Penguin(ct_size * 6, ct_size * 300, ct_size, ct_size * 1.5,
                               10, 10, p_pos,
                               ps_bullet, ct_size, ct_size, ps_ammo_snd)
        self.drips = []
        self.defined = False
        self.filled, self.resurrect = False, False
        self.paused, self.busy = False, False
        self.stages, self.state = [], 0

    def behaviour(self):
        self.get_data()
        self.define_stages()
        self.surface.fill(ct_black)
        self.draw_health()
        self.coin_bar.show_coins(self.coins)
        self.change_stage()
        pg.display.flip()
        self.quit_opts()

    def mus_stopper(self):
        for stage in self.stages:
            if stage.active:
                muting = stage.mute_level
                if muting:
                    self.music.stop()
                    self.on_mute = True
                else:
                    self.reload_mus()

    def reload_mus(self):
        if self.on_mute:
            self.music.play(-1)
            self.on_mute = False

    def stop_killed(self):
        if not self.penguin.alive:
            self.music.stop()
            self.music.unload()
            self.mus_on = False

    def draw_health(self):
        k = self.penguin.hp / self.p_max_HP
        self.health_bar.show_hp(k)

    def permanent_death(self):
        if self.coins < 0:
            self.ended = True

    def paralyze_penguin(self):
        self.penguin.onGround = True
        self.penguin.movable = False
        self.penguin.timer_up.restart()
        self.penguin.timer_run.restart()
        self.penguin.timer_fall.restart()
        self.penguin.timer_jump.restart()

    def put_penguin(self):
        for stage in self.stages:
            if stage.active:
                self.penguin = stage.penguin
                self.surface = stage.surface
            else:
                continue

    def transfer_penguin(self):
        for stage in self.stages:
            if stage.active:
                stage.penguin = self.penguin
                stage.surface = self.surface
            else:
                continue

    def define_stages(self):
        if not self.defined:
            for i, stage in enumerate(self.stages):
                if i == 0:
                    self.stages[i].active = True
                    self.stages[i].first = True
                    self.stages[i].last = False
                elif i == (len(self.stages) - 1):
                    self.stages[i].active = False
                    self.stages[i].first = False
                    self.stages[i].last = True
                else:
                    self.stages[i].active = False
                    self.stages[i].first = False
                    self.stages[i].last = False
            self.defined = True

    def change_stage(self):
        for i, stage in enumerate(self.stages):
            if self.stages[i].active:
                ab_coins = (self.coin_bar.coins >= self.coins)
                self.coins = self.coin_bar.coins if ab_coins else self.coins
                self.state = stage.state
                if self.state == 0:
                    self.resurrect = False
                elif self.state == 1:
                    if not self.resurrect:
                        self.state = 0
                        stage.state = 0
                        self.stages[i].penguin.alive = True
                        self.penguin.alive = True
                        self.coins -= 1
                        self.resurrect = True
                        self.stages[i].active = False
                        self.stages[0].active = True
                else:
                    self.ended = stage.dead
                self.penguin = self.stages[i].penguin
                self.surface = self.stages[i].surface
                self.busy = self.stages[i].busy
                self.stages[i].behaviour()
                stg_cond = self.stages[i].crossing()
                if stg_cond == 0:
                    if i <= 0:
                        self.ended = True
                    else:
                        self.stages[i-1].penguin = self.stages[i].penguin
                        self.stages[i-1].fresh = False
                        self.stages[i-1].active = True
                        self.stages[i-1].right = True
                elif stg_cond == 2:
                    if i >= (len(self.stages) - 1):
                        self.ended = True
                    else:
                        self.stages[i + 1].penguin = self.stages[i].penguin
                        self.stages[i + 1].fresh = False
                        self.stages[i + 1].active = True
                        self.stages[i + 1].right = False
                else:
                    pass
            else:
                continue

    def __del__(self):
        pass
