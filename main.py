import copy
import sys
import pygame
import numpy as np

from random import randrange
from constans import *


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")
screen.fill(BG_COLOR)


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS), dtype=int)
        self.marked_squares = 0

    def final_state(self):
        """
        @return 0 if there is a tie
        @return 1 if player 1. wins
        @return 2 if player 2. wins
        """

        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] == 1:
                return 1
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] == 2:
                return 2
            """
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
            """

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]

        # first diagonal
        first_diagonal = []
        for row in range(ROWS):
            for col in range(COLS):
                if row == col:
                    first_diagonal.append(self.squares[row][col])
        if first_diagonal.count(1) == len(first_diagonal):
            return 1
        if first_diagonal.count(2) == len(first_diagonal):
            return 2

        # second diagonal
        reversed_board = self.squares[::-1]
        second_diagonal = []
        for row in range(ROWS):
            for col in range(COLS):
                if row == col:
                    second_diagonal.append(reversed_board[row][col])
        if second_diagonal.count(1) == len(second_diagonal):
            return 1
        if second_diagonal.count(2) == len(second_diagonal):
            return 2

        del reversed_board
        del first_diagonal
        del second_diagonal

        return 0

    def mark_squares(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def is_square_empty(self, row, col):
        if self.squares[row][col] != 0:
            return False
        return True

    def empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.is_square_empty(row, col):
                    empty_squares.append((row, col))
        return empty_squares

    def is_board_full(self):
        if self.marked_squares == 9:
            return True
        return False

    def is_board_empty(self):
        if self.marked_squares == 0:
            return True
        return False


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def random_choice(self, board):
        empty_squares = board.empty_squares()
        rnd_index = randrange(0, len(empty_squares))
        return empty_squares[rnd_index]     # return (row, col)

    def minimax(self, board, maximizing):
        # terminal case
        case = board.final_state()
        # player 1 wins
        if case == 1:
            return 1, None
        # player 2 wins
        if case == 2:
            return -1, None
        # tie
        elif board.is_board_full():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_squares = board.empty_squares()
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_squares(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_squares = board.empty_squares()
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_squares(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = "random"
            move = self.random_choice(main_board)

        else:
            # minimax algorythm choice
            eval, move = self.minimax(main_board, False)
        print(f'AI has chosen to mark the square in pos {move} with an eval {eval}')
        return move


class Game:

    def __init__(self):
        self.board = Board()
        # self.ai = AI()
        self.player = 1
        self.game_mode = "ai"  # pvp or ai
        self.running = True
        self.show_lines()

    def draw_move(self, row, col):
        self.board.mark_squares(row, col, self.player)
        self.next_turn()
        self.draw_fig(row, col)

    def show_lines(self):
        # vertical
        pygame.draw.line(screen, LINE_COLOR, (SQ_SIZE, 0), (SQ_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (2 * SQ_SIZE, 0), (2 * SQ_SIZE, HEIGHT), LINE_WIDTH)
        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQ_SIZE), (WIDTH, SQ_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQ_SIZE), (WIDTH, SQ_SIZE * 2), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 2:
            # desc line
            start_desc = (col * SQ_SIZE + OFFSET, row * SQ_SIZE + OFFSET)
            end_desc = (col * SQ_SIZE + SQ_SIZE - OFFSET, row * SQ_SIZE + SQ_SIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # asc line
            start_asc = (col * SQ_SIZE + OFFSET, row * SQ_SIZE + SQ_SIZE - OFFSET)
            end_asc = (col * SQ_SIZE + SQ_SIZE - OFFSET, row * SQ_SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 1:
            center = (col * SQ_SIZE + SQ_SIZE//2, row * SQ_SIZE + SQ_SIZE//2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_game_mode(self):
        if self.game_mode == "pvp":
            self.game_mode = "ai"
        else:
            self.game_mode = "pvp"




def main():

    game = Game()
    board = game.board
    ai = AI()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = list(event.pos)
                row = click_pos[1] // SQ_SIZE
                col = click_pos[0] // SQ_SIZE

                if board.is_square_empty(row, col):
                    game.draw_move(row, col)

            if event.type == pygame.KEYDOWN:

                # g - game mode
                if event.key == pygame.K_g:
                    game.change_game_mode()

                # 0 - random ai
                if event.key == pygame.K_0:
                    ai.level = 0

                # 1 - random ai
                if event.key == pygame.K_1:
                    ai.level = 1

        if game.game_mode == "ai" and game.player == ai.player:
            pygame.display.update()
            row, col = ai.eval(board)
            pygame.time.delay(500)
            game.draw_move(row, col)

        pygame.display.update()


main()
