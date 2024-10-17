import pygame
import random
from explosion import Explosion
from typing import List, Tuple

class Shell:
    def __init__(self, screen: pygame.Surface, xy: Tuple[int, int], tankx: int, tanky: int, currentTurPos: int,
                 gun_power: int, xlocation: int, barrier_width: int, randomHeight: int, targetX: int, targetY: int,
                 ground_height: int, direction: str = "LEFT") -> None:
        self.screen = screen
        self.xy = list(xy)
        self.tankx = tankx
        self.tanky = tanky
        self.currentTurPos = currentTurPos
        self.gun_power = gun_power
        self.xlocation = xlocation
        self.barrier_width = barrier_width
        self.randomHeight = randomHeight
        self.targetX = targetX
        self.targetY = targetY
        self.ground_height = ground_height
        self.startingShell = list(xy)
        self.direction = direction

    def fire(self) -> int:
        fire = True
        damage = 0
        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame.draw.circle(self.screen, (255, 0, 0), (self.startingShell[0], self.startingShell[1]), 5)
            if self.direction == "LEFT":
                self.startingShell[0] -= (12 - self.currentTurPos) * 2
            else:
                self.startingShell[0] += (12 - self.currentTurPos) * 2
            self.startingShell[1] += int((((self.startingShell[0] - self.xy[0]) * 0.01 / (self.gun_power / 50.0)) ** 2) - (self.currentTurPos + self.currentTurPos / (12 - self.currentTurPos)))

            # Проверка, чтобы снаряд не выходил за границы экрана
            if self.startingShell[0] < 0 or self.startingShell[0] > self.screen.get_width() or self.startingShell[1] < 0:
                hit_x = self.startingShell[0]
                hit_y = self.startingShell[1]
                explosion = Explosion(self.screen, hit_x, hit_y)
                explosion.explode()
                fire = False

            if self.startingShell[1] > self.screen.get_height() - self.ground_height:
                hit_x = int((self.startingShell[0] * (self.screen.get_height() - self.ground_height)) / self.startingShell[1])
                hit_y = self.screen.get_height() - self.ground_height
                if self.targetX + 10 > hit_x > self.targetX - 10:
                    print("CRITICAL HIT")
                    damage = 25
                elif self.targetX + 15 > hit_x > self.targetX - 15:
                    print("HARD HIT")
                    damage = 18
                elif self.targetX + 25 > hit_x > self.targetX - 25:
                    print("MEDIUM HIT")
                    damage = 10
                elif self.targetX + 35 > hit_x > self.targetX - 35:
                    print("LIGHT HIT")
                    damage = 5
                explosion = Explosion(self.screen, hit_x, hit_y)
                explosion.explode()
                fire = False

            check_x_1 = self.startingShell[0] <= self.xlocation + self.barrier_width
            check_x_2 = self.startingShell[0] >= self.xlocation
            check_y_1 = self.startingShell[1] <= self.screen.get_height()
            check_y_2 = self.startingShell[1] >= self.screen.get_height() - self.randomHeight - self.ground_height
            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = self.startingShell[0]
                hit_y = self.startingShell[1]
                explosion = Explosion(self.screen, hit_x, hit_y)
                explosion.explode()
                fire = False

            pygame.display.update()
            pygame.time.Clock().tick(60)
        return damage
