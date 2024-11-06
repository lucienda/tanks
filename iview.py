from abc import ABC, abstractmethod
class IView(ABC):
    @abstractmethod
    def initialization(self, screen_size) -> None:
        pass

    @abstractmethod
    def message_to_screen(self, msg, color, size, x, y) -> None:
        pass

    @abstractmethod
    def button_type(self, x, inactive_color, active_color, action=None) -> bool:
        pass

    @abstractmethod
    def button_font(self, value, button_width, button_height) -> None:
        pass

    @abstractmethod
    def start_menu(self) -> bool:
        pass

    @abstractmethod
    def draw_game(self, tank, bot, barrier, health) -> None:
        pass

    @abstractmethod
    def draw_tank(self, tank) -> None:
        pass

    @abstractmethod
    def draw_barrier(self, barrier) -> None:
        pass

    @abstractmethod
    def draw_health(self, health) -> None:
        pass

    @abstractmethod
    def draw_shell(self, position, flag=True) -> None:
        pass

    @abstractmethod
    def draw_explosion(self, position) -> None:
        pass

    @abstractmethod
    def game_over(self) -> bool:
        pass