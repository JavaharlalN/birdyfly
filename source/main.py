import pygame as pg
from classes import *

pg.init()
info = pg.display.Info()
w, h = info.current_w, info.current_h
scr = pg.display.set_mode((w, h), pg.FULLSCREEN)
cursor = Cursor(0, 0)
startButton = Button(0, 0, cut_sprite(49, 75, 35, 8))
startButton.moveTo(w // 2, h // 2)
scene = 0  # 0 - меню, 1 - настройки, 2 - игра, 3 - экран поражения
bird = Bird(5, 1)
tube = Tube(w, h)
pg.font.init()
pg.mouse.set_visible(False)
fps = 64
clock = pg.time.Clock()
isMouseDown = False
scale = 4
clickTimeout = 200
run = True
ms = 0
while run:
    scr.fill((255, 255, 255))
    for event in pg.event.get():
        isMouseDown = event.type == pg.MOUSEBUTTONDOWN
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.MOUSEMOTION:
            cursor.x, cursor.y = event.pos
        elif event.type == pg.VIDEORESIZE:
            w, h = event.size
            if scene == 0:
                startButton.moveTo(w // 2, h // 2)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if scene == 0:
                    run = False
                else:
                    scene = 0
            elif event.key == pg.K_SPACE and scene == 2:
                tube.jump()
    if scene == 0:
        cursor.calc(ms)
        cursor.draw(scr)
        if cursor.inBtn(startButton):
            if not cursor.rect:
                # cursor.setPos(startButton.x + startButton.w // 2, startButton.y + startButton.h // 2)
                cursor.setPos(startButton.x + startButton.w * scale / 2 + 10, startButton.y + startButton.h * scale / 2 + 10)
                cursor.rect = True
                cursor.setSize(startButton.w * scale + 24, startButton.h * scale + 24)
            if isMouseDown:
                scene = 2
                cursor.reset()
        else:
            cursor.reset()
        startButton.draw(scr, 4)
    elif scene == 2:
        tube.tick(ms, scale)
        tube.draw(scr, scale)
        bird.tick(ms)
        bird.draw(scr, scale)
    pg.display.flip()
    ms = clock.tick(fps)
pg.quit()
