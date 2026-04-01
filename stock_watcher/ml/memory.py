"""
Experience Replay Memory dla RL agent
"""

import numpy as np
from collections import deque
from typing import Tuple


class ReplayMemory:
    """Pamięć do przechowywania doświadczeń agenta"""

    def __init__(self, capacity: int = 10000):
        """
        Inicjalizacja pamięci

        Args:
            capacity: Maksymalna pojemność pamięci
        """
        self.capacity = capacity
        self.memory = deque(maxlen=capacity)

    def push(
        self,
        state: np.ndarray,
        action: int,
        reward: float,
        next_state: np.ndarray,
        done: bool
    ):
        """Dodaje doświadczenie do pamięci"""
        self.memory.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int) -> Tuple:
        """Pobiera losowy batch z pamięci"""
        if len(self.memory) < batch_size:
            batch_size = len(self.memory)
        indices = np.random.choice(len(self.memory), batch_size, replace=False)
        states = np.array([self.memory[i][0] for i in indices])
        actions = np.array([self.memory[i][1] for i in indices])
        rewards = np.array([self.memory[i][2] for i in indices])
        next_states = np.array([self.memory[i][3] for i in indices])
        dones = np.array([self.memory[i][4] for i in indices])
        return states, actions, rewards, next_states, dones

    def __len__(self) -> int:
        """Zwraca rozmiar pamięci"""
        return len(self.memory)