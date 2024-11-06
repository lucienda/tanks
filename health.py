from typing import Tuple
from iview import IView

class HealthBar:
    def __init__(self, view: IView) -> None:
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.player_health = 10
        self.enemy_health = 10
        self.view = view

    def get_health_color(self, health: int) -> Tuple[int, int, int]:
        if health > 75:
            return self.green
        elif health >= 50:
            return self.yellow
        else:
            return self.red
        
    def draw(self):
        self.view.draw_health(self)
    
