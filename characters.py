from baseclasses import Bullet
from monster import Monster


class Shooter(Monster):
    def __init__(self, m_speed, m_jump, width, height, hp, attack, pos, ammo_path,
                 ammo_w, ammo_h, snd_path):
        super().__init__(m_speed, m_jump, width, height, hp, attack)
        self.bullet = Bullet(self.attack, self.m_speed*3, ammo_path, ammo_w,
                             ammo_h, pos, snd_path)
        self.fire = False

    def shoot(self, surface):
        if self.fire and not self.bullet.exist:
            self.fire = False
            self.bullet.exist = True
            self.bullet.right = self.right
            self.bullet.sound.play()
        else:
            self.bullet.update(surface)

    def __del__(self):
        pass
