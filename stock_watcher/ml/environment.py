"""
Środowisko handlowe dla RL agent
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict


class TradingEnvironment:
    """Środowisko do treningu agenta handlowego"""

    def __init__(self,
        data: pd.DataFrame,
        initial_balance: float = 10000,
        transaction_cost: float = 0.001,
        lookback_period: int = 60
    ):
        """
        Inicjalizacja środowiska

        Args:
            data: DataFrame z danymi OHLCV
            initial_balance: Początkowy kapitał
            transaction_cost: Koszt transakcji (w procentach)
            lookback_period: Liczba poprzednich obserwacji
        """
        self.data = data.reset_index(drop=True)
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.transaction_cost = transaction_cost
        self.lookback_period = lookback_period
        self.current_step = lookback_period
        self.max_step = len(data) - 1
        self.position = 0  # 0=No position, 1=Long
        self.position_price = 0
        self.portfolio_value = initial_balance
        self.history = {
            'balance': [initial_balance],
            'position': [0],
            'portfolio_value': [initial_balance],
            'price': []
        }

    def reset(self) -> np.ndarray:
        """Resetuje środowisko""" 
        self.balance = self.initial_balance
        self.current_step = self.lookback_period
        self.position = 0
        self.position_price = 0
        self.portfolio_value = self.initial_balance
        self.history = {
            'balance': [self.initial_balance],
            'position': [0],
            'portfolio_value': [self.initial_balance],
            'price': []
        }
        return self._get_state()

    def _get_state(self) -> np.ndarray:
        """Zwraca obecny stan"""
        start_idx = max(0, self.current_step - self.lookback_period)
        end_idx = self.current_step
        state_data = self.data.iloc[start_idx:end_idx][
            ['Open', 'High', 'Low', 'Close', 'Volume']
        ].values
        state_data = (state_data - state_data.mean(axis=0)) / (state_data.std(axis=0) + 1e-8)
        return state_data.flatten()

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict]:
        """Wykonuje krok w środowisku"""
        current_price = self.data['Close'].iloc[self.current_step]
        next_price = self.data['Close'].iloc[self.current_step + 1] if self.current_step < self.max_step - 1 else current_price
        reward = 0
        if action == 1:  # Buy
            if self.position == 0:
                self.position = 1
                self.position_price = current_price
                cost = current_price * (1 + self.transaction_cost)
                self.balance -= cost
        elif action == 2:  # Sell
            if self.position == 1:
                self.position = 0
                revenue = current_price * (1 - self.transaction_cost)
                profit = revenue - self.position_price
                reward = profit / self.position_price
                self.balance += revenue
        if self.position == 1:
            price_change = (next_price - current_price) / current_price
            reward += price_change
        if self.position == 1:
            self.portfolio_value = self.balance + (next_price * 1)
        else:
            self.portfolio_value = self.balance
        self.history['balance'].append(self.balance)
        self.history['position'].append(self.position)
        self.history['portfolio_value'].append(self.portfolio_value)
        self.history['price'].append(current_price)
        self.current_step += 1
        done = self.current_step >= self.max_step - 1
        info = {
            'current_price': current_price,
            'portfolio_value': self.portfolio_value,
            'balance': self.balance
        }
        return self._get_state(), reward, done, info

    def render(self):
        """Wypisuje informacje o stanie""" 
        current_price = self.data['Close'].iloc[self.current_step]
        print(f"Step: {self.current_step} | Price: ${current_price:.2f} | "
              f"Balance: ${self.balance:.2f} | Portfolio: ${self.portfolio_value:.2f}")