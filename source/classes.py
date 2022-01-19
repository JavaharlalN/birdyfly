from sprites import *
import pygame as pg

def draw_pixel(scr, x, y, color, scale=4):
    for i in range(1, scale + 1):
        for j in range(1, scale + 1):
            scr.set_at((x * scale + i, y * scale + j), color)


class Bird:
    def __init__(self, x, y):
        self.beak = choice(beaks)
        self.wing = choice(wings)
        self.eye = choice(eyes)
        self.x, self.y = x, y
        self.wingPhase = 0
        self.blink = False
        self.eyePhase = 0
        self.body = body
        self.ms = 0

    def drawEye(self, scr, scale=1):
        for x in range(7):
            for y in range(7):
                key = self.eye[self.eyePhase][y][x]
                if key == '_':
                    continue
                draw_pixel(scr, self.x + x + 9, self.y + y, colors[key], scale)

    def drawWing(self, scr, scale=1):
        w, h = len(self.wing[self.wingPhase][0]), len(self.wing[self.wingPhase])
        for x in range(w):
            for y in range(h):
                key = self.wing[self.wingPhase][y][x]
                if key == '_':
                    continue
                draw_pixel(scr, self.x + x - 4, self.y + y + 4, colors[key], scale)

    def drawBody(self, scr, scale=1):
        w, h = len(self.body[0]), len(self.body)
        for x in range(w):
            for y in range(h):
                key = self.body[y][x]
                if key == '_':
                    continue
                draw_pixel(scr, self.x + x, self.y + y, colors[key], scale)

    def drawBeak(self, scr, scale=1):
        w, h = len(self.beak[0]), len(self.beak)
        for x in range(w):
            for y in range(h):
                key = self.beak[y][x]
                if key == '_':
                    continue
                draw_pixel(scr, self.x + x + 9, self.y + y + 6, colors[key], scale)

    def draw(self, scr, scale=1):
        self.drawBody(scr, scale)
        self.drawWing(scr, scale)
        self.drawBeak(scr, scale)
        self.drawEye(scr, scale)

    def tick(self, ms):
        self.ms += ms
        if self.ms - 400 >= 0:
            self.wingPhase = (self.wingPhase + 1) % 4
            self.y += (1, -1, -1, 1)[self.wingPhase]
            self.ms = 0


class Vec:
    def __init__(self, x, y):
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
    def __init__(self, x, y, sprite=None, scale=4):
        self.x = x
        self.y = y
        self.sprite = sprite
        w, h = len(self.sprite[0]), len(self.sprite)
        self.w = w
        self.h = h
        self.x1 = x + w * scale
        self.y1 = y + h * scale
        self.scale = scale

    def moveTo(self, x, y):
        self.x = x - self.w * self.scale // 2
        self.y = y - self.h * self.scale // 2

    def draw(self, scr, scale=1):
        pg.draw.rect(scr, (255, 255, 255), (self.x, self.y, self.w * scale + 20, self.h * scale + 20))
        pg.draw.rect(scr, (0, 153, 255), (self.x, self.y, self.w * scale + 20, self.h * scale + 20), 2)
        for x in range(self.w):
            for y in range(self.h):
                key = self.sprite[y][x]
                if key == '_':
                    continue
                for i in range(1, scale + 1):
                    for j in range(1, scale + 1):
                        scr.set_at((self.x + 10 + x * scale + i, self.y + 10 + y * scale + j), colors[key])


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
        return 0 <= self.x - b.x + 10 <= b.w * b.scale + 40 and 0 <= self.y - b.y + 10 <= b.h * b.scale + 40

    def draw(self, scr):
        if self.rect:
            pg.draw.rect(scr, (153, 153, 153), (self.xn[0] - self.w[0] // 2, self.yn[0] - self.h[0] // 2, self.w[0], self.h[0]))
        else:
            pg.draw.circle(scr, (153, 153, 153), (self.x, self.y), self.r[0])


class Tube:
    def __init__(self, w, h, scale=4):
        self.x = (w // scale) // 2
        self.y = (h // scale) // 2
        self.h = h // scale
        self.v = 0

    def tick(self, ms, scale):
        self.v += 9.81 * ms / (1000 * scale)
        self.y += self.v
        if self.y + 20 > self.h:
            self.y = self.h - 20
        elif self.y < 20:
            self.y = 20
            self.v = 1

    def jump(self):
        self.v = -3

    def set(self, w, h, scale):
        self.x = (w // scale) // 2
        self.y = (h // scale) // 2

    def draw(self, scr, scale=4):
        for x in range(int(self.x - 7), self.x + 7):
            for y in range(int(self.y + 20), self.h):
                draw_pixel(scr, x, y, (155, 230, 90) if x <= self.x - 6 else (85, 130, 35) if x >= int(self.x + 5) else (120, 190, 50), scale)
            for y in range(int(self.y - 20)):
                draw_pixel(scr, x, y, (155, 230, 90) if x <= self.x - 6 else (85, 130, 35) if x >= int(self.x + 5) else (120, 190, 50), scale)
        for x in range(self.x - 8, self.x + 8):
            for y in range(int(self.y - 20), int(self.y - 13)):
                draw_pixel(scr, x, y, (155, 230, 90) if x <= self.x - 7 else (85, 130, 35) if x >= int(self.x + 6) else (120, 190, 50), scale)
        #     for y in range(int(self.y + 15), int(self.y + 20)):
        #         draw_pixel(scr, x, y, (120, 190, 50) if x <= self.x - 5 else (85, 130, 35) if x >= int(self.x + 7) else (155, 230, 90), scale)


class Game:
    def __init__(self):
        self.biome = 0
