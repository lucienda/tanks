import pygame
import sys
from game import Game, IControl, IView
from tanks import Tank, PlayerTank, EnemyTank

# Пример использования класса Menu
def main():
    pygame.init()
    screen_height = 600
    screen_wigth = 800
    screen = pygame.display.set_mode((screen_wigth, screen_height))
    
    menu = Game(screen)
    y = screen_height * 0.9
    x = screen_height * 0.9
    tank = PlayerTank(screen, x, y)
    enemy_tank = EnemyTank(screen, screen_height - x, y)
    control = IControl()
    view = IView()

    Game(tank, enemy_tank, view, control)
    

    menu.run()

if __name__ == "__main__":
    main()
