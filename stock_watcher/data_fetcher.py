"""
Moduł do pobierania danych giełdowych z yfinance
"""

import yfinance as yf
import pandas as pd
from typing import Optional, List


class DataFetcher:
    """Klasa do pobierania danych giełdowych"""

    def __init__(self):
        """Inicjalizacja DataFetchera"""
        self.data_cache = {}

    def get_historical_data(
        self,
        ticker: str,
        period: str = "1y",
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Pobiera dane historyczne dla danego tickera

        Args:
            ticker: Symbol akcji (np. 'AAPL', 'MSFT', 'MCDM.WA' dla GPW)
            period: Okres czasu ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y')
            interval: Interwał czasowy ('1m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')

        Returns:
            pd.DataFrame: DataFrame z danymi OHLCV (Open, High, Low, Close, Volume)
        """
        try:
            print(f"Pobieranie danych dla {ticker}...")
            data = yf.download(
                ticker,
                period=period,
                interval=interval,
                progress=False
            )
            
            if data.empty:
                raise ValueError(f"Brak danych dla tickera: {ticker}")
            
            # Cachuj dane
            cache_key = f"{ticker}_{period}_{interval}"
            self.data_cache[cache_key] = data
            
            print(f"✓ Pobrano {len(data)} wierszy danych")
            return data
            
        except Exception as e:
            print(f"✗ Błąd przy pobieraniu danych: {str(e)}")
            raise

    def get_multiple_tickers(
        self,
        tickers: List[str],
        period: str = "1y",
        interval: str = "1d"
    ) -> dict:
        """
        Pobiera dane dla wielu tickerów

        Args:
            tickers: Lista symbolów akcji
            period: Okres czasu
            interval: Interwał czasowy

        Returns:
            dict: Słownik z danymi dla każdego tickera
        """
        data = {}
        for ticker in tickers:
            try:
                data[ticker] = self.get_historical_data(ticker, period, interval)
            except Exception as e:
                print(f"⚠ Nie udało się pobrać danych dla {ticker}: {str(e)}")
                continue
        
        return data

    def get_latest_price(self, ticker: str) -> Optional[float]:
        """
        Pobiera najnowszą cenę dla danego tickera

        Args:
            ticker: Symbol akcji

        Returns:
            float: Ostatnia cena zamknięcia
        """
        try:
            ticker_obj = yf.Ticker(ticker)
            latest_price = ticker_obj.info.get('currentPrice') or ticker_obj.info.get('regularMarketPrice')
            return latest_price
        except Exception as e:
            print(f"✗ Błąd przy pobieraniu ceny: {str(e)}")
            return None

    def get_ticker_info(self, ticker: str) -> dict:
        """
        Pobiera informacje o tickerze

        Args:
            ticker: Symbol akcji

        Returns:
            dict: Informacje o tickerze
        """
        try:
            ticker_obj = yf.Ticker(ticker)
            return {
                'name': ticker_obj.info.get('longName', 'N/A'),
                'sector': ticker_obj.info.get('sector', 'N/A'),
                'industry': ticker_obj.info.get('industry', 'N/A'),
                'market_cap': ticker_obj.info.get('marketCap', 'N/A'),
                'pe_ratio': ticker_obj.info.get('trailingPE', 'N/A'),
                'dividend_yield': ticker_obj.info.get('dividendYield', 'N/A'),
            }
        except Exception as e:
            print(f"✗ Błąd przy pobieraniu informacji: {str(e)}")
            return {}
