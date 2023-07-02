import sys
import pygame
import constans

pygame.init()
screen = pygame.display.set_mode((constans.WIDTH, constans.HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


main()
