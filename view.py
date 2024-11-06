import pygame
from abc import ABC, abstractmethod
from tanks import PlayerTank, EnemyTank, IPlayer
from barrier import Barrier
from health import HealthBar
import random
from iview import IView

class GameView(IView):
    def initialization(self, screen_size) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('Tanks')
        self.clock = pygame.time.Clock()

    def message_to_screen(self, msg, color, size, x, y) -> None:
        font = pygame.font.SysFont('freesansbold.ttf', size)
        screen_text = font.render(msg, True, color)
        self.screen.blit(screen_text, (x, y))

    def button_type(self, x, inactive_color, active_color, action=None) -> bool:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        button_rect = pygame.Rect(x, 470, 100, 50)
        if button_rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, active_color, button_rect)
            if click[0] == 1 and action:
                if action == "play" or action == "play_again":
                    return True
                elif action == "quit":
                    pygame.quit()
                    quit()
        else:
            pygame.draw.rect(self.screen, inactive_color, button_rect)

    def button_font(self, value, button_width, button_height) -> None:
        small_text = pygame.font.Font('freesansbold.ttf', 20)
        text = small_text.render(value, True, (0, 0, 0))
        text_rect = text.get_rect(center=(button_width, button_height))
        self.screen.blit(text, text_rect)

    def start_menu(self) -> bool:
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.fill((255, 255, 255))
            basicfont = pygame.font.Font('freesansbold.ttf', 100)
            text = basicfont.render('Tank Wars', True, (0, 0, 0), (255, 255, 255))
            self.screen.blit(text, (120, 100))
            self.message_to_screen("Shoot the other tank to survive!", (255, 0, 0), 25, 150, 260)
            self.message_to_screen("Press SPACE to shoot", (255, 0, 0), 25, 150, 290)
            self.message_to_screen("Press Up or Down to move turret!", (255, 0, 0), 25, 150, 320)
            self.message_to_screen("Press Left or Right to move tank!", (255, 0, 0), 25, 150, 350)
            res = self.button_type(200, (0, 255, 0), (0, 200, 0), "play")
            if res:
                return res
            self.button_font('GO!', 250, 495)
            self.button_type(500, (255, 0, 0), (200, 0, 0), "quit")
            self.button_font('Quit', 550, 495)
            pygame.display.update()
            self.clock.tick(5)

    def draw_game(self, tank: IPlayer, bot: IPlayer, barrier: Barrier, health: HealthBar) -> None:
        self.screen.fill((255, 255, 255)) 
        tank.draw()
        bot.draw() 
        tank.draw() 
        barrier.draw()   
        health.draw()        
        pygame.display.flip()              
        self.clock.tick(15)                

    def draw_tank(self, tank: IPlayer) -> None:
        turret = tank.possible_turrets[tank.turret_position]
        pygame.draw.circle(self.screen, tank.color, (tank.x, tank.y), tank.tank_height // 2)
        pygame.draw.rect(self.screen, tank.color, (tank.x - tank.tank_height, tank.y, tank.tank_width, tank.tank_height))
        pygame.draw.line(self.screen, tank.color, (tank.x, tank.y), turret, tank.turret_width)
        wheels = [(tank.x, tank.y + 23), (tank.x + 5, tank.y + 23), (tank.x - 5, tank.y + 23),
                  (tank.x + 10, tank.y + 23), (tank.x - 10, tank.y + 23), (tank.x + 15, tank.y + 23),
                  (tank.x - 15, tank.y + 23)]
        for wheel in wheels:
            pygame.draw.circle(self.screen, tank.color, wheel, tank.wheel_width)
    
    def draw_barrier(self, barrier: Barrier) -> None:
        screen_height = self.screen.get_height()
        screen_width = self.screen.get_width()
        self.screen.fill((0, 255, 0), rect=[0, screen_height - barrier.ground_height, screen_width, barrier.ground_height])
        pygame.draw.rect(self.screen, barrier.color, (barrier.xlocation, screen_height - barrier.random_height - barrier.ground_height, barrier.barrier_width, barrier.random_height))

    def draw_health(self, health: HealthBar) -> None:
        player_health_color = health.get_health_color(health.player_health)
        enemy_health_color = health.get_health_color(health.enemy_health)

        pygame.draw.rect(self.screen, player_health_color, (680, 25, health.player_health, 25))
        pygame.draw.rect(self.screen, enemy_health_color, (20, 25, health.enemy_health, 25))

        self.message_to_screen(f"{health.player_health}%", health.black, 15, 710, 32)
        self.message_to_screen(f"{health.enemy_health}%", health.black, 15, 50, 32)

    def draw_shell(self, position, flag = True) -> None:
        if flag:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(position[0]), int(position[1])), 5)
        else:
            pygame.display.update()
            pygame.time.Clock().tick(60)

    def draw_explosion(self, position):
        color_choices = [(255, 0, 0), (255, 69, 0), (0, 255, 0), (0, 200, 0), (255, 255, 0)]
        pygame.draw.circle(self.screen, random.choice(color_choices), (position[0], position[1]), random.randrange(1, 5))
        pygame.display.update()
        pygame.time.Clock().tick(100)

    def game_over(self) -> bool:
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'bright_green': (0, 200, 0),
            'bright_red': (200, 0, 0)
        }
        game_over = True

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.screen.fill(self.colors['white'])
            basicfont = pygame.font.Font('freesansbold.ttf', 100)
            text = basicfont.render('Game Over!', True, (0, 0, 0), (255, 255, 255))
            self.screen.blit(text, (120, 100))
            self.message_to_screen("", self.colors['white'], 25, 80, 360)
            res = self.button_type(200, self.colors['green'], self.colors['bright_green'], "play_again")
            if res:
                return res
            self.button_font('Play again', 250, 495)
            self.button_type(500, self.colors['red'], self.colors['bright_red'], "quit")
            self.button_font('Quit', 550, 495)
            pygame.display.update()
            self.clock.tick(5)