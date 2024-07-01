# Responsible for creating visualizations to help analyze the performance of the trading strategies.
# This might include plotting equity curves, drawdowns, and other performance metrics.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Visualizer:
    @staticmethod
    def plot_portfolio_value(portfolio: pd.DataFrame):
        plt.figure(figsize=(14,7))
        plt.plot(portfolio.index, portfolio['total'], label='Portfolio Total')
        plt.xlabel('Date')
        plt.ylabel('Total Value')
        plt.title('Portfolio Total Value Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    @staticmethod
    def plot_signals(signals: pd.DataFrame):
        plt.figure(figsize=(14,7))
        plt.plot(signals.index, signals['price'], color='black')
        plt.plot(signals.index, signals['short_mavg'], label='Short-term SMA', color='blue')
        plt.plot(signals.index, signals['long_mavg'], label='Long-term SMA', color='red')

        # plot buy signals

        buy_signals = signals[signals['positions'] == 1.0]
        plt.plot(buy_signals.index, buy_signals['price'], '^', markersize=10, color='g', label='Buy Signal', lw=0)
        
        # plot sell signals
        sell_signals = signals[signals['positions'] == -1.0]
        plt.plot(sell_signals.index, sell_signals['price'], '^', markersize=10, color='r', label='Sell Signal', lw=0)

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Price and Buy/Sell Signals')
        plt.legend()
        plt.grid(True)
        plt.show()

# Example usage
if __name__ == "__main__":
    from data_loader import YahooFinanceLoader
    from trading_strategies.moving_average_crossover import MovingAverageCrossoverStrategy
    from simulation_engine import SimulationEngine

    loader = YahooFinanceLoader()
    data = loader.load_data('NVDA', '2020-01-01', '2022-01-01')

    strategy = MovingAverageCrossoverStrategy(40, 100)

    signals = strategy.generate_signals(data)

    engine = SimulationEngine(10000, 0.1)

    portfolio = engine.simulate_trades(signals)

    mask = signals['positions'] != 0.0
    print(signals[mask])
    print(portfolio)

    visualizer = Visualizer()
    visualizer.plot_portfolio_value(portfolio)
    visualizer.plot_signals(signals)

