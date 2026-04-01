"""
Moduł do wizualizacji danych
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Plotter:
    """Klasa do tworzenia wykresów"""

    def plot_price(
        self,
        data: pd.DataFrame,
        ticker: str = "",
        with_sma: bool = True,
        figsize: tuple = (14, 6)
    ):
        """Rysuje wykres ceny"""
        plt.figure(figsize=figsize)

        plt.plot(data.index, data['Close'], label='Close Price', linewidth=2)

        if with_sma:
            if 'SMA_20' in data.columns:
                plt.plot(data.index, data['SMA_20'], label='SMA 20', alpha=0.7)
            if 'SMA_50' in data.columns:
                plt.plot(data.index, data['SMA_50'], label='SMA 50', alpha=0.7)
            if 'SMA_200' in data.columns:
                plt.plot(data.index, data['SMA_200'], label='SMA 200', alpha=0.7)

        plt.title(f'{ticker} - Cena Zamknięcia', fontsize=16, fontweight='bold')
        plt.xlabel('Data', fontsize=12)
        plt.ylabel('Cena (PLN/USD)', fontsize=12)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plot_indicators(self, data: pd.DataFrame, ticker: str = ""):
        """Rysuje wykresy wskaźników (RSI, MACD, Bollinger Bands)"""
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Cena i Bollinger Bands', 'RSI', 'MACD'),
            specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]]
        )

        # Cena i Bollinger Bands
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Close'],
                name='Close Price',
                mode='lines',
                line=dict(color='blue', width=2)
            ),
            row=1, col=1
        )

        if 'BB_High' in data.columns and 'BB_Low' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['BB_High'],
                    name='BB Upper',
                    mode='lines',
                    line=dict(color='red', width=1, dash='dash')
                ),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['BB_Low'],
                    name='BB Lower',
                    mode='lines',
                    line=dict(color='red', width=1, dash='dash')
                ),
                row=1, col=1
            )

        # RSI
        if 'RSI' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['RSI'],
                    name='RSI',
                    mode='lines',
                    line=dict(color='orange', width=2)
                ),
                row=2, col=1
            )

            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

        # MACD
        if 'MACD' in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['MACD'],
                    name='MACD',
                    mode='lines',
                    line=dict(color='purple', width=2)
                ),
                row=3, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['MACD_Signal'],
                    name='Signal',
                    mode='lines',
                    line=dict(color='red', width=2)
                ),
                row=3, col=1
            )

        fig.update_layout(
            title_text=f'{ticker} - Wskaźniki Techniczne',
            height=900,
            hovermode='x unified'
        )

        fig.show()

    def plot_volume(self, data: pd.DataFrame, ticker: str = ""):
        """Rysuje wykres wolumenu"""
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker=dict(color='lightblue')
            )
        )

        fig.update_layout(
            title=f'{ticker} - Wolumin Handlu',
            xaxis_title='Data',
            yaxis_title='Wolumin',
            hovermode='x unified'
        )

        fig.show()
