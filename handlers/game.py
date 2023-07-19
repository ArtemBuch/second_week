import os
import sys
import subprocess

try:
	import pygame
except ImportError:
	print("Установка зависимостей...\n")
	subprocess.check_call([sys.executable, "-m", "pip", "install", 'pygame'])
finally:
	import pygame

from .misc import *
from .processing import *
from .npc import *
from .box import *
from .sprite_input import *


class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init() #звук
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font(FONT_NAME)
        #Спрайты и изображения
        self.img()
        # Цикл игры
        self.game_over = True
        self.running = True
        self.end_screen


    def run(self):
        """
            Главный игровой цикл
        """
        while self.running:

            if self.game_over:
                self.show_go_screen()

            # Держим цикл на правильной скорости
            self.clock.tick(FPS)

            # Ввод процесса (события)
            self.event()

            # Обновление
            self.all_sprites.update()

            # Рендеринг
            self.screen.fill(BLACK)
            self.screen.blit(self.background, self.background_rect)
            self.all_sprites.draw(self.screen)

            # После отрисовки всего, переворачиваем экран
            pygame.display.flip()
        pygame.quit()


    def img(self):
        """
            Добавление фона и изображений спрайтов
        """
        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, 'img')
        self.background = pygame.image.load(os.path.join(self.img_folder, BACKGROUND)).convert()
        self.background_rect = self.background.get_rect()
        self.player_x_img = pygame.image.load(os.path.join(self.img_folder, PLAYERS_SCIN[0])).convert()
        self.player_o_img = pygame.image.load(os.path.join(self.img_folder, PLAYERS_SCIN[1])).convert()


    def sprites(self):
        """
            Создание игровых объектов(спрайтов) и добавление их группы
        """
        for x in range(1, 11):
            self.PLAY_BOARD.append(list())
            for y in range(1, 11):
                self.PLAY_BOARD[x - 1].append(y)
                self.new_box(x, y)
   

    def event(self):
        """
            Обработка нажатий на кнопки клавиатуры и мышки
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Выход
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in self.boxes if s.rect.collidepoint(pos)]
                if clicked_sprites:
                    if clicked_sprites[0].marked:
                        clicked_sprites[0].change(self.mark)
                        self.PLAY_BOARD[clicked_sprites[0].y][clicked_sprites[0].x] = self.mark
                        self.game_over = check_game_finish(self.PLAY_BOARD, self.mark, self.losing_player)
                        if self.game_over:
                            self.losing_player[0] = "You"
                            return self.end_screen()
                        self.mark = self.switch_player()
                        self.npc.npc_turn(self.boxes, self.mark, self.PLAY_BOARD)
                        self.game_over = check_game_finish(self.PLAY_BOARD, self.mark, self.losing_player)
                        if self.game_over:
                            self.losing_player[0] = "NPC"
                            return self.end_screen()
                        self.mark = self.switch_player()


    def draw_text(self, text, size, x, y):
        """
            Отображение на экране текста.
            Принимает текст, размер текста, координаты x и y
        """
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


    def show_go_screen(self):
        """
            Экран начала игры
        """
        self.screen.blit(self.background, self.background_rect)
        self.draw_text("Tic Tac Toe", 64, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Tic-Tac-Toe vice versa", 22,
                  WIDTH / 2, HEIGHT / 2)
        self.draw_text("Show what you can", 22,
                  WIDTH / 2, HEIGHT * 11 / 20)
        self.draw_text("START", 18, WIDTH / 2, HEIGHT * 3 / 4)
        self.wait_game()


    def player_input(self):
        """
            Экран выбора игровой роли: крестик или нолик 
        """
        sprite_input = pygame.sprite.Group()
        self.screen.blit(self.background, self.background_rect)
        self.draw_text("Tic Tac Toe", 64, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Do you want to play as X or O?", 22,
                  WIDTH / 2, HEIGHT / 2)
        
        self.sprite_input = Sprite_input(1, self.player_x_img, 'X')
        sprite_input.add(self.sprite_input)

        self.sprite_input = Sprite_input(3, self.player_o_img, 'O')
        sprite_input.add(self.sprite_input)

        sprite_input.draw(self.screen)
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.running = False
                   waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in sprite_input if s.rect.collidepoint(pos)]
                    if clicked_sprites:
                        self.mark = clicked_sprites[0].mark
                        waiting = False


    def new_box(self, x, y):
        """
            Создание новой игровой клетки на поле
            Принимает координаты X и Y 
        """
        self.box = (Box(x, y, self.player_x_img, self.player_o_img))
        self.all_sprites.add(self.box)
        self.boxes.add(self.box)


    def switch_player(self):
        """
            Переключение роли игрока для смены очереди для хода 
        """
        return 'O' if self.mark == 'X' else 'X'


    def end_screen(self):
        """
            Экран окончания игры и предложения новой игры
        """
        self.screen.blit(self.background, self.background_rect)
        self.draw_text("Tic Tac Toe", 64, WIDTH / 2, HEIGHT / 4)
        if self.losing_player[0] == "draw":
            self.draw_text(f"This round is a {self.losing_player[0]}!", 22,
                  WIDTH / 2, HEIGHT / 2)
        else:
            self.draw_text(f"{self.losing_player[0]} lost this round!", 22,
                  WIDTH / 2, HEIGHT / 2)
        
        self.draw_text("Shall we play AGAIN?", 22,
                  WIDTH / 2, HEIGHT * 11 / 20)   
        self.draw_text("START", 18, WIDTH / 2, HEIGHT * 3 / 4)
        self.wait_game()
        

    def new_game(self):
        """
            Обновление игрового поля и всех спрайтов для новой игры
        """
        self.game_over = False
        self.all_sprites = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()
        self.PLAY_BOARD = list()
        self.losing_player = ['']
        self.npc = Npc()
        self.sprites()


    def wait_game(self):
        """
            Обработка нажатий на кнопки клавиатуры и мышки при ожидании новой игры
        """
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.running = False
                   waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if ((event.pos[0] >= 276) and (event.pos[1] >= 450)) or ((event.pos[0] <= 325) and (event.pos[1] <= 466)):
                            waiting = False
                            self.player_input()
                            self.new_game()
