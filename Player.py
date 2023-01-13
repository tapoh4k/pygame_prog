import pygame as pg

from pygame.math import Vector2

player_image = pg.image.load("Images/Ship.png")
player_shielded_image = pg.image.load("Images/ShipShielded.png")
moving_image = pg.image.load("Images/ShipMoving.png")
moving_shielded_image = pg.image.load("Images/ShipShieldedMoving.png")


class Player(pg.sprite.Sprite):

    def __init__(self, pos, angle, speed):
        super().__init__()
        self.pos = Vector2(pos)
        self.angle = angle
        self.image = pg.transform.rotate(player_image, self.angle)
        self.rect = self.image.get_rect(center=pos)
        self.rotated_image = None
        self.moving = False
        self.speed = speed
        self.shielded = False

    def draw(self, surface):
        surface.blit(self.image, (self.pos.x, self.pos.y))
        if not self.shielded:
            self.image = pg.transform.rotate(player_image, self.angle)
        else:
            self.image = pg.transform.rotate(player_shielded_image, self.angle)

    def update_speed(self):
        if self.speed >= 0:
            self.speed -= 0.1
            move = pg.math.Vector2()
            move.from_polar((self.speed, self.angle + 90))
            self.pos.x += move.x
            self.pos.y -= move.y
            if not self.shielded:
                self.image = pg.transform.rotate(moving_image, self.angle)
            else:
                self.image = pg.transform.rotate(moving_shielded_image, self.angle)
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
