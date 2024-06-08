from constants import ct_white, ct_black, ct_red, ct_green
from turtlepaths import tp_boss_portal, tp_tp_in_snd
from constants import ct_size, ct_wndSize, ct_fps2
from penguinpaths import ps_bullet, ps_ammo_snd
from constants import ct_fnt_path, ct_fnt_size
from othermuspaths import mu_tdb_mus
from baseclasses import Block, Scene
from blockpaths import bs_ice_block
from layoutsone import ls1_road
from turtleboss import TBoss
from penguin import Penguin
from timer import Timer
import pygame as pg


class ThreeDays(Scene):
    def __init__(self, surface):
        super().__init__(ct_fps2, surface)
        self.ground = []
        for row_index, row in enumerate(ls1_road):
            for col_index, cell in enumerate(row):
                x = col_index*ct_size
                y = row_index*ct_size
                if cell == 'G':
                    block = Block(ct_size, ct_size, (x, y), bs_ice_block)
                    self.ground.append(block)
        self.penguin = Penguin(ct_size*6, ct_size*300, ct_size, ct_size*1.5,
                               5, 10, (ct_size*15, ct_wndSize[1]-ct_size*4.5),
                               ps_bullet, ct_size, ct_size, ps_ammo_snd)
        self.turtle = TBoss(ct_size*6, ct_size*300, ct_size*1.5, ct_size*2.5, 666, 666,
                            (ct_size*30, ct_wndSize[1]-ct_size*5.5))
        self.tp = Block(self.turtle.width*2, self.turtle.height*2,
                        (ct_size*29, ct_wndSize[1]-ct_size*9),
                        tp_boss_portal)
        self.tp_sound = pg.mixer.Sound(tp_tp_in_snd)
        self.turtle.right = False
        self.timer = Timer()
        self.font1 = pg.font.Font(ct_fnt_path, ct_fnt_size)
        self.font2 = pg.font.Font(ct_fnt_path, ct_fnt_size*5)
        txt = '3 days earlier' if (self.ru == 0) else '3 дня до'
        self.text = self.font2.render(txt, 1, ct_white)
        p_txt1 = 'You again?' if (self.ru == 0) else 'Опять ты?'
        t_txt1 = 'Hello' if (self.ru == 0) else 'Привет'
        self.t_txt2 = ''
        if self.ru == 0:
            self.t_txt2 = 'He ordered me to destroy\nyour village if you\n'
            self.t_txt2 += ' don\'t join his army'
        else:
            self.t_txt2 = 'Он приказал мне уничтожить\nтвою деревню если ты\n'
            self.t_txt2 += 'не присоединишься к его армии'
        self.p_text = self.font1.render(p_txt1, 1, ct_red)
        self.pt_pos = (ct_size*16, ct_wndSize[1]-ct_size*6)
        self.t_text = self.font1.render(t_txt1, 1, ct_green)
        self.tt_pos = (ct_size*28, ct_wndSize[1]-ct_size*7)
        self.music = pg.mixer.music
        self.mus_path = mu_tdb_mus

    def behaviour(self):
        self.start_mus()
        self.refresh_data()
        self.surface.fill(ct_black)
        self.drawings()
        self.tempo_draw()
        pg.display.flip()
        self.quit_opts()

    def refresh_data(self):
        if not self.got_data:
            self.get_data()
            txt = '3 days earlier' if (self.ru == 0) else '3 дня до'
            self.text = self.font2.render(txt, 1, ct_white)
            p_txt1 = 'You again?' if (self.ru == 0) else 'Опять ты?'
            t_txt1 = 'Hello' if (self.ru == 0) else 'Привет'
            self.t_txt2 = ''
            if self.ru == 0:
                self.t_txt2 = 'He ordered me to destroy\nyour village if you\n'
                self.t_txt2 += ' don\'t join his army'
            else:
                self.t_txt2 = 'Он приказал мне уничтожить\nтвою деревню если ты\n'
                self.t_txt2 += 'не присоединишься к его армии'
            self.p_text = self.font1.render(p_txt1, 1, ct_red)
            self.pt_pos = (ct_size * 16, ct_wndSize[1] - ct_size * 6)
            self.t_text = self.font1.render(t_txt1, 1, ct_green)

    def tempo_draw(self):
        time = self.timer.get_time()
        if (time >= 0) and (time < 2):
            self.surface.fill(ct_black)
            self.surface.blit(self.text, (ct_wndSize[0]*.5-ct_size*15,
                                          ct_wndSize[1]-ct_size*15))
        if (time > 2) and (time < 4):
            self.tp.update(self.surface)
        if (time > 3.7) and (time < 4):
            self.tp_sound.play()
        if (time > 4) and (time < 21):
            self.turtle.update(self.surface)
        if (time > 4) and (time < 6):
            self.surface.blit(self.p_text, self.pt_pos)
        if (time > 6) and (time < 8):
            self.surface.blit(self.t_text, self.tt_pos)
        if (time > 8) and (time < 15):
            self.t_text = self.font1.render(self.t_txt2, 1, ct_green)
            x = self.tt_pos[0]-ct_size*13 if (self.ru == 0) else self.tt_pos[0]-ct_size*22
            self.surface.blit(self.t_text, (x, self.tt_pos[1]-ct_size*3))
        if (time > 15) and (time < 18):
            self.penguin.fire = True
            self.penguin.shooting(self.surface)
            self.penguin = self.turtle.defend(self.penguin)
        if time > 18:
            self.penguin.bullet.exist = False
            self.turtle.block = False
        if (time > 18) and (time < 20):
            t_text = 'Bye bye' if (self.ru == 0) else 'Пока'
            self.t_text = self.font1.render(t_text, 1, ct_green)
            self.surface.blit(self.t_text, self.tt_pos)
        if (time > 20) and (time < 22):
            self.tp.rect.left = self.turtle.rect.left-ct_size
            self.tp.rect.top = self.turtle.rect.top-ct_size*2
            self.tp.update(self.surface)
        if (time > 21.5) and (time < 21.8):
            self.tp_sound.play()
        if (time > 22) and (time < 24):
            p_text = 'Coward!' if (self.ru == 0) else 'Трус!'
            self.p_text = self.font1.render(p_text, 1, ct_red)
            self.surface.blit(self.p_text, self.pt_pos)
        if time > 24:
            self.que = 3
            self.ended = True

    def drawings(self):
        for block in self.ground:
            block.update(self.surface)
        self.surface.blit(self.penguin.image, self.penguin.rect)

    def __del__(self):
        pass
