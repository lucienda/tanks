import pygame
from abc import ABC, abstractmethod
from icontrol import IControl


class PlayerControl(IControl):
    keys = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_SPACE: False}

    def handle_keys(self, mas) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key in self.keys:
                    self.keys[event.key] = True

            if event.type == pygame.KEYUP:
                if event.key in self.keys:
                    self.keys[event.key] = False

        if self.keys[pygame.K_LEFT]:
            mas[0] = -5  
        elif self.keys[pygame.K_RIGHT]:
            mas[0] = 5 
        else:
            mas[0] = 0

        if self.keys[pygame.K_UP]:
            mas[1] = 1 
        elif self.keys[pygame.K_DOWN]:
            mas[1] = -1 
        else:
            mas[1] = 0  

        if self.keys[pygame.K_SPACE]:
            mas[2] = True

        return mas

    def reset_keys(self) -> None:
        for key in self.keys:
            self.keys[key] = False
