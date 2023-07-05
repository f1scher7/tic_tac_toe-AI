import sys
import pygame
import numpy as np

from constans import *


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")
screen.fill(BG_COLOR)


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS), dtype=int)
        self.empty_squares = self.squares
        self.marked_squares = 0

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


class Game:

    def __init__(self):
        self.board = Board()
        self.player = 1
        self.show_lines()

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


def main():

    game = Game()
    board = game.board

    # inc = 1

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
                    """
                    if inc % 2 != 0:
                        board.mark_squares(row, col, 1)
                    else:
                        board.mark_squares(row, col, 2)
                    inc += 1
                    """
                    board.mark_squares(row, col, game.player)
                    game.next_turn()
                    game.draw_fig(row, col)

        pygame.display.update()


main()
