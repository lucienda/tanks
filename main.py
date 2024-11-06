from game import Game
from tanks import PlayerTank, EnemyTank
from view import GameView
from control import PlayerControl

def main():
    screen_size = (800, 600)

    control = PlayerControl()
    view = GameView()

    player = PlayerTank(screen_size[0] * 0.9, screen_size[1] * 0.9, control, view)
    bot = EnemyTank(screen_size[0] * 0.1, screen_size[1] * 0.9, view)
    
    game = Game(view, player, bot, screen_size)
    game.game_loop()

if __name__ == "__main__":
    main()
