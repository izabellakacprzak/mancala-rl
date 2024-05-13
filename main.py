from mancala import Mancala
from player import HumanPlayer

player_0 = HumanPlayer()
player_1 = HumanPlayer()

mancala = Mancala(player_0=player_0, player_1=player_1)
mancala.play_game()