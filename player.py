from abc import ABC, abstractmethod
import random
import pickle

class Player(ABC):
    PLAYER_NAME = ''

    @abstractmethod
    def make_move(self, stores: list[int]) -> int:
        pass
    
class HumanPlayer(Player):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.PLAYER_NAME = name

    def make_move(self, stores: list[int]) -> int:
        return int(input('Make a valid move: '))
    
class RandomPlayer(Player):
    PLAYER_NAME = 'Random agent'

    def make_move(self, stores: list[int]) -> int:
        return random.randint(1, 6)
    
class RLPlayer(Player):
    PLAYER_NAME = 'RL agent'
    LOAD_AGENT_PATH = './mancala-rl.pkl'

    def __init__(self, alpha, gamma, epsilon) -> None:
        super().__init__()
        try:
            with open(self.LOAD_AGENT_PATH, 'rb') as infile:
                self.statemap = pickle.load(infile)
        except FileNotFoundError:
            print('No pretrained agent exists. Creating new agent')
            self.statemap = {}
        
        # Parameters not saved in pkl file
        self.max_actions = 6
        self.hash_previous_state = 0
        self.previous_action = 0
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.reward = 0

    def make_move(self, stores: list[int]) -> int:
        if random.random() > self.epsilon:
            action = random.randint(0, self.max_actions - 1)
        else:
            hash_current_state = self._hash_state(stores)
            current_q_set = self.statemap.get(hash_current_state)
            if current_q_set is None:
                self.statemap[hash_current_state] = [random.random()  for _ in range(self.max_actions)]
                current_q_set = self.statemap[hash_current_state]
            action = current_q_set.index(max(current_q_set)) # Argmax of Q
            
        self.previous_action = action
        return action

    def update_q(self, stores: list[int], reward: int = 0) -> None:
        hash_current_state = self._hash_state(stores)
        current_q_set = self.statemap.get(hash_current_state)
        previous_q_set = self.statemap.get(self.hash_previous_state)
        if current_q_set is None:
            self.statemap[hash_current_state] = [random.random() for _ in range(self.max_actions)]
            current_q_set = self.statemap[hash_current_state]
        if previous_q_set is None:
            self.statemap[self.hash_previous_state] = [random.random() for _ in range(self.max_actions)]
            previous_q_set = self.statemap[self.hash_previous_state]

        q_s_a = self.statemap[self.hash_previous_state][self.previous_action]
        q_s_a = q_s_a + self.alpha * (reward + self.gamma * max(current_q_set) - q_s_a)
        
        self.statemap[self.hash_previous_state][self.previous_action] = q_s_a

        self.hash_previous_state = hash_current_state
    
    def _hash_state(self, stores: list[int]) -> int:
        return hash(''.join(map(str, stores)))
    
    def save_agent(self, save_path):
        with open(save_path, 'wb') as outfile:
            pickle.dump(self.statemap, outfile)