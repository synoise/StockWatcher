"""
Preprocessing danych dla CNN
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple, List


class DataPreprocessor:
    """Klasa do preprocessing danych dla CNN"""

    def __init__(self, lookback_period: int = 60):
        """
        Inicjalizacja preprocessora

        Args:
            lookback_period: Liczba poprzednich dni do użycia jako input
        """
        self.lookback_period = lookback_period
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def normalize_data(self, data: np.ndarray) -> np.ndarray:
        """Normalizuje dane do zakresu [0, 1]"""
        return self.scaler.fit_transform(data.reshape(-1, 1)).flatten()

    def create_sequences(
        self,
        data: pd.DataFrame,
        target_column: str = 'Close'
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Tworzy sekwencje do treningu CNN

        Args:
            data: DataFrame z danymi OHLCV
            target_column: Kolumna docelowa

        Returns:
            Tuple: (X - features, y - targets)
        """
        normalized_data = np.zeros((len(data), len(data.columns)))
        
        for i, col in enumerate(data.columns):
            normalized_data[:, i] = self.normalize_data(data[col].values)

        X, y = [], []

        for i in range(len(normalized_data) - self.lookback_period):
            X.append(normalized_data[i:i + self.lookback_period])
            current_price = data[target_column].iloc[i + self.lookback_period]
            next_price = data[target_column].iloc[i + self.lookback_period + 1]
            y.append(1 if next_price > current_price else 0)

        return np.array(X), np.array(y)

    def create_image_sequences(
        self,
        data: pd.DataFrame,
        image_height: int = 28,
        image_width: int = 28
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Tworzy sekwencje jako obrazy dla CNN

        Args:
            data: DataFrame z danymi
            image_height: Wysokość obrazu
            image_width: Szerokość obrazu

        Returns:
            Tuple: (X - obrazy, y - labels)
        """
        X, y = self.create_sequences(data)
        X_images = []
        
        for sequence in X:
            resized = np.zeros((image_height, image_width, sequence.shape[1]))
            for channel in range(sequence.shape[1]):
                from scipy.ndimage import zoom
                scale_factors = (image_height / sequence.shape[0], 1)
                resized[:, :, channel] = zoom(
                    sequence[:, channel].reshape(-1, 1),
                    (image_height / sequence.shape[0], image_width / 1),
                    order=1
                )[:image_height, :image_width]
            X_images.append(resized)
        return np.array(X_images), y

    def prepare_train_test_split(
        self,
        data: pd.DataFrame,
        test_size: float = 0.2
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Dzieli dane na train i test"""
        X, y = self.create_sequences(data)
        split_idx = int(len(X) * (1 - test_size))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        return X_train, X_test, y_train, y_test