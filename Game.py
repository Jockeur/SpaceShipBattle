import pygame
from pygame.locals import *
from SpaceShip import *
from EnemyManager import *
import time
import colorsys
import json

from Text import *
pygame.mixer.init()
pygame.joystick.init()


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
        self.is_running = False

        self.true = True
        self.game_over_true = False

        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load("res/bg/fond.png")
        self.bg_img = pygame.transform.scale2x(self.bg)

        self.player_ship_image = pygame.image.load("res/sprites/spaceship.png")
        self.bullet_image = pygame.image.load("res/sprites/bullet.png")

        self.player = SpaceShip((self.res[0] / 2, self.res[1] / 2), 10, self.player_ship_image, self.bullet_image)

        self.player_bullet_group = pygame.sprite.Group()

        self.enemy_manager = EnemyManager(res, self.player)

        self.score = 0
        self.score_font_size = 40
        self.score_text_pos = (self.res[0] / 2, 30)

        self.game_over_timer = 2
        self.game_over_timer_start = 0

        self.banner = pygame.image.load('res/images/banner.png')

        self.play_button = pygame.image.load('res/images/play.png')
        self.play_button_rect = self.play_button.get_rect()

        self.quit_button = pygame.image.load('res/images/quit.png')
        self.quit_button_rect = self.quit_button.get_rect()

        self.menu_button = pygame.image.load('res/images/menu.png')
        self.menu_button_rect = self.menu_button.get_rect()

        self.highscore = {}

        self.joystick = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        self.vector = [0, 0]

        self.start()

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption(self.window_title)
        pygame.display.set_icon(self.player_ship_image)

        self.run()

    def run(self):
        try:
            while self.true:
                for e in pygame.event.get():
                    self.manage_events(e)

                self.manage_pressed_keys()
                self.update()
        except pygame.error:
            pass

    def manage_events(self, e):
        if e.type == QUIT:
            self.quit()

        if e.type == MOUSEBUTTONDOWN:
            if self.play_button_rect.collidepoint(pygame.mouse.get_pos()):
                self.is_running = True

        if e.type == JOYBUTTONUP:
            if e.button == 0:
                if not self.is_running:
                    self.is_running = True
            if e.button == 1:
                bullet = self.player.fire()
                if bullet:
                    self.player_bullet_group.add(bullet)

        if e.type == JOYAXISMOTION:
            if e.axis < 2:
                self.vector[e.axis] = round(e.value)

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                bullet = self.player.fire()
                if bullet:
                    self.player_bullet_group.add(bullet)

    def manage_pressed_keys(self):
        pressed = pygame.key.get_pressed()

        if pressed[K_q] or pressed[K_LEFT]:
            self.vector[0] -= 1
        if pressed[K_d] or pressed[K_RIGHT]:
            self.vector[0] += 1
        if pressed[K_s] or pressed[K_DOWN]:
            self.vector[1] += 1
        if pressed[K_z] or pressed[K_UP]:
            self.vector[1] -= 1
        self.player.move(self.vector[0], self.vector[1])

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

    def manage_collision(self):
        for enemy in self.enemy_manager.sprite_group.sprites():
            for bullet in pygame.sprite.spritecollide(enemy, self.player_bullet_group, False):
                enemy.kill()
                bullet.kill()
                enemy.play_explo_sound()
                del enemy
                del bullet
                self.score += 1

        for bullet in pygame.sprite.spritecollide(self.player, self.enemy_manager.bullet_group, False):
            bullet.kill()
            self.player.play_explo_sound()

            del bullet
            del self.player
            self.game_over()

    def draw_score(self):
        screen_text(f"Score : {str(self.score)}", self.score_font_size, pygame.Color(255, 255, 255, 255), self.screen, self.score_text_pos)

    def clear_bullets(self, group):
        for bullet in group.sprites():
            if bullet.rect.centerx < self.bords[0][0] or bullet.rect.centerx > self.bords[0][1]:
                group.remove(bullet)
            if bullet.rect.centery < self.bords[1][0] or bullet.rect.centery > self.bords[1][1]:
                group.remove(bullet)
            if bullet not in group.sprites():
                del bullet

    def update(self):
        self.screen.blit(self.bg_img, (0, 0))

        self.clear_bullets(self.player_bullet_group)
        self.clear_bullets(self.enemy_manager.bullet_group)

        if self.is_running:

            self.player.update()
            self.player_bullet_group.update()

            self.enemy_manager.update()
            self.draw_score()

            self.draw()

            self.manage_collision()

        else:
            self.screen.blit(self.banner, (self.res[0]/2 - 181, self.res[1]/2 - 70))
            self.screen.blit(self.play_button, self.play_button_rect.topleft)
            self.play_button_rect.topleft = self.res[0]/2 - 56, self.res[1]/2 + 75
            if pygame.joystick.get_count() >= 1:
                screen_text('Press A / X to start', 40, pygame.Color(255, 255, 255, 255), self.screen, (self.res[0]/2 - 13, self.res[1]/2 + 145))

        self.clock.tick(50)
        pygame.display.flip()

    def game_over(self):
        self.game_over_true = True
        self.game_over_timer_start = time.time()
        while self.game_over_true:
            self.screen.blit(self.bg_img, (0, 0))

            screen_text("Game Over", 70, pygame.Color(255, 0, 0, 255), self.screen, (self.res[0]/2, self.res[1]/2))
            screen_text(f"Score : {str(self.score)}", 50, pygame.Color(255, 255, 255, 255), self.screen, (self.res[0] / 2, self.res[1] / 2 + 50))

            self.screen.blit(self.quit_button, self.quit_button_rect.topleft)
            self.quit_button_rect.topleft = (self.res[0]/2 - 50, self.res[1]/2 + 75)
            self.screen.blit(self.menu_button, self.menu_button_rect.topleft)
            self.menu_button_rect.topleft = (self.res[0]/2 - 50, self.res[1]/2 + 130)
            for e in pygame.event.get():
                if e.type == MOUSEBUTTONDOWN:
                    if self.quit_button_rect.collidepoint(e.pos):
                        self.game_over_true = False
                    if self.menu_button_rect.collidepoint(e.pos):
                        self.is_running = False
                        self.__init__((1200, 720))

                if e.type == JOYBUTTONUP:
                    if e.button == 1:
                        self.quit()
                    if e.button == 0:
                        self.is_running = False
                        self.__init__((1200, 720))

            pygame.display.flip()

        self.is_running = False
        self.quit()

    def restart(self):
        pass

    def quit(self):
        pygame.display.quit()
        pygame.quit()
        del self
