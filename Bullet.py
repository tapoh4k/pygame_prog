import pygame as pg

from pygame.math import Vector2

bullet_image = pg.image.load("Images/Rocket.png")

screen = pg.display.set_mode((1240, 960))


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pg.transform.rotate(bullet_image, angle)
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.angle = angle
        self.timer = 0

    def update(self):
        move = pg.math.Vector2()
        move.from_polar((15, self.angle + 90))
        self.pos.x += move.x
        self.pos.y -= move.y
        self.rect.center = self.pos
        self.timer += 1
        if self.timer == 50:
            self.kill()
