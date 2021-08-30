import pygame


def text_surface(text, size, color, font):
    text_font = pygame.font.SysFont(font, size)
    return text_font.render(text, True, color)


def screen_text(text, size, color, frame, pos, font="res/fonts/Calibri 400.tff"):
    surface = text_surface(text, size, color, font)
    rect = surface.get_rect()
    frame.blit(surface, (pos[0] - rect.w/2, pos[1] - rect.h/2))
