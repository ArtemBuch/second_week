from .misc import *
import pygame


class Box(pygame.sprite.Sprite):
    """
        Создает ячейку поля
    """
    def __init__(self, x, y, player_x_img, player_o_img):
        """
        Принимает координаты X и Y, и спрайты маркеров игрока(X и O)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.player_x_img = player_x_img
        self.player_o_img = player_o_img
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH * x / 11, HEIGHT * y / 11)
        self.marked = 1
        self.x = x - 1
        self.y = y - 1

    def change(self, mark):
        """
            Замена спрайта ячейки поля на которую поставили крестик или нолик
            Принимает маркер игрока
        """
        self.image = self.player_x_img if mark == 'X' else self.player_o_img
        self.image.set_colorkey(BLACK)
        self.marked = 0
