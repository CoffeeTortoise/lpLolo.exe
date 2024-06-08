from rectmotion import Patrol
from baseclasses import Block
from timer import Timer
import pygame as pg


class Coin(Block):
    def __init__(self, width, height, pos, img_path, snd_path):
        super().__init__(width, height, pos, img_path)
        self.sound = pg.mixer.Sound(snd_path)
        self.collected = False

    def update(self, surface):
        if not self.collected:
            surface.blit(self.image, self.rect)

    def collect(self, score, penguin):
        if self.rect.colliderect(penguin.rect):
            if not self.collected:
                self.sound.play()
                score += 1
                self.collected = True
        return score

    def __del__(self):
        pass


class SolidBlock(Block):
    def __init__(self, width, height, pos, img_path, is_barrier, col_snd):
        super().__init__(width, height, pos, img_path)
        self.is_barrier = is_barrier
        self.is_ground = False
        self.sound = pg.mixer.Sound(col_snd)

    def collide_ammo(self, ammo):
        if self.rect.colliderect(ammo.rect):
            self.sound.play()
            ammo.exist = False
        return ammo

    def grounded(self, chara, blocks):
        for block in blocks:
            if block.rect.colliderect(chara.rect):
                if chara.jump >= 0:
                    chara.onGround = True
                    self.is_ground = True
                    break

    def react(self, chara, blocks):
        dist_y = abs(self.rect.top - chara.rect.top)
        self.is_ground = False
        if dist_y > chara.height:
            chara.onGround = False
        self.grounded(chara, blocks)
        if self.rect.colliderect(chara.rect):
            if self.is_ground:
                chara.onGround = True
            if dist_y <= self.width:
                chara.rect.left -= chara.speed
                chara.speed = 0
        return chara

    def __del__(self):
        pass


class Spike(SolidBlock):
    def __init__(self, width, height, pos, img_path, is_barrier, col_snd):
        super().__init__(width, height, pos, img_path, is_barrier, col_snd)
        self.timer_hit, self.time_hit = Timer(), .5
        self.damage, self.timer_dmg = 1, Timer()

    def hit_penguin(self, penguin):
        if penguin.rect.colliderect(self.rect):
            time = self.timer_hit.get_time()
            if time >= self.time_hit:
                hit = self.timer_dmg.get_time()
                self.timer_dmg.restart()
                penguin.hp -= self.damage*hit
        else:
            self.timer_hit.restart()
        return penguin

    def __del__(self):
        pass


class DestroyableBlock(SolidBlock):
    def __init__(self, width, height, pos, img_path, is_barrier, is_destructible, col_snd):
        super().__init__(width, height, pos, img_path, is_barrier, col_snd)
        self.destructible = is_destructible
        self.destroyed = False

    def behaviour(self, surface):
        if not self.destroyed:
            surface.blit(self.image, self.rect)

    def callback(self, chara, blocks):
        if not self.destroyed:
            chara = self.react(chara, blocks)
        return chara

    def collide_ammo(self, ammo):
        if ammo.exist and not self.destroyed:
            if self.rect.colliderect(ammo.rect) and self.destructible:
                self.sound.play()
                ammo.exist = False
                self.destroyed = True
        return ammo

    def __del__(self):
        pass


class Masher(SolidBlock):
    def __init__(self, *args):
        """Arguments: width, height, pos, img_path, is_barrier, col_snd, speed,
            top, bottom, fall_snd, active
        """
        super().__init__(args[0], args[1], args[2], args[3], args[4], args[5])
        self.motion = Patrol(self.rect, False, args[6], top=args[7], bottom=args[8])
        self.fall_snd = pg.mixer.Sound(args[9])
        self.bottom = args[8]
        self.active, self.on = args[10], True

    def update(self, surface):
        self.work()
        super().update(surface)

    def kill_penguin(self, penguin):
        x, m_x = penguin.rect.left, self.rect.left
        pos = x if not penguin.right else (x + penguin.width)
        m_pos = m_x if penguin.right else (m_x + self.width)
        if penguin.rect.colliderect(self.rect):
            if abs(pos - m_pos) >= self.width*.1:
                penguin.alive = False
        return penguin

    def work(self):
        if self.active and self.on:
            self.rect = self.motion.patrol_v()
            self.motion.me_rect = (self.rect, False)
            if self.rect.top >= self.bottom:
                self.fall_snd.play()

    def __del__(self):
        pass
