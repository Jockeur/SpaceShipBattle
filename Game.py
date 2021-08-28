import pygame
from pygame.locals import *

class Game:
    def __init__(self, res):
        self.res = res

        self.is_running = True

        self.start()

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.res)

        self.run()

    def run(self):
        while self.is_running:
            for e in pygame.event.get():
                self.manage_events(e)
            self.update()
        self.quit()

    def manage_events(self, e):
        if e.type == QUIT:
            self.is_running = False
        # On va gérer d'autres events

    def update(self):
        self.screen.fill(50)

        pygame.display.flip()

    def quit(self):
        pygame.quit()
        del self
