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

    def mark_squares(self, row, col, player):
        self.squares[row][col] = player

    def is_square_empty(self, row, col):
        if self.squares[row][col] != 0:
            return False
        return True


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
                    board.mark_squares(row, col, 1)
                    print(board.squares)

        pygame.display.update()


main()
