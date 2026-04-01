"""
Testy dla wskaźników technicznych
"""

import unittest
import pandas as pd
import numpy as np
from stock_watcher.indicators import TechnicalIndicators


class TestTechnicalIndicators(unittest.TestCase):
    """Testy dla TechnicalIndicators"""
    
    def setUp(self):
        """Inicjalizacja przed każdym testem"""
        self.indicators = TechnicalIndicators()
        # Stwórz testowe dane
        self.prices = pd.Series([100, 102, 101, 103, 105, 104, 106, 108, 107, 109] * 5)
    
    def test_sma(self):
        """Test SMA"""
        sma = self.indicators.calculate_sma(self.prices, 5)
        self.assertEqual(len(sma), len(self.prices))
        self.assertTrue(pd.isna(sma.iloc[0]))
    
    def test_rsi(self):
        """Test RSI"""
        rsi = self.indicators.calculate_rsi(self.prices, 14)
        self.assertEqual(len(rsi), len(self.prices))
        # RSI powinien być między 0 a 100
        self.assertTrue((rsi.dropna() >= 0).all() and (rsi.dropna() <= 100).all())


if __name__ == '__main__':
    unittest.main()
