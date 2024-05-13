from player import Player

class Mancala:
    NUM_OF_STORES = 14
    INITIAL_BALLS = 4

    STORE_OPPOSITES = {0:12, 12:0, 1:11, 11:1, 2:10,
                        10:2, 3:9, 9:3, 4:8, 8:4, 5:7, 7:5}
    def __init__(self, player_0: Player, player_1: Player):
        self.stores = [self.INITIAL_BALLS for _ in range(self.NUM_OF_STORES)]
        self.stores[6] = 0
        self.stores[13] = 0

        self.current_player = 0
        self.player_0: Player = player_0
        self.player_1: Player = player_1

    def play_game(self) -> None:
        self._draw_board()
        while True:
            if self.current_player == 0:
                player = self.player_0
            else:
                player = self.player_1

            is_move_valid = False
            while not is_move_valid:
                print(f"Player {self.current_player}'s move")
                store_to_move = player.make_move(self.stores)
                is_move_valid = self._is_move_valid(store_to_move)
            
            self._update_stores(store_to_move)
            self._draw_board()

            if self._is_game_over():
                print(f"The winner is {self._get_winner()}")
                return

            self.current_player = 1 - self.current_player

    def _is_move_valid(self, store_to_move: int) -> bool:
        if self.current_player == 0:
            if store_to_move < 0 or store_to_move > 5:
                return False
        elif store_to_move < 7 or store_to_move >= self.NUM_OF_STORES:
            return False
        if self.stores[store_to_move] <= 0:
            return False
        return True
    
    #   [5] [4] [3]  [2]  [1]  [0]
    # [6]                         [13]
    #   [7] [8] [9] [10] [11] [12]
    #
    #

    def _update_stores(self, store_to_move: int) -> None:
        balls_to_distribute = self.stores[store_to_move]
        self.stores[store_to_move] = 0

        current_store = store_to_move
        while balls_to_distribute > 0:
            current_store += 1
            if current_store >= self.NUM_OF_STORES:
                current_store = 0

            # if current store is opponents big store, skip
            if current_store == 6 and self.current_player == 1:
                continue
            if current_store == 13 and self.current_player == 0:
                continue

            self.stores[current_store] = self.stores[current_store] + 1

            balls_to_distribute -= 1

        # prevent change of player - extra round
        if (self.current_player == 0 and current_store == 6
            or self.current_player == 1 and current_store == 13):
            self.current_player = 1 - self.current_player
        
        # if last ball landed in empty store, capture all opposite balls
        if self.stores[current_store] == 1 and ((self.current_player == 0 and 0 <= current_store <= 5)
                                                or (self.current_player == 1 and 7 <= current_store <= 12)):
            opposite_store = self.STORE_OPPOSITES[current_store]
            big_store = 6 if self.current_player == 0 else 13
            self.stores[big_store] = self.stores[big_store] + self.stores[opposite_store]
            self.stores[opposite_store] = 0

    def _is_game_over(self) -> bool:
        return (all([store == 0 for store in self.stores[0:6]])
                or all([store == 0 for store in self.stores[7:-1]]))
    
    def _get_winner(self) -> Player:
        player_0_count = sum([store for store in self.stores[0:7]])
        player_1_count = sum([store for store in self.stores[7:]])

        if player_0_count > player_1_count: return self.player_0

        return self.player_1
    
    def _draw_board(self):
        player_0_board = "".join([f"[{store}]" for store in self.stores[5::-1]])
        player_1_board = "".join([f"[{store}]" for store in self.stores[7:13]])

        print("===============================================")
        print(f"    {player_0_board}    ")
        print(f"[{self.stores[6]}]                        [{self.stores[13]}]")
        print(f"    {player_1_board}    ")
        print("===============================================")