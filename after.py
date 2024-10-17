import pygame
import sys
from menu import Menu

# Пример использования класса Menu
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    menu = Menu(screen)
    menu.run()

if __name__ == "__main__":
    main()
