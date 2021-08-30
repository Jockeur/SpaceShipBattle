import pygame
import random

from Enemy import *


class EnemyManager:
    def __init__(self, res, player):
        self.res = res
        self.player = player

        self.sprite_group = pygame.sprite.Group()

        # images
        self.bullet_img = pygame.image.load("res/sprites/bullet.png")

        self.enemy_1 = pygame.image.load("res/sprites/e1.png")
        self.enemy_2 = pygame.image.load("res/sprites/e2.png")
        self.enemy_3 = pygame.image.load("res/sprites/e3.png")

        self.enemy_list = [self.enemy_1, self.enemy_2, self.enemy_3]

        self.ellipse = (self.res[0]/2 - 20, self.res[1]/2 - 10)

        self.level = 1

        self.spawn(self.level)

    def update(self):
        if len(self.sprite_group.sprites())  == 0:
            self.level += 1
            self.spawn(self.level)

        for enemy in self.sprite_group.sprites():
            enemy.pre_update(self.player)
        self.sprite_group.update()

    def draw(self, surface):
        self.sprite_group.draw(surface)

    def spawn(self, n):
        for k in range(n):
            enemy_img = random.choice(self.enemy_list)
            enemy = Enemy((400, 75*k), self.player.speed, enemy_img, self.bullet_img, self.ellipse, self.res)
            self.sprite_group.add(enemy)
