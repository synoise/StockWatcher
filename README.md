# StockWatcher 📈

System do analizowania giełdy GPW (Warszawska Giełda Papierów Wartościowych) i S&P 500.

## Funkcjonalności

✅ Śledzenie cen w czasie rzeczywistym
✅ Analiza techniczna (wskaźniki, wykresy)
✅ Analiza danych historycznych
✅ Wsparcie dla GPW i S&P 500

## Wymagania

- Python 3.8+
- pip

## Instalacja

```bash
# Klonuj repozytorium
git clone https://github.com/synoise/StockWatcher.git
cd StockWatcher

# Stwórz wirtualne środowisko
python -m venv venv

# Aktywuj wirtualne środowisko
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt
```

## Użycie

```python
from stock_watcher import StockAnalyzer

# Inicjalizuj analizator
analyzer = StockAnalyzer()

# Pobierz dane dla akcji
data = analyzer.get_historical_data('AAPL', period='1y')

# Oblicz wskaźniki techniczne
indicators = analyzer.calculate_indicators(data)

# Generuj wykres
analyzer.plot_price(data)
```

## Struktura projektu

```
StockWatcher/
├── stock_watcher/
│   ├── __init__.py
│   ├── analyzer.py          # Główna klasa analizatora
│   ├── data_fetcher.py      # Pobieranie danych z yfinance
│   ├── indicators.py        # Wskaźniki techniczne
│   ├── plotter.py           # Wykresy i wizualizacja
│   └── utils.py             # Funkcje pomocnicze
├── examples/
│   ├── basic_analysis.py
│   └── real_time_tracking.py
├── tests/
│   ├── test_analyzer.py
│   └── test_indicators.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Roadmap

- [ ] Pobieranie danych z yfinance
- [ ] Wskaźniki techniczne (SMA, RSI, MACD, Bollinger Bands)
- [ ] Wykresy interaktywne (Plotly)
- [ ] Śledzenie portfela
- [ ] Alerty cenowe
- [ ] Dashboard webowy

## Licencja

MIT
