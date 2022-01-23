from random import randint
from perlin import createLeaf, im
import pygame as pg
import os

pg.init()
info = pg.display.Info()
w, h = info.current_w, info.current_h
run = [True]
scale = 4
trs = 0
trees = pg.sprite.Group()


class Sprite(pg.sprite.Sprite):
    allSprites = pg.sprite.Group()

    def __init__(self, x, y, img, a=True, *groups):
        super().__init__(groups);
        self.image = img
        self.rect = img.get_rect()
        self.xf = x
        self.yf = y
        self.rect.x = x
        self.rect.y = y
        self.a = a
        if a:
            Sprite.allSprites.add(self)

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def amove(self):
        self.rect.x = self.xf
        self.rect.y = self.yf

    def move_to(self, x, y):
        self.rect.x = self.fx = x
        self.rect.y = self.fy = y


def createTree(offset):
    global trs
    tree_w = randint(100, 150)
    tree_h = tree_w + randint(1, 50)
    tr = im.new(mode="RGB", size=(tree_w, tree_h), color=(0, 0, 255))
    tree = tr.load()
    for i in range(tree_w // 2, tree_h):
        tree[tree_w // 2 - 3, i] = (190, 110, 73)
        for j in range(-2, 3):
            tree[tree_w // 2 + j, i] = (137, 71, 53)
        tree[tree_w // 2 + 3, i] = (108, 46, 31)
    leaf = createLeaf(tree_w, tree_w)
    for x in range(tree_w):
        for y in range(tree_w):
            if leaf[x, y] != (0, 0, 255):
                tree[x, y] = leaf[x, y]
    tr.save(f"{os.getcwd()}\sprites\\tree{trs}.png")
    # image = pg.image.load(os.path.join("", f"\sprites\leaf{trees}.png"))
    try:
        image = pg.image.load(f"{os.getcwd()}\sprites\\tree{trs}.png")
        image.set_colorkey((0, 0, 255))
        # trees.add(Sprite(w // scale + tree_w + offset, h - 10 * scale - tree_h, image, False))
        trees.add(Sprite(0, h // scale - 20 - tree_h, image, False))
        # trees.add(Sprite(w + tree_w * scale + offset, 0, image, False))
        trs += 1
    except FileNotFoundError:
        pass


# def createTree():
#     global trs
#     tree_w = randint(100, 150)
#     tree_h = tree_w + randint(1, 50)
#     tr = im.new(mode="RGB", size=(tree_w, tree_h), color=(0, 0, 255))
#     tree = tr.load()
#     for i in range(tree_w // 2, tree_h):
#         tree[tree_w // 2 - 3, i] = (190, 110, 73)
#         for j in range(-2, 3):
#             tree[tree_w // 2 + j, i] = (137, 71, 53)
#         tree[tree_w // 2 + 3, i] = (108, 46, 31)
#     leaf = createLeaf(tree_w, tree_w)
#     for x in range(tree_w):
#         for y in range(tree_w):
#             if leaf[x][y] != (0, 0, 255):
#                 tree[x, y] = leaf[x][y]
#     tr.save(f"{os.getcwd()}\sprites\\tree{trs % 10}.png")
#     try:
#         image = pg.image.load(f"{os.getcwd()}\sprites\\tree{trs % 10}.png")
#         image.set_colorkey((0, 0, 255))
#         trees.add(Sprite(w // scale + tree_w, h // scale - 10 - tree_h, image, False))
#         trs += 1
#     except FileNotFoundError:
#         pass
#     if len(trees) > 10:
#         del trees[0]
