from classes import *
from server import *
import datetime
from time import sleep

# pg.init()

scr = pg.display.set_mode((w, h), pg.FULLSCREEN)
cursor = Cursor(0, 0)
pg.font.init()
pg.mouse.set_visible(False)
bgs = ((255, 255, 255), (255, 255, 255), (0, 153, 255), (255, 255, 255))
fps = 64
clock = pg.time.Clock()
startButton = Button(w // scale // 2 - 28, h // scale // 2 - 30, cut_img(63, 144, 57, 12, "startbutton"))
bird = Bird(1, 1)
tube = Tube()
font = pg.font.Font("Comfortaa-Bold.ttf", 20)
scene = 3  # 0 - меню, 1 - настройки, 2 - игра, 3 - экран поражения
ms = 0
isMouseDown = False
treeTimer = 3000
lastFrameDate = datetime.datetime.now()
threads = []
bench = Bench(w // scale + 50, h // scale - 52)
deathbench = Bench(w // scale + 50, h // scale - 52, True)
scr1 = pg.Surface((w // scale, h // scale))
scr1.fill((1, 1, 1))
scr1.set_colorkey((1, 1, 1))
generate_trees = True
death_mp3 = pg.mixer.Sound("dead.mp3")
score = 0

while run[0]:
    scr.fill((bgs[scene]))
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
                    run[0] = False
                else:
                    scr1.fill((1, 1, 1))
                    scr1.set_colorkey((1, 1, 1))
                    scene = 0
            elif event.key == pg.K_SPACE and scene == 2:
                tube.jump()
        elif event.type == pg.KEYUP and event.key == pg.K_SPACE:
            tube.unjump()
    if scene == 0:
        cursor.calc(ms)
        cursor.draw(scr)
        if cursor.inBtn(startButton):
            if not cursor.rect:
                # cursor.setPos(startButton.x + startButton.w // 2, startButton.y + startButton.h // 2)
                cursor.setPos((startButton.x + startButton.w // 2 + 1) * scale - 2, (startButton.y + startButton.h // 2) * scale)
                cursor.rect = True
                cursor.setSize(startButton.w * scale + scale * 2, startButton.h * scale + scale * 2)
            if isMouseDown:
                scene = 2
                cursor.reset()
                # if not len(trees):
                #     for i in range(20):
                #         scr.fill((255, 255, 255))
                #         pg.draw.polygon(scr, (0, 153, 255), ((0, 0), (w / 9 * i, 0), (0, h / 9 * i)))
                #         pg.display.flip()
                #         createTree(i * randint(30, 50))
                # lt = 0
                # for t in trees:
                #     t.xf = lt = lt +  randint(30, 50)
                #     t.amove()
        else:
            cursor.reset()
        Button.group.draw(scr1)
    elif scene == 2:
        scr1.fill((0, 153, 255))
        for t in trees:
            t.xf -= ms / 40
            if t.xf <= -t.rect.w:
                r = max(trees, key=lambda a: a.rect.x).rect
                t.xf = r.x + randint(30, 50)
            t.amove()
        treeTimer -= ms
        if treeTimer <= 0:
            treeTimer = 3000
        intersection = bird.intersect(tube)
        if intersection:
            if intersection[1] <= 3:
                bird.pos.y += 1 + intersection[1]
                bird.pos.x += 1 + intersection[1]
            elif intersection[1] >= 7:
                bird.pos.y -= 1 + intersection[1]
        tube.tick(ms)
        bird.tick(ms)
        pg.draw.rect(scr1, (14, 120, 0), (0, h // scale - 25, w // scale, 25))
        trees.draw(scr1)
        Bench.group.draw(scr1)
        Sprite.allSprites.draw(scr1)
        if bird.died(tube):
            r = max(((wi - bird.pos.x) ** 2 + (hi - bird.pos.y) ** 2) ** 0.5 for wi, hi in ((0, 0), (w, 0), (h, 0), (w, h)))
            for i in range(100):
                pg.draw.circle(scr, (255, 102, 0), (bird.pos.x * scale, bird.pos.y * scale), i * r / 100)
                pg.display.flip()
                sleep(0.003)
            for i in range(100):
                pg.draw.rect(scr, (255 - i * 2.55, 102 - 1.02 * i, 0), (0, 0, w, h))
                pg.display.flip()
                sleep(0.003)
            scr1.fill((1, 1, 1))
            scr1.set_colorkey((1, 1, 1))
            scene = 3
    elif scene == 3:
        scr.fill((0, 0, 0))
        scr1.fill((1, 1, 1))
        scr1.set_colorkey((1, 1, 1))
        if deathbench.xf > w // scale / 2:
            deathbench.move(-1, 0)
        deathbench.set_time(score // 1000, score % 1000 // 100, score % 100 // 10, score % 10)
        deathbench.tick(ms)
        deathbench.group.draw(scr1)
    scr.blit(pg.transform.scale(scr1, (w, h)), (0, 0))
    pg.display.flip()
    ms = (datetime.datetime.now() - lastFrameDate).total_seconds() * 1000
    lastFrameDate = datetime.datetime.now()
    # clock.tick()

pg.quit()
