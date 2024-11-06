import pygame
import random
from typing import Tuple
from view import IView

class Explosion:
    def __init__(self, x: int, y: int, view: IView, explosion_size: int = 50) -> None:
        self.x = x
        self.y = y
        self.explosion_size = explosion_size
        self.color_choices = [(255, 0, 0), (255, 69, 0), (0, 255, 0), (0, 200, 0), (255, 255, 0)]
        self.view = view

    def explode(self) -> None:
        explode = True
        while explode:
            magnitude = 1
            while magnitude < self.explosion_size:
                exploding_bit_x = self.x + random.randrange(-1 * magnitude, magnitude)
                exploding_bit_y = self.y + random.randrange(-1 * magnitude, magnitude)

                self.view.draw_explosion((exploding_bit_x, exploding_bit_y))
                magnitude+=1
            explode = False
