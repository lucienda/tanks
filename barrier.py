import pygame
import random

class Barrier:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.screen_height = self.screen.get_height()
        self.screen_width = self.screen.get_width()
        self.xlocation  = (self.screen_width // 2) + random.randint(-int(0.1 * self.screen_width), int(0.1 * self.screen_width))
        self.random_height = random.randrange(int(self.screen_height * 0.1), int(self.screen_height * 0.3))
        self.color = (0, 0, 0)  
        self.ground_height = 35 
        self.barrier_width = 40

    def draw(self) -> None:
        screen_height = self.screen.get_height()
        screen_width = self.screen.get_width()
        self.screen.fill((0, 255, 0), rect=[0, screen_height - self.ground_height, screen_width, self.ground_height])
        pygame.draw.rect(self.screen, self.color, (self.xlocation, screen_height - self.random_height - self.ground_height, self.barrier_width, self.random_height))
