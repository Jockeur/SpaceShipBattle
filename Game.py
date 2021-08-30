import pygame
from pygame.locals import *
from SpaceShip import *
from EnemyManager import *


class Game:
    def __init__(self, res):
        self.res = res

        self.bords = [
            [-30, self.res[0] + 30],
            [-30, self.res[1] + 30]
        ]

        self.player_bords = [[10, self.res[0] - 10],
                             [10, self.res[1] - 10]]

        self.window_title = "SpaceShips Battle"
        self.is_running = True

        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load("res/bg/fond.png")
        self.bg_img = pygame.transform.scale2x(self.bg)

        self.player_ship_image = pygame.image.load("res/sprites/spaceship.png")
        self.bullet_image = pygame.image.load("res/sprites/bullet.png")

        self.player = SpaceShip((self.res[0]/2, self.res[1]/2), 10, self.player_ship_image, self.bullet_image)

        self.player_bullet_group = pygame.sprite.Group()

        self.enemy_manager = EnemyManager(res, self.player)

        self.start()

    def start(self):
        print('Starting...')
        pygame.init()
        print('Pygame initializated')
        self.screen = pygame.display.set_mode(self.res)
        print('Window opened')
        pygame.display.set_caption(self.window_title)
        print('Initializing player')

        self.run()

    def run(self):
        while self.is_running:
            for e in pygame.event.get():
                self.manage_events(e)
            self.manage_pressed_keys()
            self.update()
        self.quit()

    def manage_events(self, e):
        if e.type == QUIT:
            self.is_running = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                bullet = self.player.fire()
                if bullet:
                    self.player_bullet_group.add(bullet)

    def manage_pressed_keys(self):
        pressed = pygame.key.get_pressed()

        vector = [0, 0]
        if pressed[K_q] or pressed[K_LEFT]:
            vector[0] -= 1
        if pressed[K_d] or pressed[K_RIGHT]:
            vector[0] += 1
        if pressed[K_s] or pressed[K_DOWN]:
            vector[1] += 1
        if pressed[K_z] or pressed[K_UP]:
            vector[1] -= 1

        self.player.move(vector[0], vector[1])

        # x
        if self.player.pos[0] < self.player_bords[0][0]:
            self.player.pos = (self.player_bords[0][0], self.player.pos[1])
        elif self.player.pos[0] > self.player_bords[0][1]:
            self.player.pos = (self.player_bords[0][1], self.player.pos[1])

        # y
        if self.player.pos[1] < self.player_bords[1][0]:
            self.player.pos = (self.player.pos[0], self.player_bords[1][0])
        elif self.player.pos[1] > self.player_bords[1][1]:
            self.player.pos = (self.player.pos[0], self.player_bords[1][1])

    def draw(self):
        self.screen.blit(self.player.image, self.player.rect)

        self.enemy_manager.draw(self.screen)

        self.player_bullet_group.draw(self.screen)

    def clear_bullets(self):
        for bullet in self.player_bullet_group.sprites():
            if bullet.rect.centerx < self.bords[0][0] or bullet.rect.centerx > self.bords[0][1]:
                self.player_bullet_group.remove(bullet)
            if bullet.rect.centery < self.bords[1][0] or bullet.rect.centery > self.bords[1][1]:
                self.player_bullet_group.remove(bullet)
            if bullet not in self.player_bullet_group.sprites():
                del bullet

    def update(self):
        self.screen.blit(self.bg_img, (0, 0))

        self.clear_bullets()

        self.player.update()
        self.player_bullet_group.update()

        self.enemy_manager.update()

        self.draw()

        self.clock.tick(50)
        pygame.display.flip()

    def quit(self):
        pygame.display.quit()
        pygame.quit()
        print('Stopping the game')
        del self
