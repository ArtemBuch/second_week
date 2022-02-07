from .misc import *
import pygame


class Sprite_input(pygame.sprite.Sprite):
    """
        Создание спрайтов для выбора игровой роли(Х или О)
    """
    def __init__(self, x, player_img, mark):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * x / 4, HEIGHT * 13 / 20)
        self.mark = mark
