from .misc import *

def check_game_finish(board, mark, losing_player):
    """
        Проверка проиграл ли игрок с указанным маркером игру
        Или поле запонилось и игра закончилась ничьей
        Принимает игровое поле, маркер игрока и переменную для отображения проигравшего игрока
    """
    for col in range(6):
        for row in range(6):
            if check_diag(board, mark, col, row) or check_cols_rows(board, mark, col, row): return True
    if full_board_check(board):
        losing_player[0] = "draw"
        return True
    return False

def check_diag(board, mark, offset_x, offset_y):
    """
        Проверка диагоналей
        Принимает игровое поле, маркер игрока и смещение по X и Y
    """
    right_diag = True
    left_diag = True
    for i in range(NUM_TO_DEFEAT):
        right_diag = right_diag and (board[i + offset_x][i + offset_y] == mark)
        left_diag = left_diag and (board[NUM_TO_DEFEAT - i + offset_x - 1][i + offset_y] == mark)
    return right_diag or left_diag

def check_cols_rows(board, mark, offset_x, offset_y):
    """
        Проверка столбцов и строк
        Принимает игровое поле, маркер игрока и смещение по X и Y
    """
    for col in range(offset_x, NUM_TO_DEFEAT + offset_x):
        cols = True
        rows = True
        for row in range(offset_y, NUM_TO_DEFEAT + offset_y):
            cols = cols and (board[col][row] == mark)
            rows = rows and (board[row][col] == mark)
        if (cols or rows): return True
    return False

def full_board_check(board):
    """
        Определяет что поле запонилось и игра закончилась ничьей
        Принимает игровое поле
    """
    board_set = set()
    for i in board:
        board_set.update(set(i))
    return len(board_set) == 2
