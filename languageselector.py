from constants import ct_size, ct_wndSize, ct_fps1, ct_fnt_path
from constants import ct_fnt_size, ct_white, ct_black
from othermuspaths import mu_language_mus
from penguinpaths import ps_just_penguin
from baseclasses import Block, Scene
import pygame as pg


class LanguageSelector(Scene):
    def __init__(self, surface):
        super().__init__(ct_fps1, surface)
        self.penguin = Block(ct_size*7, ct_size*9,
                             (ct_size*20, ct_wndSize[1]-ct_size*23), ps_just_penguin)
        self.canvas = pg.Surface((ct_size*24, ct_wndSize[1]))
        self.penguin.rect.left, self.penguin.rect.top = ct_size*8, 0
        self.blank = pg.Surface((ct_size*24, ct_wndSize[1]-ct_size*9))
        self.font1 = pg.font.Font(ct_fnt_path, ct_fnt_size)
        self.font2 = pg.font.Font(ct_fnt_path, ct_fnt_size*4)
        choose, ru, en = 'Choose the language: ', 'RU', 'En'
        self.text = self.font1.render(choose, 1, ct_white)
        self.rus = self.font2.render(ru, 1, ct_black, ct_white)
        self.eng = self.font2.render(en, 1, ct_black, ct_white)
        self.ru_btn = self.rus.get_rect()
        self.en_btn = self.eng.get_rect()
        self.ru_btn.left, self.ru_btn.top = ct_size * 17.5, ct_wndSize[1] - ct_size * 9
        self.en_btn.left, self.en_btn.top = ct_size * 25.5, ct_wndSize[1] - ct_size * 9
        self.music = pg.mixer.music
        self.mus_path = mu_language_mus

    def behaviour(self):
        self.start_mus()
        self.surface.fill(ct_black)
        self.drawings()
        self.about_mouse()
        pg.display.flip()
        self.buttons()
        self.quit_opts()

    def drawings(self):
        self.draw_on_canvas()
        self.draw_on_blank()
        self.surface.blit(self.canvas, (ct_size * 12, 0))
        self.surface.blit(self.blank, (ct_size * 12, ct_wndSize[1] - ct_size * 13))
        self.surface.blit(self.rus, self.ru_btn)
        self.surface.blit(self.eng, self.en_btn)

    def draw_on_canvas(self):
        self.canvas.fill(ct_white)
        self.canvas.blit(self.penguin.image, self.penguin.rect)

    def draw_on_blank(self):
        self.blank.fill(ct_black)
        rect = (0, 0, int(ct_size*24), int(ct_size*10))
        pg.draw.rect(self.blank, ct_white, rect, int(ct_size/2))
        self.blank.blit(self.text, (ct_size, ct_size))

    def buttons(self):
        m_key = pg.mouse.get_pressed()
        m_pos = pg.mouse.get_pos()
        if m_key[0]:
            if self.ru_btn.collidepoint(m_pos):
                self.ru = 1
                self.ended = True
                self.que = 1
            elif self.en_btn.collidepoint(m_pos):
                self.ru = 0
                self.ended = True
                self.que = 1
            else:
                pass

    def __del__(self):
        pass
