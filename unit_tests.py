import unittest, pygame
from unittest.mock import Mock, patch
from game import Game
from tanks import PlayerTank, EnemyTank
from view import GameView
from barrier import Barrier
from health import HealthBar
from fireshell import Shell

class TestGame(unittest.TestCase):
    def setUp(self):
        self.screen_size = (800, 600)
        self.player = Mock()
        self.player.x = 300 
        self.player.y = 400 
        self.player.turret_position = 0 

        self.enemy = Mock()
        self.enemy.x = 100 
        self.enemy.y = 400 

        self.view = Mock()
        self.direction = 'LEFT'

        self.game = Game( self.view, self.player, self.enemy, self.screen_size)
        self.game.player = self.player
        self.game.enemy = self.enemy
        self.game.gun_power = 10 
        self.game.barrier = Barrier(self.screen_size, self.view)
        self.game.health = HealthBar(self.view)

    def test_game_initialization(self):
        """Проверка правильной инициализации объекта Game."""
        self.assertEqual(self.game.size, self.screen_size)
        self.assertEqual(self.game.view, self.view)  
        self.assertEqual(self.game.player, self.player) 
        self.assertEqual(self.game.enemy, self.enemy)
        self.assertTrue(isinstance(self.game.barrier, Barrier))  
        self.assertTrue(isinstance(self.game.health, HealthBar))  
        self.assertTrue(self.game.turn)
        self.assertEqual(self.game.gun_power, 10)  

class TestPlayerTank(unittest.TestCase):
    def setUp(self):
        self.view = Mock()
        self.control = Mock()
        self.player_tank = PlayerTank(100, 100, self.control, self.view)

    def test_move(self):
        """Проверка метода move."""
        mas = (5, 1)
        self.player_tank.move(mas)
        self.assertEqual(self.player_tank.x, 105) 
        self.assertEqual(self.player_tank.turret_position, 8) 

    def test_reset_position(self):
        """Проверка метода reset_position."""
        self.player_tank.reset_position(800, 600)
        self.assertEqual(self.player_tank.x, 800)
        self.assertEqual(self.player_tank.y, 600)

    def test_draw(self):
        """Проверка метода draw на вызов метода отрисовки."""
        self.player_tank.draw()
        self.view.draw_tank.assert_called_once_with(self.player_tank)

class TestEnemyTank(unittest.TestCase):
    def setUp(self):
        self.view = Mock()
        self.enemy_tank = EnemyTank(100, 500, self.view)

    def test_move(self):
        """Проверка метода move."""
        mas = (self.enemy_tank.x, self.enemy_tank.turret_position)
        self.enemy_tank.move()
        self.assertNotEqual(self.enemy_tank.x, mas[0]) 
        self.assertNotEqual(self.enemy_tank.turret_position, mas[1]) 

    def test_reset_position(self):
        """Проверка метода reset_position."""
        self.enemy_tank.reset_position(200, 300)
        self.assertEqual(self.enemy_tank.x, 200)
        self.assertEqual(self.enemy_tank.y, 300)

    def test_draw(self):
        """Проверка метода draw на вызов метода отрисовки в представлении."""
        self.enemy_tank.draw()
        self.view.draw_tank.assert_called_once_with(self.enemy_tank)
    
class TestShell(unittest.TestCase):
    @patch('view.IView')
    def test_shell_fire(self, MockView):
        """Проверка метода fire на корректное поведение и вызовы отрисовки."""
        view = MockView()
        barrier = Mock(Barrier)
        barrier.ground_height = 35
        barrier.xlocation = 100
        barrier.barrier_width = 40
        barrier.random_height = 50

        shell = Shell((800, 600), (50, 50), 50, 50, 7, 50, barrier, 750, 500, view, "RIGHT")
        shell.fire()
        view.draw_shell.assert_called()  

class TestGameView(unittest.TestCase):
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    def test_initialization(self, mock_set_caption, mock_set_mode):
        """Проверка инициализации окна игры."""
        view = GameView()
        view.initialization((800, 600))
        mock_set_mode.assert_called_once_with((800, 600))
        mock_set_caption.assert_called_once_with('Tanks')

    @patch('pygame.display.flip')  
    def test_draw_game(self, mock_flip):
        """Проверка метода draw_game на вызовы отрисовки всех компонентов."""
        view = GameView()
        view.initialization((800, 600))  
        view.screen = Mock()  
        tank = Mock()
        bot = Mock()
        barrier = Mock()
        health = Mock()

        view.draw_game(tank, bot, barrier, health)

        tank.draw.assert_called()
        bot.draw.assert_called()
        barrier.draw.assert_called()
        health.draw.assert_called()
  

if __name__ == "__main__":
    unittest.main()

