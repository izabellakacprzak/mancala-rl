from mancala import Mancala
from player import HumanPlayer, RandomPlayer, RLPlayer

player_0 = HumanPlayer(name='Player 0')
player_1 = RLPlayer(alpha=0.5, gamma=0.5, epsilon=0.9)

mancala = Mancala(player_0=player_0, player_1=player_1)
mancala.play_game()