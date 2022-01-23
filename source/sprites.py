from PIL import Image as im
import numpy as np
import pygame as pg
from threading import Thread
import os

img = im.open("sprites.png")
pixels = img.load()
w, h = img.size


def cut_img(x, y, w, h, name):
    spi = im.new(mode="RGB", size=(w, h), color=(0, 0, 255))
    spip = spi.load()
    for j in range(h):
        for i in range(w):
            spip[i, j] = pixels[x + i, y + j]
    spi.save(f"{os.getcwd()}\sprites\{name}.png")
    # image = pg.image.load(os.path.join("", f"sprites\{name}.png"))
    image = pg.image.load(f"{os.getcwd()}\sprites\{name}.png")
    image.set_colorkey((0, 0, 255))
    return image


bird_parts = [
    [cut_img(1 + i % 3 * 8, 1 + (i // 3) * 8, 7, 7, f"eye{i % 3}{i // 3}") for i in range(9)] +  # 0..9 eyes
    [cut_img(1 + 12 * i, 54, 11, 6, f"wing1{i}") for i in range(3)] +  # 9..12 wing1
    [cut_img(1 + 12 * i, 61, 11, 6, f"wing2{i}") for i in range(3)] +  # 12..15 wing2
    [cut_img(45, 54, 11, 12, "body")] + [  # 15 body
        cut_img(1, 25, 9, 5, "beak1"),  # 16 beak1
        cut_img(1, 31, 14, 7, "beak2"),  # 17 beak2
        cut_img(1, 39, 14, 5, "beak3"),  # 18 beak3
        cut_img(1, 45, 9, 8, "beak4")  # 19 beak4
    ]
][0]
