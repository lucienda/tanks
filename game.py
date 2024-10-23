import pygame
import random
from typing import Tuple
from barrier import Barrier
from health import HealthBar
from fireshell import Shell
from tanks import Tank, EnemyTank

class IView:
    def __init__(self, screen, barrier=None, tank=None, enemy_tank=None, health_bar=None, colors=None, font=None, clock=None):
        self.screen = screen
        self.barrier = barrier
        self.tank = tank
        self.enemy_tank = enemy_tank
        self.health_bar = health_bar
        self.colors = colors or {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'bright_green': (0, 200, 0),
            'bright_red': (200, 0, 0)
        }
        self.font = font or pygame.font.SysFont('freesansbold.ttf', 25)
        self.clock = clock or pygame.time.Clock()

    def render(self) -> None:
        self.screen.fill(self.colors['white'])
        if self.barrier:
            self.barrier.draw()
        if self.tank:
            self.tank.draw()
        if self.enemy_tank:
            self.enemy_tank.draw()
        if self.health_bar:
            self.health_bar.draw()
        pygame.display.flip()

    def message_to_screen(self, msg: str, color: Tuple[int, int, int], size: int, x: int, y: int) -> None:
        font = pygame.font.SysFont('freesansbold.ttf', size)
        screen_text = font.render(msg, True, color)
        self.screen.blit(screen_text, (x, y))

    def button(self, x: int, inactive_color: Tuple[int, int, int], active_color: Tuple[int, int, int], action: str = None) -> None:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button_rect = pygame.Rect(x, 470, 100, 50)
        if button_rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, active_color, button_rect)
            if click[0] == 1 and action:
                if action == "play" or action == "play_again":
                    self.health_bar.enemy_health = 100
                    self.health_bar.player_health = 100
                    self.turn = True
                    self.shot = False
                    self.run_game()
                elif action == "quit":
                    pygame.quit()
        else:
            pygame.draw.rect(self.screen, inactive_color, button_rect)

    def button_font(self, value: str, button_width: int, button_height: int) -> None:
        small_text = pygame.font.Font('freesansbold.ttf', 20)
        text = small_text.render(value, True, self.colors['black'])
        text_rect = text.get_rect(center=(button_width, button_height))
        self.screen.blit(text, text_rect)

    def run(self) -> None:
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.screen.fill(self.colors['white'])
            text = self.font.render('Tank Wars', True, self.colors['black'], self.colors['white'])
            self.screen.blit(text, (120, 100))
            self.message_to_screen("Shoot the other tank to survive!", self.colors['red'], 40, 150, 260)
            self.message_to_screen("Press SPACE to shoot", self.colors['red'], 40, 150, 290)
            self.message_to_screen("Press Up or Down to move turret!", self.colors['red'], 40, 150, 320)
            self.message_to_screen("Press Left or Right to move tank!", self.colors['red'], 40, 150, 350)
            self.button(200, self.colors['green'], self.colors['bright_green'], "play")
            self.button_font('GO!', 250, 495)
            self.button(500, self.colors['red'], self.colors['bright_red'], "quit")
            self.button_font('Quit', 550, 495)
            pygame.display.update()
            self.clock.tick(5)

    def game_over(self) -> None:
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.screen.fill(self.colors['white'])
            basicfont = pygame.font.Font('freesansbold.ttf', 100)
            text = basicfont.render('Game Over!', True, (0, 0, 0), (255, 255, 255))
            self.screen.blit(text, (120, 100))
            self.message_to_screen("", self.colors['red'], 25, 80, 360)
            self.button(200, self.colors['green'], self.colors['bright_green'], "play_again")
            self.button_font('Play again', 250, 495)
            self.button(500, self.colors['red'], self.colors['bright_red'], "quit")
            self.button_font('Quit', 550, 495)
            pygame.display.update()
            self.clock.tick(5)

class IControl:
    def __init__(self, tank, barrier, screen_width):
        self.tank = tank
        self.barrier = barrier
        self.screen_width = screen_width
 
    def handle_tank_movement(self) -> None:
        if self.tank.move_left and self.tank.x - self.tank.tank_width // 2 > 0:
            if not (self.tank.x - self.tank.tank_width // 2 <= self.barrier.xlocation + self.barrier.barrier_width):
                self.tank.move(-1)
        
        if self.tank.move_right and self.tank.x + self.tank.tank_width // 2 < self.screen_width:
            if not (self.tank.x >= self.screen_width):
                self.tank.move(1)

    def handle_turret_rotation(self) -> None:
        if self.tank.turret_up and self.tank.turret_position < len(self.tank.possible_turrets) - 1:
            self.tank.change_turret("UP")
        
        if self.tank.turret_down and self.tank.turret_position > 0:
            self.tank.change_turret("DOWN")

    def handle_key_down(self, event) -> bool:
        if event.key == pygame.K_LEFT:
            self.tank.move_left = True
        elif event.key == pygame.K_RIGHT:
            self.tank.move_right = True
        elif event.key == pygame.K_UP:
            self.tank.turret_up = True
        elif event.key == pygame.K_DOWN:
            self.tank.turret_down = True
        elif event.key == pygame.K_SPACE:
            return True

    def handle_key_up(self, event) -> None:
        if event.key == pygame.K_LEFT:
            self.tank.move_left = False
        elif event.key == pygame.K_RIGHT:
            self.tank.move_right = False
        elif event.key == pygame.K_UP:
            self.tank.turret_up = False
        elif event.key == pygame.K_DOWN:
            self.tank.turret_down = False

class Game:
    def __init__(self, screen: pygame.Surface, tank: Tank, enemy_tank: EnemyTank, barrier: Barrier, view: IView, control: IControl) -> None:
        self.screen = screen
        self.view = view
        self.control = control
        self.tank = tank
        self.enemy_tank = enemy_tank
        self.barrier = barrier
        self.font = pygame.font.Font('freesansbold.ttf', 100)
        self.clock = pygame.time.Clock()
        self.health_bar = view.health_bar
        self.turn = True
        self.shot = False
        self.gun_power = 50

    def fire_shell(self) -> None:
        shell = Shell(self.screen, (self.tank.x, self.tank.y), self.tank.x, self.tank.y,
                    self.tank.turret_position, self.gun_power, self.barrier.xlocation, self.barrier.barrier_width,
                    self.barrier.random_height, self.enemy_tank.x, self.enemy_tank.y, self.barrier.ground_height, direction="LEFT")
        damage = shell.fire()
        self.health_bar.enemy_health -= damage
        print(f"Damage dealt: {damage}")

    def enemy_fire_shell(self) -> None:
        enemy_shell = Shell(self.screen, (self.enemy_tank.x, self.enemy_tank.y), self.enemy_tank.x, self.enemy_tank.y,
                            self.enemy_tank.turret_position, self.gun_power, self.barrier.xlocation, self.barrier.barrier_width,
                            self.barrier.random_height, self.tank.x, self.tank.y, self.barrier.ground_height, direction="RIGHT")
        damage = enemy_shell.fire()
        self.health_bar.player_health -= damage
        print(f"Damage dealt: {damage}")

    def run_game(self) -> None:
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if (self.control.handle_key_down(event)):
                        self.fire_shell() 
                        self.shot = True
                elif event.type == pygame.KEYUP:
                    self.control.handle_key_up(event)
            
            if self.turn:
                self.control.handle_tank_movement()
                self.control.handle_turret_rotation()
                if self.shot:
                    self.turn = False
                    self.shot = False
            else:
                self.enemy_tank.move_randomly()
                self.enemy_tank.change_turret()
                pygame.display.update()
                self.view.render()
                self.enemy_fire_shell()
                self.turn = True
                self.shot = False
            
            self.view.render()
            self.clock.tick(60)

            if self.health_bar.enemy_health <= 0 or self.health_bar.player_health <= 0:
                self.view.game_over()

        pygame.quit()