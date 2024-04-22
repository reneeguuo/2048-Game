# sprite classes
from settings import *
import pygame as pg
vec = pg.math.Vector2

class Cell(pg.sprite.Sprite):
    def __init__(self, cx, cy, value):
        pg.sprite.Sprite.__init__(self)
        self.value = value
        if value == 2:
            img = pg.image.load('img\\cell_2.jpg')
        if value == 4:
            img = pg.image.load('img\\cell_4.jpg')
        if value == 8:
            img = pg.image.load('img\\cell_8.jpg')
        if value == 16:
            img = pg.image.load('img\\cell_16.jpg')
        if value == 32:
            img = pg.image.load('img\\cell_32.jpg')
        if value == 64:
            img = pg.image.load('img\\cell_64.jpg')
        if value == 128:
            img = pg.image.load('img\\cell_128.jpg')
        if value == 256:
            img = pg.image.load('img\\cell_256.jpg')
        if value == 512:
            img = pg.image.load('img\\cell_512.jpg')
        if value == 1024:
            img = pg.image.load('img\\cell_1024.jpg')
        if value == 2048:
            img = pg.image.load('img\\cell_2048.jpg')
        if value == 4096:
            img = pg.image.load('img\\cell_4096.jpg')
        if value == 8192:
            img = pg.image.load('img\\cell_8192.jpg')
        self.image = pg.transform.smoothscale(img, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = ((CELL_SIZE*cx+int(CELL_SIZE/2), CELL_SIZE*cy+int(CELL_SIZE/2)))
        self.fuse = True
        self.vel = vec(0, 0)
        self.cx = cx
        self.cy = cy

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        self.cx = int(self.rect.center[0]/CELL_SIZE)
        self.cy = int(self.rect.center[1]/CELL_SIZE)