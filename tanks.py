import pygame
import random
from typing import List, Tuple

class Tank:
    def __init__(self, screen: pygame.Surface, x: int, y: int) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.color = (0, 0, 0)
        self.tank_width = 40
        self.tank_height = 20
        self.turret_width = 5
        self.wheel_width = 5
        self.turret_position = 8
        self.move_left = False
        self.move_right = False
        self.turret_up = False
        self.turret_down = False

    def draw(self) -> None:
        self.update_turrets()
        turret = self.possible_turrets[self.turret_position]
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.tank_height // 2)
        pygame.draw.rect(self.screen, self.color, (self.x - self.tank_height, self.y, self.tank_width, self.tank_height))
        pygame.draw.line(self.screen, self.color, (self.x, self.y), turret, self.turret_width)
        wheels = [(self.x, self.y + 23), (self.x + 5, self.y + 23), (self.x - 5, self.y + 23),
                  (self.x + 10, self.y + 23), (self.x - 10, self.y + 23), (self.x + 15, self.y + 23),
                  (self.x - 15, self.y + 23)]
        for wheel in wheels:
            pygame.draw.circle(self.screen, self.color, wheel, self.wheel_width)

    def move(self, dx: int) -> None:
        self.x += dx
        self.update_turrets()

    def update_turrets(self) -> None:
        self.possible_turrets = [(self.x - 27, self.y - 2), (self.x - 26, self.y - 5),
                                 (self.x - 25, self.y - 8), (self.x - 23, self.y - 12),
                                 (self.x - 21, self.y - 14), (self.x - 20, self.y - 17),
                                 (self.x - 18, self.y - 19), (self.x - 16, self.y - 21),
                                 (self.x - 14, self.y - 23)]
        
    def change_turret(self, direction: str) -> None:
        if direction == "UP":
            if self.turret_position < len(self.possible_turrets) - 1:
                self.turret_position += 1
        elif direction == "DOWN":
            if self.turret_position > 0:
                self.turret_position -= 1

class PlayerTank(Tank):
    def update_turrets(self) -> None:
        self.possible_turrets = [(self.x - 27, self.y - 2), (self.x - 26, self.y - 5),
                                 (self.x - 25, self.y - 8), (self.x - 23, self.y - 12),
                                 (self.x - 21, self.y - 14), (self.x - 20, self.y - 17),
                                 (self.x - 18, self.y - 19), (self.x - 16, self.y - 21),
                                 (self.x - 14, self.y - 23)]

    def draw(self) -> None:
        super().draw()

    def move(self, dx: int) -> None:
        super().move(dx)

    def change_turret(self, direction: str) -> None:
        super().change_turret(direction)

class EnemyTank(Tank):
    def update_turrets(self) -> None:
        self.possible_turrets = [(self.x + 27, self.y - 2), (self.x + 26, self.y - 5), 
                                 (self.x + 25, self.y - 8), (self.x + 23, self.y - 12), 
                                 (self.x + 21, self.y - 14), (self.x + 20, self.y - 17), 
                                 (self.x + 18, self.y - 19), (self.x + 16, self.y - 21), 
                                 (self.x + 14, self.y - 23)]
        
    def draw(self) -> None:
        super().draw()

    def move_randomly(self) -> None:
        move_direction = random.choice(["LEFT", "RIGHT", "STAY"])
        if move_direction == "LEFT" and self.x - self.tank_width // 2 > 0:
            self.move(-5)
        elif move_direction == "RIGHT" and self.x + self.tank_width // 2 < self.screen.get_width():
            self.move(5)

    def change_turret(self) -> None:
        move_direction = random.choice(["UP", "DOWN", "STAY"])
        super().change_turret(move_direction)
