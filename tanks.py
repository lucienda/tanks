from abc import ABC, abstractmethod
import random
from control import IControl
from iview import IView

class IPlayer(ABC):
    @abstractmethod
    def move(self, mas):
        pass

    @abstractmethod
    def change_turret(self, direction: int):
        pass

    @abstractmethod
    def reset_position(self, x: int, y: int):
        pass

    @abstractmethod
    def update_turrets(self):
        pass

    @abstractmethod
    def draw(self):
        pass

class PlayerTank(IPlayer):
    def __init__(self, x: int, y: int, control: IControl, view: IView) -> None:
        self.x = x
        self.y = y
        self.control = control
        self.color = (0, 0, 0)
        self.tank_width = 40
        self.tank_height = 20
        self.turret_width = 5
        self.wheel_width = 5
        self.turret_position = 7 
        self.possible_turrets = self.calculate_possible_turrets()
        self.view = view

    def move(self, mas) -> None:
        if (mas == [0,0,False]):
            mas = self.control.handle_keys(mas)  
             
        self.x += mas[0]
        self.change_turret(mas[1])
        
    def change_turret(self, dy: int) -> None:
        self.turret_position += dy
        self.turret_position = max(0, min(self.turret_position, len(self.possible_turrets) - 1))
        self.update_turrets()

    def reset_position(self, x: int, y: int):
        self.x = x
        self.y = y
        self.turret_position = 7
        self.update_turrets()
        self.control.reset_keys()

    def update_turrets(self) -> None:
        self.possible_turrets = self.calculate_possible_turrets()

    def calculate_possible_turrets(self):
        return [
            (self.x - 27, self.y - 2), (self.x - 26, self.y - 5),
            (self.x - 25, self.y - 8), (self.x - 23, self.y - 12),
            (self.x - 21, self.y - 14), (self.x - 20, self.y - 17),
            (self.x - 18, self.y - 19), (self.x - 16, self.y - 21),
            (self.x - 14, self.y - 23)
        ]
    
    def draw(self):
        self.view.draw_tank(self)

class EnemyTank(IPlayer):
    def __init__(self, x: int, y: int, view: IView) -> None:
        self.x = x
        self.y = y
        self.color = (0, 0, 0)
        self.tank_width = 40
        self.tank_height = 20
        self.turret_width = 5
        self.wheel_width = 5
        self.turret_position = 7 
        self.possible_turrets = self.calculate_possible_turrets()
        self.view = view

    def move(self) -> None:
        direction = random.randint(-20, 20)
        if self.x + direction >= 0:

            self.x += direction
            self.change_turret()

    def change_turret(self) -> None:
        #self.turret_position += dy
        self.turret_position = random.randint(0, len(self.possible_turrets) - 1)
        self.update_turrets()

    def reset_position(self, x: int, y: int):
        self.x = x
        self.y = y
        self.turret_position = 7
        self.update_turrets()

    def update_turrets(self) -> None:
        self.possible_turrets = self.calculate_possible_turrets()

    def calculate_possible_turrets(self):
        return [
            (self.x + 27, self.y - 2), (self.x + 26, self.y - 5),
            (self.x + 25, self.y - 8), (self.x + 23, self.y - 12),
            (self.x + 21, self.y - 14), (self.x + 20, self.y - 17),
            (self.x + 18, self.y - 19), (self.x + 16, self.y - 21),
            (self.x + 14, self.y - 23)
        ]

    def draw(self):
        self.view.draw_tank(self)