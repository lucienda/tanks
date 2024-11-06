import random
from iview import IView

class Barrier:
    def __init__(self, screen_size, view: IView) -> None:
        self.view = view
        self.screen_height = screen_size[0]
        self.screen_width = screen_size[1]
        self.xlocation  = (self.screen_width // 2) + random.randint(-int(0.1 * self.screen_width), int(0.1 * self.screen_width))
        self.random_height = random.randrange(int(self.screen_height * 0.1), int(self.screen_height * 0.3))
        self.color = (0, 0, 0)  
        self.ground_height = 35 
        self.barrier_width = 40

    def draw(self):
        self.view.draw_barrier(self)
