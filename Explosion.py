import pygame as pg

explosion_image = pg.image.load("Images/Explosion.png")


class Explosion(pg.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.image = explosion_image
        self.rect = rect
        self.rect.x -= 50
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer == 20:
            self.kill()

    def hit(self):
        self.kill()
