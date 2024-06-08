from constants import ct_red, ct_green, ct_blue, ct_white, ct_black, ct_scarlett
from constants import ct_fnt_path, ct_fnt_size, ct_carmine, ct_papyrus
from constants import ct_amethyst, ct_size, ct_wndSize, ct_sunrise
from demonspaths import dp_star, dp_star_ask
from baseclasses import Block, ShortScene
from rectentity import RectEntity
from random import randint
from timer import Timer
import fleshpaths as f
import soulspaths as s
import pygame as pg


class Lolo(ShortScene):
    def __init__(self, surface):
        super().__init__(surface)
        lo_x, lo_y = ct_size*18, ct_size
        self.lo_al = Block(ct_size*10, ct_size*15, (lo_x, lo_y),
                           s.sp_lo_al)
        self.lo_de = Block(ct_size*10, ct_size*15, (lo_x, lo_y),
                           s.sp_lo_de)
        txt1 = 'What\'s up?' if (self.ru == 0) else 'Как дела?'
        self.text1 = self.base_fnt.render(txt1, 1, ct_blue)
        self.text1_pos = (ct_size*18, ct_wndSize[1]-ct_size*7)
        txt2 = 'Where were you?' if (self.ru == 0) else 'Где ты был?'
        self.text2 = self.base_fnt.render(txt2, 1, ct_black)
        self.text2_pos = (ct_size*15, ct_wndSize[1]-ct_size*7)
        self.sound = pg.mixer.Sound(s.sp_bell)

    def behaviour(self):
        if not self.ended:
            self.refresh()
            self.drawings()

    def drawings(self):
        time = self.timer.get_time()
        if time < 3:
            self.draw_one()
        elif (time > 3) and (time < 6):
            if not self.mute:
                self.sound.play()
                self.mute = True
            self.draw_two()
        else:
            self.ended = True

    def refresh(self):
        if not self.fresh:
            self.refresh_data()
            txt1 = 'What\'s up?' if (self.ru == 0) else 'Как дела?'
            self.text1 = self.base_fnt.render(txt1, 1, ct_blue)
            txt2 = 'Where were you?' if (self.ru == 0) else 'Где ты был?'
            self.text2 = self.base_fnt.render(txt2, 1, ct_black)

    def draw_one(self):
        self.surface.fill(ct_white)
        self.lo_al.update(self.surface)
        self.surface.blit(self.text1, self.text1_pos)

    def draw_two(self):
        self.surface.fill(ct_scarlett)
        self.lo_de.update(self.surface)
        self.surface.blit(self.text2, self.text2_pos)

    def __del__(self):
        pass


class Family(ShortScene):
    def __init__(self, surface):
        super().__init__(surface)
        da_x, da_y = ct_size*13, ct_wndSize[1]-ct_size*13
        da_al = Block(ct_size*5, ct_size*6, (da_x, da_y),
                      s.sp_da_al)
        wi_x, wi_y = da_x+da_al.width+ct_size, da_y-ct_size*9
        wi_al = Block(ct_size*9, ct_size*15, (wi_x, wi_y),
                      s.sp_wi_al)
        so_x, so_y = wi_x+wi_al.width+ct_size, da_y-ct_size
        so_al = Block(ct_size*6, ct_size*7, (so_x, so_y),
                      s.sp_so_al)
        self.penguins1 = [da_al, wi_al, so_al]
        da_de = Block(ct_size*5, ct_size*7, (da_x-ct_size, da_y-ct_size),
                      s.sp_da_de)
        wi_de = Block(ct_size*13, ct_size*15, (wi_x-ct_size, wi_y),
                      s.sp_wi_de)
        so_de = Block(ct_size*6, ct_size*7, (so_x+ct_size*3, so_y),
                      s.sp_so_de)
        self.penguins2 = [da_de, wi_de, so_de]
        txt1 = 'We feel so lonely without you'
        txt2 = 'Join us'
        if self.ru == 1:
            txt1 = 'Нам так одиноко без тебя'
            txt2 = 'Присоединяйся к нам'
        self.text1_pos = (ct_size*11, ct_wndSize[1]-ct_size*6)
        self.text1 = self.base_fnt.render(txt1, 1, ct_amethyst)
        self.text2_pos = (ct_size*15, ct_wndSize[1]-ct_size*6)
        self.text2 = self.base_fnt.render(txt2, 1, ct_black)
        self.sound = pg.mixer.Sound(s.sp_corps)

    def behaviour(self):
        if not self.ended:
            self.refresh()
            self.drawings()

    def drawings(self):
        time = self.timer.get_time()
        if time < 3:
            self.draw_one()
        elif (time > 3) and (time < 6):
            if not self.mute:
                self.sound.play()
                self.mute = True
            self.draw_two()
        else:
            self.ended = True

    def refresh(self):
        if not self.fresh:
            self.refresh_data()
            txt1 = 'We feel so lonely without you'
            txt2 = 'Join us'
            if self.ru == 1:
                txt1 = 'Нам так одиноко без тебя'
                txt2 = 'Присоединяйся к нам'
            self.text1 = self.base_fnt.render(txt1, 1, ct_amethyst)
            self.text2 = self.base_fnt.render(txt2, 1, ct_black)

    def draw_one(self):
        self.surface.fill(ct_white)
        for penguin in self.penguins1:
            penguin.update(self.surface)
        self.surface.blit(self.text1, self.text1_pos)

    def draw_two(self):
        self.surface.fill(ct_red)
        for penguin in self.penguins2:
            penguin.update(self.surface)
        self.surface.blit(self.text2, self.text2_pos)

    def __del__(self):
        pass


class Joke(ShortScene):
    def __init__(self, surface):
        super().__init__(surface)
        self.booked = False
        x_b, y_b = ct_size*10, 0
        b_width, b_height = ct_size*30, ct_wndSize[1]-ct_size
        sat = Block(b_width, b_height, (x_b, y_b), s.sp_sat)
        lizard = Block(b_width, b_height, (x_b, y_b), s.sp_liz)
        turtle = Block(b_width, b_height, (x_b, y_b), s.sp_tur)
        self.book = [sat, lizard, turtle]
        self.turtle = Block(ct_size*40, b_height, (x_b-ct_size*5, y_b),
                            s.sp_hel)
        self.timer2 = Timer()
        self.fnt2 = pg.font.Font(ct_fnt_path, ct_fnt_size*7)
        txt1 = 'Just...' if (self.ru == 0) else 'Я просто...'
        txt2 = 'KIDDING!' if (self.ru == 0) else 'ШУЧУ!'
        self.text1 = self.base_fnt.render(txt1, 1, ct_green)
        self.text2 = self.fnt2.render(txt2, 1, ct_green)
        self.text1_pos = (ct_size*5, ct_size*2)
        self.text2_pos = (ct_size*8, ct_size*10)
        self.sound = pg.mixer.Sound(s.sp_browse)
        self.sound2 = pg.mixer.Sound(s.sp_t_scream)

    def behaviour(self):
        if not self.ended:
            self.refresh()
            if not self.booked:
                self.draw_one()
            else:
                self.draw_two()

    def refresh(self):
        if not self.fresh:
            self.refresh_data()
            txt1 = 'Just...' if (self.ru == 0) else 'Я просто...'
            txt2 = 'KIDDING!' if (self.ru == 0) else 'ШУЧУ!'
            self.text1 = self.base_fnt.render(txt1, 1, ct_green)
            self.text2 = self.fnt2.render(txt2, 1, ct_green)

    def draw_one(self):
        self.surface.fill(ct_black)
        time = self.timer.get_time()
        self.sound.play()
        for i, page in enumerate(self.book):
            if time >= i:
                self.book[i].update(self.surface)
        if time > 3:
            self.booked = True

    def draw_two(self):
        time = self.timer2.get_time()
        if time < 2.5:
            self.sound2.play()
        if time < 2:
            self.surface.fill(ct_carmine)
            self.turtle.update(self.surface)
        elif (time > 2) and (time < 4):
            self.surface.fill(ct_black)
            if time > 2:
                self.surface.blit(self.text1, self.text1_pos)
            if time > 3:
                self.surface.blit(self.text2, self.text2_pos)
        else:
            self.ended = True

    def __del__(self):
        pass


class StarPainter(ShortScene):
    def __init__(self, surface):
        super().__init__(surface)
        s_x, s_y = ct_size*7, ct_size
        self.star = Block(ct_size*10, ct_size*10, (s_x, s_y), dp_star)
        c_x, c_y = ct_size*20, 0
        self.canvas = RectEntity(ct_size*26, ct_size*22, ct_papyrus, c_x, c_y)
        txt1 = 'Do you like ' if (self.ru == 0) else 'Тебе нравится '
        txt2 = 'my art?' if (self.ru == 0) else 'моё искусство?'
        self.text1 = self.base_fnt.render(txt1, 1, ct_scarlett)
        self.text2 = self.base_fnt.render(txt2, 1, ct_scarlett)
        self.text1_pos = (s_x, ct_wndSize[1]-ct_size*11)
        self.text2_pos = (s_x+ct_size, ct_wndSize[1]-ct_size*9)
        a_x, a_y = c_x+ct_size*2, ct_size*5
        art1 = Block(ct_size*20, ct_size*14, (a_x, a_y), f.fs_face)
        art2 = Block(ct_size*20, ct_size*20, (a_x, a_y-ct_size*4), f.fs_octo)
        art3 = Block(ct_size*20, ct_size*15, (a_x+ct_size, a_y-ct_size*2), f.fs_peace)
        art4 = Block(ct_size*20, ct_size*20, (a_x, a_y-ct_size*4), f.fs_man)
        self.arts = [art1, art2, art3, art4]
        self.sound = pg.mixer.Sound(dp_star_ask)
        self.paint = art2
        self.determined = False

    def behaviour(self):
        if not self.ended:
            self.refresh()
            self.general()

    def general(self):
        time = self.timer.get_time()
        if not self.mute:
            self.sound.play()
            self.mute = True
        if time < 2:
            self.drawings()
        else:
            self.determined = False
            self.ended = True

    def refresh(self):
        if not self.fresh:
            self.refresh_data()
            txt1 = 'Do you like ' if (self.ru == 0) else 'Тебе нравится '
            txt2 = 'my art?' if (self.ru == 0) else 'моё искусство?'
            self.text1 = self.base_fnt.render(txt1, 1, ct_scarlett)
            self.text2 = self.base_fnt.render(txt2, 1, ct_scarlett)

    def drawings(self):
        if not self.determined:
            n = randint(0, len(self.arts)-1)
            self.paint = self.arts[n]
            self.determined = True
        self.surface.fill(ct_sunrise)
        self.star.update(self.surface)
        self.canvas.draw(self.surface)
        self.surface.blit(self.text1, self.text1_pos)
        self.surface.blit(self.text2, self.text2_pos)
        self.paint.update(self.surface)

    def __del__(self):
        pass
