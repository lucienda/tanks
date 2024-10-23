import pygame
from typing import Tuple

class HealthBar:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.player_health = 5
        self.enemy_health = 5

    def message_to_screen(self, msg: str, color: Tuple[int, int, int], size: int, x: int, y: int) -> None:
        font = pygame.font.SysFont(None, size)
        screen_text = font.render(msg, True, color)
        self.screen.blit(screen_text, [x, y])

    def draw(self) -> None:
        player_health_color = self.get_health_color(self.player_health)
        enemy_health_color = self.get_health_color(self.enemy_health)

        pygame.draw.rect(self.screen, player_health_color, (680, 25, self.player_health, 25))
        pygame.draw.rect(self.screen, enemy_health_color, (20, 25, self.enemy_health, 25))

        self.message_to_screen(f"{self.player_health}%", self.black, 15, 710, 32)
        self.message_to_screen(f"{self.enemy_health}%", self.black, 15, 50, 32)

    def get_health_color(self, health: int) -> Tuple[int, int, int]:
        if health > 75:
            return self.green
        elif health >= 50:
            return self.yellow
        else:
            return self.red
