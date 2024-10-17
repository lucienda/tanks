import pygame
import random
from typing import Tuple

class Explosion:
    def __init__(self, screen: pygame.Surface, x: int, y: int, explosion_size: int = 50) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.explosion_size = explosion_size
        self.color_choices = [(255, 0, 0), (255, 69, 0), (0, 255, 0), (0, 200, 0), (255, 255, 0)]

    def explode(self) -> None:
        explode = True
        while explode:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            magnitude = 1
            while magnitude < self.explosion_size:
                exploding_bit_x = self.x + random.randrange(-1 * magnitude, magnitude)
                exploding_bit_y = self.y + random.randrange(-1 * magnitude, magnitude)
                pygame.draw.circle(self.screen, random.choice(self.color_choices), (exploding_bit_x, exploding_bit_y), random.randrange(1, 5))
                magnitude += 1
                pygame.display.update()
                pygame.time.Clock().tick(100)
            explode = False
