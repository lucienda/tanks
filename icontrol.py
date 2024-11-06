import pygame
from abc import ABC, abstractmethod

class IControl(ABC):
    @abstractmethod
    def handle_keys(self, mas) -> None:
        pass

    @abstractmethod
    def reset_keys(self) -> None:
        pass
