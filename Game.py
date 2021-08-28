import pygame
from pygame.locals import *

class Game:
    def __init__(self, res):
        self.res = res

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.res)

        self.run

    def run(self):
        pass

    def manage_events(self):
        pass

    def update(self):
        pass

    def quit(self):
        pygame.quit()
        del self