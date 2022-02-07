import pygame
import random


class Npc(pygame.sprite.Sprite):

    def npc_turn(self, box_group, mark, board):
        """
            Ход компьютера
            Выбирается рандомное число и проверяется не занято ли та ячейка на поле
            Принимает группу спрайтов с ячейками поля, маркер игрока и игровое поле
        """
        check = True
        while check:
            xy = random.randrange(1, 101)
            check = board[(xy - 1) % 10][(xy - 1) // 10] == "X" or board[(xy - 1) % 10][(xy - 1) // 10] == "O"
        box_group.sprites()[xy-1].change(mark)
        board[(xy - 1) % 10][(xy - 1) // 10] = mark
