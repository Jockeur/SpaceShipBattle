import pygame
from pygame.locals import *

class Game:
    def __init__(self, res):
        self.res = res

        self.window_title = "SpaceShips Battle"
        self.is_running = True
        # self.clock = pygame.time.Clock()

        self.start()

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.res)
        pygame.display.set_caption(self.window_title)

        self.run()

    def run(self):
        while self.is_running:
            for e in pygame.event.get():
                self.manage_event(e)
            self.update()
        self.quit()

    def manage_event(self, e):
        if e.type == QUIT:
            self.is_running = False
        # On va gérer d'autres event

    def update(self):
        self.screen.fill(50)

        # self.clock.tick(50)
        pygame.display.flip()

    def quit(self):
        pygame.display.quit()
        pygame.quit()
        del self