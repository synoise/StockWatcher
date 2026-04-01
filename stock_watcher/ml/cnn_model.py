"""
Model CNN dla predykcji cen giełdowych
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Sequential
import numpy as np
from typing import Tuple


class CNNModel:
    """Model CNN do predykcji kierunku ceny"""

    def __init__(self,
        input_shape: Tuple = (60, 5),
        learning_rate: float = 0.001,
        dropout_rate: float = 0.2
    ):
        """
        Inicjalizacja modelu CNN

        Args:
            input_shape: Kształt danych wejściowych
            learning_rate: Learning rate dla optimizera
            dropout_rate: Dropout rate
        """
        self.input_shape = input_shape
        self.learning_rate = learning_rate
        self.dropout_rate = dropout_rate
        self.model = self._build_model()

    def _build_model(self) -> Sequential:
        """Buduje architekturę modelu CNN"""
        model = Sequential([
            layers.Input(shape=self.input_shape),
            layers.Reshape((*self.input_shape, 1)),
            layers.Conv1D(32, kernel_size=3, activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(pool_size=2),
            layers.Dropout(self.dropout_rate),
            layers.Conv1D(64, kernel_size=3, activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(pool_size=2),
            layers.Dropout(self.dropout_rate),
            layers.Conv1D(128, kernel_size=3, activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(pool_size=2),
            layers.Dropout(self.dropout_rate),
            layers.Flatten(),
            layers.Dense(256, activation='relu'),
            layers.Dropout(self.dropout_rate),
            layers.Dense(128, activation='relu'),
            layers.Dropout(self.dropout_rate),
            layers.Dense(64, activation='relu'),
            layers.Dropout(self.dropout_rate),
            layers.Dense(2, activation='softmax')  # Up/Down classification
        ])
        optimizer = keras.optimizers.Adam(learning_rate=self.learning_rate)
        model.compile(
            optimizer=optimizer,
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    def summary(self):
        """Wypisuje summary modelu"""
        return self.model.summary()

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray = None,
        y_val: np.ndarray = None,
        epochs: int = 50,
        batch_size: int = 32,
        verbose: int = 1
    ) -> dict:
        """Trenuje model"""
        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
        history = self.model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            verbose=verbose,
            callbacks=[
                keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=5,
                    restore_best_weights=True
                )
            ]
        )
        return history.history

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Prognozuje dla nowych danych""" 
        return self.model.predict(X, verbose=0)

    def predict_signal(self, X: np.ndarray) -> np.ndarray:
        """Prognozuje sygnał (0=Down, 1=Up)"""
        predictions = self.predict(X)
        return np.argmax(predictions, axis=1)

    def save(self, filepath: str):
        """Zapisuje model"""
        self.model.save(filepath)
        print(f"✓ Model zapisany: {filepath}")

    def load(self, filepath: str):
        """Ładuje model"""
        self.model = keras.models.load_model(filepath)
        print(f"✓ Model załadowany: {filepath}")