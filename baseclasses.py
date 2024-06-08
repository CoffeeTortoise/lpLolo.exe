from constants import ct_size, ct_title, ct_ico_path, ct_wndSize, ct_mouse_img
from constants import ct_beg_path, ct_lev_path, ct_prog_path, ct_que_path, ct_ru_path
from constants import ct_stag_path, ct_mouse_snd, ct_grey
from constants import ct_fnt_path, ct_fnt_size
from saveload import SaveLoad
from timer import Timer
import pygame as pg


class Character(pg.sprite.Sprite):
    def __init__(self, m_speed, m_jump, width, height, hp, attack):
        pg.sprite.Sprite.__init__(self)
        self.m_speed = m_speed
        self.m_jump = m_jump
        self.speed = 0
        self.jump = 0
        self.width = width
        self.height = height
        self.hp = hp
        self.attack = attack
        self.alive = True
        self.right = True
        self.movable = True
        self.timer = Timer()

    def __del__(self):
        pass


class Block(pg.sprite.Sprite):
    def __init__(self, width, height, pos, img_path):
        pg.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        image = pg.image.load(img_path).convert_alpha()
        self.image = pg.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos[0], pos[1]

    @property
    def pos(self):
        return self.rect.left, self.rect.top

    @pos.setter
    def pos(self, new):
        self.rect.left, self.rect.top = new

    def update(self, surface):
        surface.blit(self.image, self.rect)

    def __del__(self):
        pass


class Bullet(pg.sprite.Sprite):
    def __init__(self, attack, speed, img_path, width, height, pos, snd_path):
        pg.sprite.Sprite.__init__(self)
        image = pg.image.load(img_path).convert_alpha()
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos[0], pos[1]
        self.width, self.height = width, height
        self.attack, self.speed = attack, speed
        self.exist, self.right = False, True
        self.timer = Timer()
        self.timer_shoot = Timer()
        self.sound = pg.mixer.Sound(snd_path)

    def update(self, surface):
        self.fly()
        if self.exist:
            surface.blit(self.image, self.rect)

    def collide_bullet(self, bullet):
        if self.rect.colliderect(bullet.rect):
            self.exist = False
            bullet.exist = False
        return bullet

    def fly(self):
        time = self.timer.get_time()
        time_shoot = self.timer_shoot.get_time()
        self.timer_shoot.restart()
        self.define_right()
        if self.exist:
            if time <= 1.5:
                self.rect.left += self.speed*time_shoot
            else:
                self.exist = False
                self.timer.restart()
        else:
            pass

    def define_right(self):
        if self.right:
            if self.speed < 0:
                self.speed *= -1
            else:
                pass
        else:
            if self.speed > 0:
                self.speed *= -1
            else:
                pass

    def __del__(self):
        pass


class Scene:
    def __init__(self, fps, surface):
        pg.display.set_caption(ct_title)
        self.surface = surface
        raw_icon = pg.image.load(ct_ico_path).convert()
        icon = pg.transform.scale(raw_icon, (ct_size, ct_size))
        pg.display.set_icon(icon)
        pg.mouse.set_visible(False)
        self.fps = fps
        m_pos = pg.mouse.get_pos()
        self.mouse = Block(ct_wndSize[1]/21, ct_wndSize[1]/21, m_pos, ct_mouse_img)
        self.beg, self.lev = int(SaveLoad.load(ct_beg_path)), int(SaveLoad.load(ct_lev_path))
        self.prog, self.que = int(SaveLoad.load(ct_prog_path)), int(SaveLoad.load(ct_que_path))
        self.ru, self.stag = int(SaveLoad.load(ct_ru_path)), int(SaveLoad.load(ct_stag_path))
        self.mouse_snd = pg.mixer.Sound(ct_mouse_snd)
        self.mus_on, self.on_mute = False, False
        self.got_data = False
        self.ended = False
        self.music = pg.mixer.music
        self.mus_path = None

    def behaviour(self):
        self.surface.fill(ct_grey)
        self.about_mouse()
        pg.display.flip()
        self.close()

    def get_data(self):
        if not self.got_data:
            self.beg, self.lev = int(SaveLoad.load(ct_beg_path)), int(SaveLoad.load(ct_lev_path))
            self.prog, self.que = int(SaveLoad.load(ct_prog_path)), int(SaveLoad.load(ct_que_path))
            self.ru, self.stag = int(SaveLoad.load(ct_ru_path)), int(SaveLoad.load(ct_stag_path))
            self.got_data = True

    def start_mus(self):
        if not self.mus_on:
            self.music.load(self.mus_path)
            self.music.play(-1)
            self.mus_on = True

    def quit_opts(self):
        if not self.ended:
            self.close()
        else:
            pg.time.delay(1000)
            self.memorize()

    def close(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.music.stop()
            self.que = 666
            self.memorize()
            self.ended = True
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.music.stop()
                    self.que = 666
                    self.memorize()
                    self.ended = True

    def about_mouse(self):
        m_pos = pg.mouse.get_pos()
        m_click = pg.mouse.get_pressed()
        if pg.mouse.get_focused():
            self.mouse.rect.center = m_pos
            self.surface.blit(self.mouse.image, self.mouse.rect)
        if m_click[0]:
            self.mouse_snd.play()

    def memorize(self):
        SaveLoad.save(ct_beg_path, str(self.beg))
        SaveLoad.save(ct_lev_path, str(self.lev))
        SaveLoad.save(ct_prog_path, str(self.prog))
        SaveLoad.save(ct_que_path, str(self.que))
        SaveLoad.save(ct_ru_path, str(self.ru))
        SaveLoad.save(ct_stag_path, str(self.stag))

    def __del__(self):
        pass


class ShortScene:
    def __init__(self, surface):
        self.surface = surface
        self.ended, self.fresh, self.mute = False, False, False
        self.base_fnt = pg.font.Font(ct_fnt_path, ct_fnt_size*2)
        self.ru = int(SaveLoad.load(ct_ru_path))
        self.sound = None
        self.timer = Timer()

    def refresh_data(self):
        if not self.fresh:
            self.ru = int(SaveLoad.load(ct_ru_path))
            self.fresh = True

    def __del__(self):
        pass


class ScreamScene:
    def __init__(self, surface):
        self.surface = surface
        self.ru = int(SaveLoad.load(ct_ru_path))
        self.base_fnt = pg.font.Font(ct_fnt_path, ct_fnt_size)
        self.ended, self.mute, self.fresh = False, False, False
        self.sound, self.start_mus = None, False
        self.timer, self.time_period = Timer(), 10

    def play_mus(self):
        if not self.mute:
            time = self.timer.get_time()
            if time <= self.time_period:
                if not self.start_mus:
                    self.sound.play()
                    self.start_mus = True
            else:
                self.start_mus = False
                self.timer.restart()

    def refresh_data(self):
        if not self.fresh:
            self.ru = int(SaveLoad.load(ct_ru_path))
            self.fresh = True
    
    def __del__(self):
        pass


class RectMotion:
    def __init__(self, rect, is_entity, speed):
        self.rect = rect.my_rect if is_entity else rect
        self.speed = speed
        self.timer = Timer()

    @property
    def me_rect(self):
        return self.rect

    @me_rect.setter
    def me_rect(self, rect_data):
        self.rect = rect_data[0].my_rect if rect_data[1] else rect_data[0]

    def __del__(self):
        pass
