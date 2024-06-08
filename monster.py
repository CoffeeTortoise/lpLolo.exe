from baseclasses import Character, Timer


class Monster(Character):
    def __init__(self, m_speed, m_jump, width, height, hp, attack):
        super().__init__(m_speed, m_jump, width, height, hp, attack)
        self.frames_r = None
        self.frames_l = None
        self.image = None
        self.rect = None
        self.animate_r = None
        self.animate_l = None
        self.timer_run = Timer()
        self.timer_up = Timer()

    @property
    def pos(self):
        return self.rect.left, self.rect.top

    @pos.setter
    def pos(self, new):
        self.rect.left, self.rect.top = new

    def update(self, surface):
        if self.alive:
            self.define_right()
            self.animate()
            self.define_pos()
            self.speed, self.jump = 0, 0
            surface.blit(self.image, self.rect)
            if self.hp <= 0:
                self.alive = False

    def moving(self, x):
        time = self.timer_run.get_time()
        pos_x = self.rect.left
        self.timer_run.restart()
        self.speed = self.m_speed * time
        if pos_x - x > 0:
            if self.speed > 0:
                self.speed *= -1
        elif pos_x - x < 0:
            if self.speed < 0:
                self.speed *= -1
        else:
            self.speed = 0
        self.rect.move_ip(self.speed, 0)

    def upping(self, y):
        time = self.timer_up.get_time()
        self.timer_up.restart()
        self.jump = self.m_jump * time
        pos_y = self.rect.top
        if pos_y - y > 0:
            if self.jump > 0:
                self.jump *= -1
        elif pos_y - y < 0:
            if self.jump < 0:
                self.jump *= -1
        else:
            self.jump = 0
        self.rect.move_ip(0, self.jump)

    def define_right(self):
        if self.speed > 0:
            self.right = True
        if self.speed < 0:
            self.right = False

    def define_pos(self):
        pos_x, pos_y = self.rect.left, self.rect.top
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos_x, pos_y

    def animate(self):
        if self.speed != 0:
            if self.right:
                self.image = self.animate_r.animate()
            else:
                self.image = self.animate_l.animate()
        else:
            if self.right:
                self.image = self.frames_r[0]
            else:
                self.image = self.frames_l[0]

    def __del__(self):
        pass
