import pygame
import random
import time

from math import cos, sin, pi

from SpaceShip import *


class Enemy(SpaceShip):
    def __init__(self, pos, speed, img, bullet_img, ellipse, res):
        SpaceShip.__init__(self, pos, speed, img, bullet_img)
        self.res = res

        self.ellipse_origin = ellipse

        self.ellipse = self.ellipse_origin

        self.ellipse_speed = 0.015

        self.time = random.random() * 100
        self.clockwise = False

        # Fire System
        self.fire_timer_range = [1.2, 1.5]
        self.fire_timer_start = time.time()
        self.fire_timer = self.calculate_timer(self.fire_timer_range)

        # Reverse system
        self.reverse_timer_range = [2.5, 5]
        self.reverse_timer_start = time.time()
        self.reverse_fire_timer = self.calculate_timer(self.reverse_timer_range)

    def increase_time(self):
        if self.clockwise:
            self.time += self.ellipse_speed
        else:
            self.time -= self.ellipse_speed

    def calculate_ellipse(self, a, b, t):
        return (self.res[0] / 2 + a * cos(t), self.res[1] / 2 + b * sin(t))

    def pre_update(self, player):
        direction = pygame.math.Vector2(self.pos[0] - player.pos[0], self.pos[1] - player.pos[1]).normalize()
        self.rotation = direction.angle_to(pygame.math.Vector2(0, -1))

        self.direction = pygame.math.Vector2(float(direction.x), float(direction.y))

        self.increase_time()
        self.pos = self.calculate_ellipse(self.ellipse[0], self.ellipse[1], self.time)

        if time.time() - self.reverse_timer_start >= self.reverse_fire_timer:
            self.reverse_timer_start = time.time()
            self.reverse_fire_timer = self.calculate_timer(self.reverse_timer_range)
            self.clockwise = not self.clockwise

        if time.time() - self.fire_timer_start >= self.fire_timer:
            self.fire_timer_start = time.time()
            self.fire_timer = self.calculate_timer(self.fire_timer_range)
            return self.fire()
        else:
            return None

    def calculate_timer(self, L):
        return random.random() * (L[1] - L[0] + L[0])
