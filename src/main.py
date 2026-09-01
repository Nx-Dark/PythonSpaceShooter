import pygame as pg
import sys

pg.init()

screen_res = (960, 540)
display = pg.display.set_mode(screen_res)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    pg.display.flip()

#exit
pg.quit()
sys.exit(0)