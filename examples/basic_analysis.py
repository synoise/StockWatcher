"""
Przykład: Podstawowa analiza akcji
"""

from stock_watcher import StockAnalyzer
from stock_watcher.utils import print_summary

def main():
    """Główna funkcja"""
    
    # Inicjalizuj analizator
    analyzer = StockAnalyzer()
    
    # Wybór tickerów
    tickers = ['AAPL', 'MCDM.WA']  # Apple i mBank (GPW)
    
    for ticker in tickers:
        try:
            print(f"\n🔍 Analiza: {ticker}")
            
            # Pobierz dane historyczne
            data = analyzer.get_historical_data(ticker, period='6mo')
            
            # Wypisz podsumowanie
            print_summary(data, ticker)
            
            # Oblicz wskaźniki
            data_with_indicators = analyzer.calculate_indicators(data)
            
            # Wypisz ostatnie dane
            print(f"\nOstatnie dane dla {ticker}:")
            print(data_with_indicators[['Close', 'SMA_20', 'SMA_50', 'RSI']].tail())
            
            # Rysuj wykresy
            analyzer.plot_price(data, ticker, with_sma=True)
            analyzer.plot_indicators(data_with_indicators, ticker)
            
        except Exception as e:
            print(f"❌ Błąd dla {ticker}: {str(e)}")


if __name__ == "__main__":
    main()
