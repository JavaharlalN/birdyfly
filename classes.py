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
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x1 = x + w
        self.y1 = y + h

    def moveTo(self, x, y):
        self.x = x - self.w // 2
        self.y = x - self.h // 2


class Cursor:
    def __init__(self, x, y):
        self.rect = False
        self.r = [4, 4]  # значение сейчас, нужное значение
        self.w = [4, 4]  # аналогично
        self.h = [4, 4]  # аналогично
        self.x = x
        self.y = y
        self.k = 0.125  # коэффициент изменения

    def setSize(self, *v):
        if self.rect:
            self.w[1], self.h[1] = v
        else:
            self.r[1] = v[0]

    def resize(self):
        self.w[0] = min(self.w[0] + (self.w[1] - 4) * self.k, self.w[1])
        self.h[0] = min(self.h[0] + (self.h[1] - 4) * self.k, self.h[1])
        self.r[0] = min(self.r[0] + (self.r[1] - 2) * self.k, self.r[1])
