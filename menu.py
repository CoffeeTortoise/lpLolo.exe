from constants import ct_size, ct_wndSize, ct_red, ct_green, ct_blue
from constants import ct_fps1, ct_fnt_path, ct_fnt_size, ct_white
from blockpaths import bs_gray40_block, bs_bld_drip
from constants import ct_black, ct_grey
from glitter import ColorMaker, Glitter
from othermuspaths import mu_menu_mus
from baseclasses import Block, Scene
from turtlepaths import tp_boss_stay
from penguinpaths import ps_stay
from layoutsone import ls1_road
from timer import Timer
from drip import Drip
import pygame as pg


class Menu(Scene):
    def __init__(self, surface):
        super().__init__(ct_fps1, surface)
        self.font = pg.font.Font(ct_fnt_path, ct_fnt_size*3)
        self.small_font = pg.font.Font(ct_fnt_path, ct_fnt_size*2)
        t_start = 'Start' if (self.ru == 0) else 'Начать'
        t_basics = 'Basics' if (self.ru == 0) else 'Основы'
        t_quit = 'Quit' if (self.ru == 0) else 'Выйти'
        self.line_width = int(ct_size*.2)
        self.t_start = self.font.render(t_start, 1, ct_red)
        self.t_basics = self.font.render(t_basics, 1, ct_green)
        self.t_quit = self.font.render(t_quit, 1, ct_blue)
        strt_size = (self.t_start.get_width(), self.t_start.get_height())
        bscs_size = (self.t_basics.get_width(), self.t_basics.get_height())
        quit_size = (self.t_quit.get_width(), self.t_quit.get_height())
        btn1_pos = (ct_size*20, ct_wndSize[1]-ct_size*15)
        btn2_pos = (ct_size*19.5, ct_wndSize[1]-ct_size*11)
        btn3_pos = (ct_size*21, ct_wndSize[1]-ct_size*7)
        self.btn_start = pg.Rect(btn1_pos, strt_size)
        self.btn_basics = pg.Rect(btn2_pos, bscs_size)
        self.btn_quit = pg.Rect(btn3_pos, quit_size)
        pos_p = (ct_size*10, ct_wndSize[1]-ct_size*7)
        self.penguin = Block(ct_size*2, ct_size*3, pos_p, ps_stay)
        t_img_raw = pg.image.load(tp_boss_stay).convert_alpha()
        t_img = pg.transform.scale(t_img_raw, (ct_size*3, ct_size*5))
        pos_t = (ct_size*36, ct_wndSize[1]-ct_size*9)
        self.turtle = pg.transform.flip(t_img, True, False)
        self.turtle_rect = self.turtle.get_rect()
        self.turtle_rect.left, self.turtle_rect.top = pos_t[0], pos_t[1]
        self.ground = []
        for row_index, row in enumerate(ls1_road):
            for col_index, cell in enumerate(row):
                if cell == 'G':
                    x = col_index * ct_size * 2
                    y = row_index * ct_size/1.05
                    block = Block(ct_size * 2, ct_size * 2, (x, y), bs_gray40_block)
                    self.ground.append(block)
        self.glitter = []
        top, bottom, begin, end = 0, ct_size * 5, 0, ct_wndSize[0]
        len_glit, speed = 150, .5
        for i in range(len_glit):
            boost = speed + i / (len_glit * 10)
            circle = Glitter(boost, ct_size, top, bottom, begin, end)
            self.glitter.append(circle)
        self.rain = []
        top, line, bottom = -ct_size*5, 0, ct_wndSize[1]-ct_size*2
        begin, end, speed = 0, ct_wndSize[0], ct_size*50
        for i in range(100):
            speed -= i/50
            drip = Drip(ct_size*.2, ct_size*4, bs_bld_drip, top, line, bottom,
                        begin, end, speed)
            self.rain.append(drip)
        arrows1 = 'Use left and right arrows to move' if (self.ru == 0) else 'Для\
         перемещения используйте левую и правую стрелки'
        arrows2 = 'Use up arrow to jump' if (self.ru == 0) else 'Для прыжка\
         используйте верхнюю стрелку'
        hit = 'Use space to shoot the enemies' if (self.ru == 0) else 'Используйте\
         пробел чтобы стрелять'
        bck = 'Back' if (self.ru == 0) else 'Вернуться'
        self.t_arrows1 = self.small_font.render(arrows1, 1, ct_white)
        self.t_arrows2 = self.small_font.render(arrows2, 1, ct_white)
        self.t_hit = self.small_font.render(hit, 1, ct_white)
        self.btn_back = self.font.render(bck, 1, ct_black, ct_white)
        self.btn_back_rect = self.btn_back.get_rect()
        self.pos_t_arrows1 = (ct_size, ct_wndSize[1]-ct_size*20)
        self.pos_t_arrows2 = (ct_size, ct_wndSize[1]-ct_size*16)
        self.pos_t_hit = (ct_size, ct_wndSize[1]-ct_size*12)
        self.pos_btn_back = (ct_size*19, ct_wndSize[1]-ct_size*7)
        self.btn_back_rect.left = self.pos_btn_back[0]
        self.btn_back_rect.top = self.pos_btn_back[1]
        self.makeColor = ColorMaker(.25)
        self.surface2 = pg.Surface((ct_wndSize[0]-ct_size*10, ct_wndSize[1]-ct_size*4))
        self.rd_color = [0, 0, 0]
        self.menu = True
        self.timer = Timer()
        self.music = pg.mixer.music
        self.mus_path = mu_menu_mus

    def behaviour(self):
        self.start_mus()
        self.refresh_data()
        self.drawings()
        self.about_mouse()
        pg.display.flip()
        self.buttons()
        self.quit_opts()

    def refresh_data(self):
        if not self.got_data:
            self.get_data()
            t_start = 'Start' if (self.ru == 0) else 'Начать'
            t_basics = 'Basics' if (self.ru == 0) else 'Основы'
            t_quit = 'Quit' if (self.ru == 0) else 'Выйти'
            self.line_width = int(ct_size * .2)
            self.t_start = self.font.render(t_start, 1, ct_red)
            self.t_basics = self.font.render(t_basics, 1, ct_green)
            self.t_quit = self.font.render(t_quit, 1, ct_blue)
            strt_size = (self.t_start.get_width(), self.t_start.get_height())
            bscs_size = (self.t_basics.get_width(), self.t_basics.get_height())
            quit_size = (self.t_quit.get_width(), self.t_quit.get_height())
            btn1_pos = (ct_size * 20, ct_wndSize[1] - ct_size * 15)
            btn2_pos = (ct_size * 19.5, ct_wndSize[1] - ct_size * 11)
            btn3_pos = (ct_size * 21, ct_wndSize[1] - ct_size * 7)
            self.btn_start = pg.Rect(btn1_pos, strt_size)
            self.btn_basics = pg.Rect(btn2_pos, bscs_size)
            self.btn_quit = pg.Rect(btn3_pos, quit_size)
            arrows1, arrows2, hit = 'Penguin', 'eats', 'fish'
            if self.ru == 0:
                arrows1 = 'Use left and right arrows to move'
                arrows2 = 'Use up arrow to jump'
                hit = 'Use space to shoot the enemies'
            else:
                arrows1 = 'Для перемещения используйте левую и правую стрелки'
                arrows2 = 'Для прыжка используйте верхнюю стрелку'
                hit = 'Используйте пробел чтобы стрелять'
                self.small_font = pg.font.Font(ct_fnt_path, int(ct_fnt_size*1.3))
            bck = 'Back' if (self.ru == 0) else 'Вернуться'
            self.t_arrows1 = self.small_font.render(arrows1, 1, ct_white)
            self.t_arrows2 = self.small_font.render(arrows2, 1, ct_white)
            self.t_hit = self.small_font.render(hit, 1, ct_white)
            self.btn_back = self.font.render(bck, 1, ct_black, ct_white)

    def drawings(self):
        if self.menu:
            self.draw_menu()
        else:
            self.draw_basics()

    def draw_basics(self):
        time = self.timer.get_time()
        if time < 5:
            self.rd_color = self.makeColor.make_red()
        elif (time > 5) and (time < 15):
            self.rd_color = self.makeColor.make_green()
        elif (time > 15) and (time < 20):
            self.rd_color = self.makeColor.make_blue()
        else:
            self.timer.restart()
        self.surface.fill(self.rd_color)
        self.surface2.fill(ct_grey)
        self.surface2.blit(self.t_arrows1, self.pos_t_arrows1)
        self.surface2.blit(self.t_arrows2, self.pos_t_arrows2)
        self.surface2.blit(self.t_hit, self.pos_t_hit)
        self.surface.blit(self.surface2, (ct_size*5, ct_size))
        self.surface.blit(self.btn_back, self.btn_back_rect)

    def draw_menu(self):
        self.surface.fill(ct_black)
        for block in self.ground:
            block.update(self.surface)
        for drip in self.rain:
            drip.update(self.surface)
        for glow in self.glitter:
            glow.behaviour(self.surface)
        self.penguin.update(self.surface)
        self.surface.blit(self.turtle, self.turtle_rect)
        pg.draw.rect(self.surface, ct_white, self.btn_start, width=self.line_width)
        pg.draw.rect(self.surface, ct_white, self.btn_basics, width=self.line_width)
        pg.draw.rect(self.surface, ct_white, self.btn_quit, width=self.line_width)
        self.surface.blit(self.t_start, self.btn_start)
        self.surface.blit(self.t_basics, self.btn_basics)
        self.surface.blit(self.t_quit, self.btn_quit)

    def buttons(self):
        m_pos = pg.mouse.get_pos()
        m_click = pg.mouse.get_pressed()
        if m_click[0]:
            if self.menu:
                if self.btn_basics.collidepoint(m_pos):
                    self.menu = False
                if self.btn_quit.collidepoint(m_pos):
                    self.que = 666
                    self.ended = True
                if self.btn_start.collidepoint(m_pos):
                    self.que = 1
                    self.ended = True
            else:
                if self.btn_back_rect.collidepoint(m_pos):
                    self.menu = True

    def __del__(self):
        pass
