import pygame

from SpaceShip import *


class Enemy(SpaceShip):
    def __init__(self, pos, speed, img, bullet_img):
        SpaceShip.__init__(pos, speed, img, bullet_img)
