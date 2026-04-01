"""
CNN Agent z Reinforcement Learning
"""

import numpy as np
import pickle
from typing import Tuple, List
from .cnn_model import CNNModel
from .memory import ReplayMemory
from .environment import TradingEnvironment


class CNNAgent:
    """Agent do handlu akcjami z Deep Q-Learning"""

    def __init__(self,
        input_shape: Tuple = (300,),  # 60 dni * 5 wskaźników
        learning_rate: float = 0.001,
        epsilon: float = 1.0,
        epsilon_decay: float = 0.995,
        epsilon_min: float = 0.01,
        gamma: float = 0.95,
        memory_capacity: int = 10000
    ):
        """
        Inicjalizacja agenta

        Args:
            input_shape: Kształt stanu
            learning_rate: Learning rate
            epsilon: Exploration rate
            epsilon_decay: Decay exploration rate
            epsilon_min: Minimalna exploration rate
            gamma: Discount factor
            memory_capacity: Pojemność pamięci
        """
        self.input_shape = input_shape
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.gamma = gamma
        self.q_network = CNNModel(input_shape=(60, 5), learning_rate=learning_rate)
        self.target_network = CNNModel(input_shape=(60, 5), learning_rate=learning_rate)
        self.memory = ReplayMemory(memory_capacity)
        self.steps = 0
        self.episodes = 0

    def select_action(self, state: np.ndarray, training: bool = True) -> int:
        """Wybiera akcję używając epsilon-greedy strategy""" 
        if training and np.random.random() < self.epsilon:
            return np.random.choice([0, 1, 2])
        state_input = state.reshape(1, 60, 5)
        q_values = self.q_network.predict(state_input)[0]
        return np.argmax(q_values)

    def train_step(self, batch_size: int = 32):
        """Trenuje model na batch z pamięci"""
        if len(self.memory) < batch_size:
            return
        states, actions, rewards, next_states, dones = self.memory.sample(batch_size)
        target_q_values = self.q_network.predict(states.reshape(-1, 60, 5))
        next_q_values = self.target_network.predict(
            next_states.reshape(-1, 60, 5)
        )
        for i in range(batch_size):
            if dones[i]:
                target_q_values[i][actions[i]] = rewards[i]
            else:
                target_q_values[i][actions[i]] = (
                    rewards[i] + self.gamma * np.max(next_q_values[i])
                )
        self.q_network.model.fit(
            states.reshape(-1, 60, 5),
            target_q_values,
            epochs=1,
            verbose=0
        )
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def train_episode(
        self,
        environment: TradingEnvironment,
        batch_size: int = 32
    ) -> float:
        """Trenuje jeden epizod"""
        state = environment.reset()
        total_reward = 0
        while True:
            action = self.select_action(state, training=True)
            next_state, reward, done, info = environment.step(action)
            self.memory.push(state, action, reward, next_state, done)
            self.train_step(batch_size)
            total_reward += reward
            state = next_state
            self.steps += 1
            if done:
                break
        self.episodes += 1
        return total_reward

    def train(
        self,
        environment: TradingEnvironment,
        episodes: int = 100,
        batch_size: int = 32,
        update_target_freq: int = 10
    ) -> List[float]:
        """Trenuje agenta"""
        episode_rewards = []
        for episode in range(episodes):
            reward = self.train_episode(environment, batch_size)
            episode_rewards.append(reward)
            if (episode + 1) % update_target_freq == 0:
                self.target_network.model.set_weights(
                    self.q_network.model.get_weights()
                )
            if (episode + 1) % 10 == 0:
                avg_reward = np.mean(episode_rewards[-10:])
                print(f"Episode {episode + 1}/{episodes} | Avg Reward: {avg_reward:.4f} | "
                      f"Epsilon: {self.epsilon:.4f}")
        return episode_rewards

    def save(self, filepath_prefix: str):
        """Zapisuje agenta""" 
        self.q_network.save(f"{filepath_prefix}_q_network.h5")
        self.target_network.save(f"{filepath_prefix}_target_network.h5")
        with open(f"{filepath_prefix}_agent.pkl", 'wb') as f:
            pickle.dump({
                'epsilon': self.epsilon,
                'episodes': self.episodes,
                'steps': self.steps
            }, f)
        print(f"✓ Agent zapisany: {filepath_prefix}")

    def load(self, filepath_prefix: str):
        """Ładuje agenta"""
        self.q_network.load(f"{filepath_prefix}_q_network.h5")
        self.target_network.load(f"{filepath_prefix}_target_network.h5")
        with open(f"{filepath_prefix}_agent.pkl", 'rb') as f:
            agent_data = pickle.load(f)
            self.epsilon = agent_data['epsilon']
            self.episodes = agent_data['episodes']
            self.steps = agent_data['steps']
        print(f"✓ Agent załadowany: {filepath_prefix}")