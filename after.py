import pygame
import sys
from game import Game, IView, IControl
from tanks import PlayerTank, EnemyTank
from barrier import Barrier
from health import HealthBar

def main():
    pygame.init()
    screen_height = 600
    screen_width = 800
    screen = pygame.display.set_mode((screen_width, screen_height))

    y = screen_height * 0.9
    x = screen_width * 0.9

    barrier = Barrier(screen, 35)
    health_bar = HealthBar(screen)
    tank = PlayerTank(screen, x, y)
    enemy_tank = EnemyTank(screen, screen_width - x, y)

    view = IView(screen, barrier, tank, enemy_tank, health_bar)
    control = IControl(tank, barrier, screen_width)
    
    game = Game(screen, tank, enemy_tank, barrier, view, control)
    
    game.run_game()

if __name__ == "__main__":
    main()