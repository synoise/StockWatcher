"""
Przykład: Śledzenie cen w czasie rzeczywistym
"""

from stock_watcher import StockAnalyzer
from stock_watcher.utils import format_currency, calculate_percentage_change
import time


def track_price(ticker: str, check_interval: int = 60):
    """Śledzi cenę akcji w czasie rzeczywistym"""
    
    analyzer = StockAnalyzer()
    
    print(f"\n📊 Rozpoczęto śledzenie: {ticker}")
    print(f"Interwał sprawdzania: {check_interval} sekund")
    print("=" * 50)
    
    # Pobierz informacje o tickerze
    info = analyzer.get_ticker_info(ticker)
    print(f"Nazwa: {info.get('name', 'N/A')}")
    print(f"Sektor: {info.get('sector', 'N/A')}")
    print("=" * 50)
    
    previous_price = None
    
    try:
        while True:
            current_price = analyzer.fetcher.get_latest_price(ticker)
            
            if current_price:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                
                if previous_price:
                    change = current_price - previous_price
                    pct_change = calculate_percentage_change(previous_price, current_price)
                    direction = "📈" if change >= 0 else "📉"
                    
                    print(
                        f"{timestamp} | "
                        f"Cena: {format_currency(current_price)} | "
                        f"Zmiana: {change:+.2f} ({pct_change:+.2f}%) {direction}"
                    )
                else:
                    print(f"{timestamp} | Cena: {format_currency(current_price)}")
                
                previous_price = current_price
            
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print("\n\n⏹ Zatrzymano śledzenie")


if __name__ == "__main__":
    # Śledzenie Apple
    track_price('AAPL', check_interval=60)
