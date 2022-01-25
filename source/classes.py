from sprites import *
import pygame as pg
from perlin import *
from server import w, h, scale, Sprite

g = 15


class AnimatedSprite(Sprite):
    def __init__(self, x, y, seq, a=False, *groups):
        super().__init__(x, y, seq[0], a, groups)
        self.phase = 0
        self.seq = seq

    def update(self):
        self.phase = (self.phase + 1) % len(self.seq)
        self.image = self.seq[self.phase]


class Cat(pg.sprite.Sprite):
    seq_sit = [cut_img(122, 1 + i * 55, 68, 54, f"cs{i}") for i in range(7)]
    seq_flow = [cut_img(191, 1 + i * 55, 112, 54, f"cf{i}") for i in range(26)]

    def __init__(self, x, y, seq, *groups):
        super().__init__(groups)
        self.sit = seq == Cat.seq_sit
        self.image = seq[0]
        self.seq = seq
        self.phase = 0
        self.rect = self.image.get_rect()
        self.xf = self.rect.x = x
        self.yf = self.rect.y = y
        self.tick_to = 100
        self.dir = 0

    def change_seq(self):
        self.phase = 0
        if self.sit:
            self.seq = Cat.seq_flow
        else:
            self.seq = Cat.seq_sit
        self.sit = not self.sit
        self.image = self.seq[0]

    def tick(self, x, y, ms):
        self.tick_to -= ms
        self.rect.x = self.xf = x
        self.rect.y = self.yf = y
        if self.tick_to < 0:
            self.tick_to = 100
            if self.phase == len(self.seq) - 1:
                self.dir = -1
            elif self.phase == 0:
                if not self.sit:
                    self.change_seq()
                elif self.sit and not random.randint(0, 5):
                    self.change_seq()
                self.dir = 1
            self.phase += self.dir
            self.image = self.seq[self.phase]


class LampClock(pg.sprite.Sprite):
    clock = cut_img(57, 54, 44, 20, "clock")
    col = cut_img(102, 1, 18, 96, "col")
    lamp_off = cut_img(1, 68, 20, 19, "lamp_off")
    lamp_on = cut_img(22, 68, 20, 19, "lamp_on")
    lamp = cut_img(25, 1, 75, 41, "lamp")
    digits = [cut_img(29 + 7 * i, 43, 6, 10, f"{i}.png") for i in range(10)]

    def __init__(self, x, y, withClock, *groups):
        super().__init__(groups)
        self.isLamp = not withClock
        self.image = LampClock.col
        if self.isLamp:
            self.head = Sprite(x - 29, y - 37, LampClock.lamp, False, groups)
            self.lb = Sprite(x - 29, y - 18, LampClock.lamp_off, False, groups)
            self.rb = Sprite(x + 27, y - 18, LampClock.lamp_off, False, groups)
        else:
            self.head = Sprite(x - 13, y, LampClock.clock, False, groups)
            self.d1 = Sprite(x - 8, y + 5, random.choice(LampClock.digits), False, groups)
            self.d2 = Sprite(x, y + 5, random.choice(LampClock.digits), False, groups)
            self.semicolon = Sprite(x + 8, y + 5, cut_img(99, 43, 2, 10, "semicolon"), False, groups)
            self.d3 = Sprite(x + 12, y + 5, random.choice(LampClock.digits), False, groups)
            self.d4 = Sprite(x + 20, y + 5, random.choice(LampClock.digits), False, groups)
        self.rect = self.image.get_rect()
        self.rect.x = self.xf = x
        self.rect.y = self.yf = y

    def move(self, x, y):
        self.xf += x
        self.yf += y
        self.rect.x = self.xf
        self.rect.y = self.yf
        self.head.xf += x
        self.head.yf += y
        self.head.amove()
        if self.isLamp:
            self.lb.xf += x
            self.lb.yf += y
            self.rb.xf += x
            self.rb.yf += y
            self.lb.amove()
            self.rb.amove()
        else:
            self.d1.xf += x
            self.d1.yf += y
            self.d2.xf += x
            self.d2.yf += y
            self.d3.xf += x
            self.d3.yf += y
            self.d4.xf += x
            self.d4.yf += y
            self.semicolon.xf += x
            self.semicolon.yf += y
            self.semicolon.amove()
            self.d1.amove()
            self.d2.amove()
            self.d3.amove()
            self.d4.amove()

    def set_time(self, d1, d2, d3, d4):
        self.d1.image = LampClock.digits[d1]
        self.d2.image = LampClock.digits[d2]
        self.d3.image = LampClock.digits[d3]
        self.d4.image = LampClock.digits[d4]


class Bench(pg.sprite.Sprite):
    def __init__(self, x, y, withClock=False):
        self.group = pg.sprite.Group()
        super().__init__(self.group)
        self.ll = LampClock(x - 20, y - 45, withClock, self.group)
        self.cat = Cat(x, y - 29, random.choice((Cat.seq_sit, Cat.seq_flow)), self.group)
        self.image = cut_img(18, 98, 102, 45, "bench")
        self.rect = self.image.get_rect()
        self.rect.x = self.xf = x
        self.rect.y = self.yf = y

    def move(self, x, y):
        self.xf += x
        self.yf += y
        self.rect.x = self.xf
        self.rect.y = self.yf
        self.cat.rect.x = self.xf
        self.cat.rect.y = self.yf - 29
        self.ll.move(x, y)

    def move_to(self, x, y):
        self.move(x - self.xf, y - self.yf)

    def set_time(self, d1, d2, d3, d4):
        self.ll.set_time(d1, d2, d3, d4)

    def tick(self, ms):
        self.cat.tick(self.xf, self.yf - 29, ms)


class Bird:
    def __init__(self, x, y):
        self.sprites = pg.sprite.Group()
        self.body = Sprite(x, y, bird_parts[15], True, self.sprites)
        self.beak = Sprite(x + 9, y + 6, random.choice(bird_parts[16:]), True, self.sprites)
        wing = (bird_parts[9:12], bird_parts[12:15])[random.randint(0, 1)]
        wing.append(wing[1])
        self.wing = AnimatedSprite(x - 2, y + 5, wing, True, self.sprites)
        self.eye = AnimatedSprite(x + 9, y, random.choice((bird_parts[:3], bird_parts[3:6], bird_parts[6:9])), True, self.sprites)
        self.pos = Vec(x, y)
        self.blink = False
        self.wave_to = 400
        self.blink_to = random.randint(3000, 10000)
        self.bf_to = 100
        self.a = 0.0078125
        self.v = Vec(0.9)
        self.score = 0

    def tick(self, ms):
        self.wave_to -= ms
        self.blink_to -= ms
        self.bf_to -= ms
        if self.wave_to <= 0:
            self.wing.update()
            self.pos.y += (1, -1, -1, 1)[self.wing.phase]
            self.wave_to = 400
        if self.bf_to <= 0:
            self.bf_to = 100
            if self.blink:
                self.blink = self.eye.phase != 2
                self.eye.update()
        if self.blink_to <= 0:
            self.blink = True
            self.blink_to = random.randint(3000, 10000)
        self.v.y += g * ms / 30000
        self.v.x += self.a * ms / 1000
        self.pos += self.v
        if self.pos.x > w // scale + 20:
            self.pos.x = -20
            self.score += 1
        self.wing.move_to(self.pos.x - 2, self.pos.y + 5)
        self.body.move_to(self.pos.x, self.pos.y)
        self.eye.move_to(self.pos.x + 9, self.pos.y)
        self.beak.move_to(self.pos.x + 9, self.pos.y + 6)
        if (40 < self.pos.y < h // scale - 40 and (random.random() * self.pos.y / (h // scale) > 0.3)) or self.pos.y >= h // scale - 40:
            self.v.y = -0.5 + self.v.x / 10

    def died(self, tube):
        return bool(pg.sprite.collide_mask(self.beak, tube.sprite))

    def intersect(self, tube):
        return pg.sprite.collide_mask(self.body, tube.sprite)


class Vec:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __mul__(self, v):
        return Vec(self.x * v, self.y * v)

    def __sub__(self, v):
        return Vec(self.x - v.x, self.y - v.y)

    def __add__(self, v):
        return Vec(self.x + v.x, self.y + v.y)

    def __truediv__(self, v):
        return Vec(self.x / v, self.y / v)

    def reflect(self, hor=False):
        if hor:
            self.x = -self.x
        else:
            self.y = -self.y

    def __call__(self):
        return self.x, self.y


class Button:
    group = pg.sprite.Group()

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.sprite = Sprite(x, y, img, False, Button.group)
        w, h = img.get_rect().size
        self.w = w
        self.h = h
        self.x1 = x + w * scale
        self.y1 = y + h * scale
        self.scale = scale

    def moveTo(self, x, y):
        self.x = x - self.w * self.scale // 2
        self.y = y - self.h * self.scale // 2
        self.sprite.rect.x = self.x
        self.sprite.rect.y = self.y


class Cursor:
    def __init__(self, x, y):
        self.rect = False
        self.r = [4, 4]     # значение сейчас, нужное значение
        self.w = [4, 4]     # аналогично
        self.h = [4, 4]     # аналогично
        self.x = x          # x настоящий
        self.y = y          # y настоящий
        self.xn = [x, x, x] # x отображаемый, x нужный, x начальный
        self.yn = [y, y, y] # y отображаемый, y нужный, y начальный
        self.k = 0.0625      # коэффициент изменения
        self.ms = 0

    def setSize(self, *v):
        if self.rect:
            self.w[1], self.h[1] = v
        else:
            self.r[1] = v[0]

    def setPos(self, *v):
        self.xn = [self.x, v[0], self.x]
        self.yn = [self.y, v[1], self.y]

    def reset(self):
        self.rect = False
        self.xn = [self.x] * 3
        self.yn = [self.y] * 3
        self.r = [4, 4]
        self.w = [4, 4]
        self.h = [4, 4]

    def calc(self, ms):
        self.ms += ms
        if self.ms - 10 >= 0:
            self.ms = 0
            self.w[0] = min(self.w[0] + (self.w[1] - 4) * self.k, self.w[1])
            self.h[0] = min(self.h[0] + (self.h[1] - 4) * self.k, self.h[1])
            self.r[0] = min(self.r[0] + (self.r[1] - 2) * self.k, self.r[1])
            self.xn[0] = self.xn[0] + (self.xn[1] - self.xn[2]) * self.k
            self.yn[0] = self.yn[0] + (self.yn[1] - self.yn[2]) * self.k
            if self.xn[0] < self.xn[1] < self.xn[2] or self.xn[0] > self.xn[1] > self.xn[2]:
                self.xn[0] = self.xn[1]
            if self.yn[0] < self.yn[1] < self.yn[2] or self.yn[0] > self.yn[1] > self.yn[2]:
                self.yn[0] = self.yn[1]

    def inBtn(self, b):
        return -1 <= self.x // scale - b.x <= b.w and -1 <= self.y // scale - b.y <= b.h

    def draw(self, scr):
        if self.rect:
            pg.draw.rect(scr, (153, 153, 153), (self.xn[0] - self.w[0] // 2, self.yn[0] - self.h[0] // 2, self.w[0], self.h[0]))
        else:
            pg.draw.circle(scr, (153, 153, 153), (self.x, self.y), self.r[0])


class Tube:
    def __init__(self):
        self.pos = Vec(w // scale // 2, h // scale // 2)
        self.v = 0
        self.sprite = Sprite(self.pos.x - 8, self.pos.y - 620, cut_img(304, 1, 17, 1240, "tube"))
        self.h = h // scale
        self.fly = False
        self.sprite.mask = pg.mask.from_surface(self.sprite.image)

    def tick(self, ms):
        if not self.fly:
            self.v = min(2, self.v + g * ms / 2000)
        self.pos.y += self.v
        if self.pos.y + 25 > self.h:
            self.pos.y = self.h - 25
        elif self.pos.y < 25:
            self.pos.y = 25
            self.v = 1
        self.sprite.rect.x = self.pos.x - 8
        self.sprite.rect.y = self.pos.y - 620

    def jump(self):
        self.v = -2
        self.fly = True

    def unjump(self):
        self.fly = False

    def setPos(self):
        self.pos = Vec((w // scale) // 2, (h // scale) // 2)
