"""
Testy dla klasy StockAnalyzer
"""

import unittest
import pandas as pd
from stock_watcher import StockAnalyzer


class TestStockAnalyzer(unittest.TestCase):
    """Testy dla StockAnalyzer"""
    
    def setUp(self):
        """Inicjalizacja przed każdym testem"""
        self.analyzer = StockAnalyzer()
    
    def test_get_historical_data(self):
        """Test pobierania danych historycznych"""
        data = self.analyzer.get_historical_data('AAPL', period='1mo')
        
        self.assertIsInstance(data, pd.DataFrame)
        self.assertGreater(len(data), 0)
        self.assertIn('Close', data.columns)
    
    def test_calculate_indicators(self):
        """Test obliczania wskaźników"""
        data = self.analyzer.get_historical_data('AAPL', period='3mo')
        indicators_data = self.analyzer.calculate_indicators(data)
        
        self.assertIn('SMA_20', indicators_data.columns)
        self.assertIn('RSI', indicators_data.columns)
        self.assertIn('MACD', indicators_data.columns)


if __name__ == '__main__':
    unittest.main()
