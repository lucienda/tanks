import pygame
from abc import ABC, abstractmethod
from tanks import PlayerTank, EnemyTank, IPlayer
from barrier import Barrier
from health import HealthBar
from fireshell import Shell
from view import IView


class Game:
    def __init__(self, view: IView, player: IPlayer, bot: IPlayer, screen_size):
        self.size = screen_size
        self.view = view
        self.player_tank = player
        self.enemy_tank = bot
        self.barrier = Barrier(self.size, self.view) 
        self.health = HealthBar(self.view)
        self.turn = True
        self.gun_power = 50

    def fire_shell(self) -> None:
        shell = Shell(
            self.size, 
            (self.player_tank.x, self.player_tank.y), 
            self.player_tank.x, 
            self.player_tank.y,
            self.player_tank.turret_position, 
            self.gun_power,
            self.barrier, 
            self.enemy_tank.x, 
            self.enemy_tank.y, 
            self.view, 
            direction="LEFT"
        )
        damage = shell.fire()
        self.health.enemy_health -= damage
        return shell

    def enemy_fire_shell(self) -> None:
        enemy_shell = Shell(self.size, (self.enemy_tank.x, self.enemy_tank.y), self.enemy_tank.x, self.enemy_tank.y,
                            self.enemy_tank.turret_position, self.gun_power, self.barrier, self.player_tank.x, self.player_tank.y, self.view,  direction="RIGHT")
        damage = enemy_shell.fire()
        self.health.player_health -= damage

    def reset_game(self) -> None:
        self.health = HealthBar(self.view)
        self.barrier = Barrier(self.size, self.view) 
        self.turn = True
        self.player_tank.reset_position(self.size[0] * 0.9, self.size[1] * 0.9)
        self.enemy_tank.reset_position(self.size[0] * 0.1, self.size[1] * 0.9)

    def game_loop(self):
        self.view.initialization(self.size)
        running = self.view.start_menu()
        
        while running:
            if self.turn:
                mas = [0, 0, False]
                self.player_tank.move(mas)
                if mas[2]: 
                    self.fire_shell()  
                    self.turn = False
            else:
                self.enemy_tank.move()
                self.enemy_fire_shell()  
                self.turn = True

            self.view.draw_game(self.player_tank, self.enemy_tank, self.barrier, self.health)

            if self.health.enemy_health <= 0 or self.health.player_health <= 0:
                res = self.view.game_over()
                if res:
                    self.reset_game()
                else:
                    self.running = False
