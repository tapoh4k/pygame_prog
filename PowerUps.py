import random

import pygame as pg

from pygame.math import Vector2

heal = pg.image.load("Images/heal.png")
shield = pg.image.load("Images/shield.png")
double_shot = pg.image.load("Images/double.png")
slowdown = pg.image.load("Images/slowdown.png")

screen = pg.display.set_mode((1240, 960))

class PowerUp(pg.sprite.Sprite):
    def __init__(self, type, pos, angle, vel=10):
        super().__init__()
        self.type = type
        self.vel = vel
        self.pos = Vector2(pos)
        self.angle = angle
        if type == "heal":
            self.image = pg.transform.rotate(heal, self.angle)
        elif type == "armor":
            self.image = pg.transform.rotate(shield, self.angle)
        elif type == "double shot":
            self.image = pg.transform.rotate(double_shot, self.angle)
        elif type == "slowdown":
            self.image = pg.transform.rotate(slowdown, self.angle)
        print(self.image.get_rect(center=pos))
        self.rect = self.image.get_rect(center=pos)