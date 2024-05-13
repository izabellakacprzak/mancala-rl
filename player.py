from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def make_move(self, stores: list) -> int:
        pass
    
class HumanPlayer(Player):
    def make_move(self, stores: list) -> int:
        return int(input("Make a valid move:"))