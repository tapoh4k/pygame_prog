import pygame as pg

from pygame.math import Vector2

asteroid_image = pg.image.load("Images/Asteroid.png")

screen = pg.display.set_mode((1240, 960))


class Asteroid(pg.sprite.Sprite):
    def __init__(self, pos, angle, vel=10):
        super().__init__()
        self.image = pg.transform.rotate(asteroid_image, angle)
        self.rect = self.image.get_rect(center=pos)
        self.vel = vel
        self.pos = Vector2(pos)
        self.angle = angle

    def update(self, slowdown=False):
        move = pg.math.Vector2()
        if not slowdown:
            move.from_polar((self.vel, self.angle + 90))
        else:
            move.from_polar((self.vel/2, self.angle + 90))
        self.pos.x += move.x
        self.pos.y -= move.y
        self.rect.center = self.pos
        if self.rect.centery >= screen.get_height() - 25:
            self.kill()

    def hit(self):
        self.kill()
