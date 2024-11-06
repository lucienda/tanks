import random
from explosion import Explosion
from barrier import Barrier
from typing import List, Tuple
from view import IView

class Shell:
    def __init__(self, size: Tuple[int, int], xy: Tuple[int, int], tankx: int, tanky: int, currentTurPos: int,
                 gun_power: int, barrier: Barrier, targetX: int, targetY: int, view: IView, direction: str) -> None:
        self.size = list(size)
        self.xy = list(xy)
        self.tankx = tankx
        self.tanky = tanky
        self.currentTurPos = currentTurPos
        self.gun_power = gun_power
        self.barrier = barrier
        self.targetX = targetX
        self.targetY = targetY
        self.startingShell = list(xy)
        self.direction = direction
        self.view = view

    def fire(self) -> int:
        fire = True
        damage = 0
        while fire:
            self.view.draw_shell((self.startingShell[0], self.startingShell[1]), True)
            if self.direction == "LEFT":
                self.startingShell[0] -= (12 - self.currentTurPos) * 2
            else:
                self.startingShell[0] += (12 - self.currentTurPos) * 2
            self.startingShell[1] += int((((self.startingShell[0] - self.xy[0]) * 0.01 / (self.gun_power / 50.0)) ** 2) - (self.currentTurPos + self.currentTurPos / (12 - self.currentTurPos)))

            if self.startingShell[0] < 0 or self.startingShell[0] > self.size[0] or self.startingShell[1] < 0:
                hit_x = self.startingShell[0]
                hit_y = self.startingShell[1]
                explosion = Explosion(hit_x, hit_y, self.view)
                explosion.explode()
                fire = False

            if self.startingShell[1] > self.size[1] - self.barrier.ground_height:
                hit_x = int((self.startingShell[0] * (self.size[1] - self.barrier.ground_height)) / self.startingShell[1])
                hit_y = self.size[1] - self.barrier.ground_height
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
                explosion = Explosion(hit_x, hit_y, self.view)
                explosion.explode()
                fire = False

            check_x_1 = self.startingShell[0] <= self.barrier.xlocation + self.barrier.barrier_width
            check_x_2 = self.startingShell[0] >= self.barrier.xlocation
            check_y_1 = self.startingShell[1] <= self.size[1]
            check_y_2 = self.startingShell[1] >= self.size[1] - self.barrier.random_height - self.barrier.ground_height
            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = self.startingShell[0]
                hit_y = self.startingShell[1]
                explosion = Explosion(hit_x, hit_y, self.view)
                explosion.explode()
                fire = False
            self.view.draw_shell((0,0), False)

        return damage
