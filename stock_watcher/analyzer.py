"""
Główna klasa analizatora giełdowego
"""

import pandas as pd
from .data_fetcher import DataFetcher
from .indicators import TechnicalIndicators
from .plotter import Plotter


class StockAnalyzer:
    """Główna klasa do analizy akcji"""

    def __init__(self):
        """Inicjalizacja analizatora"""
        self.fetcher = DataFetcher()
        self.indicators = TechnicalIndicators()
        self.plotter = Plotter()

    def get_historical_data(
        self,
        ticker: str,
        period: str = "1y",
        interval: str = "1d"
    ) -> pd.DataFrame:
        """Pobiera dane historyczne"""
        return self.fetcher.get_historical_data(ticker, period, interval)

    def calculate_indicators(
        self,
        data: pd.DataFrame,
        sma_periods: list = [20, 50, 200],
        rsi_period: int = 14,
        macd_periods: tuple = (12, 26, 9)
    ) -> pd.DataFrame:
        """Oblicza wskaźniki techniczne"""
        result = data.copy()

        # SMA (Simple Moving Average)
        for period in sma_periods:
            result[f'SMA_{period}'] = self.indicators.calculate_sma(data['Close'], period)

        # RSI (Relative Strength Index)
        result['RSI'] = self.indicators.calculate_rsi(data['Close'], rsi_period)

        # MACD
        macd, signal, histogram = self.indicators.calculate_macd(
            data['Close'],
            macd_periods[0],
            macd_periods[1],
            macd_periods[2]
        )
        result['MACD'] = macd
        result['MACD_Signal'] = signal
        result['MACD_Histogram'] = histogram

        # Bollinger Bands
        bb_high, bb_mid, bb_low = self.indicators.calculate_bollinger_bands(
            data['Close'],
            period=20,
            std_dev=2
        )
        result['BB_High'] = bb_high
        result['BB_Mid'] = bb_mid
        result['BB_Low'] = bb_low

        return result

    def get_ticker_info(self, ticker: str) -> dict:
        """Pobiera informacje o tickerze"""
        return self.fetcher.get_ticker_info(ticker)

    def plot_price(self, data: pd.DataFrame, ticker: str = "", with_sma: bool = True):
        """Rysuje wykres ceny"""
        self.plotter.plot_price(data, ticker, with_sma)

    def plot_indicators(self, data: pd.DataFrame, ticker: str = ""):
        """Rysuje wykresy wskaźników"""
        self.plotter.plot_indicators(data, ticker)
