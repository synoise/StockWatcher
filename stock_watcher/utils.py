"""
Funkcje pomocnicze
"""

import pandas as pd
from typing import Optional


def format_currency(value: Optional[float], currency: str = "PLN") -> str:
    """Formatuje wartość na format walutowy"""
    if value is None:
        return "N/A"
    return f"{value:,.2f} {currency}"


def calculate_percentage_change(start: float, end: float) -> float:
    """Oblicza procentową zmianę"""
    if start == 0:
        return 0
    return ((end - start) / start) * 100


def get_date_range(data: pd.DataFrame) -> tuple:
    """Pobiera zakres dat z DataFrame"""
    return data.index.min(), data.index.max()


def print_summary(data: pd.DataFrame, ticker: str = ""):
    """Wypisuje podsumowanie danych"""
    print(f"\n{'='*50}")
    print(f"Podsumowanie: {ticker}")
    print(f"{'='*50}")
    print(f"Okres: {data.index.min().date()} do {data.index.max().date()}")
    print(f"Liczba obserwacji: {len(data)}")
    print(f"Cena otwarcia: {format_currency(data['Close'].iloc[0])}")
    print(f"Cena zamknięcia: {format_currency(data['Close'].iloc[-1])}")
    print(f"Cena minimalna: {format_currency(data['Low'].min())}")
    print(f"Cena maksymalna: {format_currency(data['High'].max())}")
    print(f"Średnia cena: {format_currency(data['Close'].mean())}")
    
    pct_change = calculate_percentage_change(data['Close'].iloc[0], data['Close'].iloc[-1])
    print(f"Zmiana: {pct_change:+.2f}%")
    print(f"{'='*50}\n")


if __name__ == '__main__':
    pass
