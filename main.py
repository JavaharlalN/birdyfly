import pygame as pg
from classes import *

pg.init()
w, h = 300, 300
scr = pg.display.set_mode((w, h), pg.RESIZABLE)
cursor = Cursor(0, 0)
startButton = Button(150 - 88, 150 - 26, 176, 52)
startButtonImage = pg.image.load("play.png")
scene = 0  # 0 - меню, 1 - настройки, 2 - игра, 3 - экран поражения
pg.font.init()
fps = 64
clock = pg.time.Clock()
run = True
while run:
    scr.fill((255, 255, 255))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.MOUSEMOTION:
            cursor.x, cursor.y = event.pos
        elif event.type == pg.VIDEORESIZE:
            w, h = event.size
            if scene == 0:
                startButton.moveTo(w // 2, h // 2)
    if scene == 0:
        scr.blit(startButtonImage, (startButton.x, startButton.y))
        pg.draw.rect(scr, (0, 153, 255), (startButton.x - 10, startButton.y - 10, startButton.w, startButton.h), 2)
    pg.display.flip()
    clock.tick(fps)
pg.quit()
