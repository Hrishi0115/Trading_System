# Responsible for creating visualizations to help analyze the performance of the trading strategies.
# This might include plotting equity curves, drawdowns, and other performance metrics.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import inspect

class Visualizer:
    def __init__(self):
        pass

    def plot_portfolio_value(self, portfolio: pd.DataFrame):
        plt.figure(figsize=(14, 7))
        plt.plot(portfolio.index, portfolio['total'], label='Portfolio Total')
        plt.xlabel('Date')
        plt.ylabel('Total Value')
        plt.title('Portfolio Total Value Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_signals(self, signals: pd.DataFrame):
        plt.figure(figsize=(14, 7))
        plt.plot(signals.index, signals['price'], color='black')
        plt.plot(signals.index, signals['short_mavg'], label='Short-term SMA', color='blue')
        plt.plot(signals.index, signals['long_mavg'], label='Long-term SMA', color='red')

        # Plot buy signals
        buy_signals = signals[signals['positions'] == 1.0]
        plt.plot(buy_signals.index, buy_signals['price'], '^', markersize=10, color='g', label='Buy Signal', lw=0)

        # Plot sell signals
        sell_signals = signals[signals['positions'] == -1.0]
        plt.plot(sell_signals.index, sell_signals['price'], 'v', markersize=10, color='r', label='Sell Signal', lw=0)

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Price and Buy/Sell Signals')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_orders(self, portfolio: pd.DataFrame):
        orders = portfolio[['price_per_share','order']][portfolio['order'].notna()]
        plt.figure(figsize=(14,7))
        plt.plot(portfolio.index, portfolio['price_per_share'], color='black')
        
        # plot buy order
        buy_orders = orders[orders['order'] == 'buy']
        plt.plot(buy_orders.index, buy_orders['price_per_share'], '^', markersize=10, color='g', label='Buy Signal', lw=0)

        # plot sell order
        sell_orders = orders[orders['order'] == 'sell']
        plt.plot(sell_orders.index, sell_orders['price_per_share'], 'v', markersize=10, color='r', label='Sell Signal', lw=0)

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Price and Buy/Sell Orders')
        plt.legend()
        plt.show()

    def all_visualizations(self, portfolio: pd.DataFrame, signals: pd.DataFrame):
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        plot_methods = [method for name, method in methods if name.startswith('plot_')]
        for plot_method in plot_methods:
            # Check the method signature to determine the appropriate argument
            sig = inspect.signature(plot_method)
            if 'portfolio' in sig.parameters:
                plot_method(portfolio)
            elif 'signals' in sig.parameters:
                plot_method(signals)

        # alternatively
        # self.plot_portfolio_value(portfolio)
        # self.plot_signals(signals)



# Example usage
if __name__ == "__main__":
    from data_loader import YahooFinanceLoader
    from trading_strategies.moving_average_crossover import MovingAverageCrossoverStrategy
    from backtesting_engine.simulation_engine import SimulationEngine

    loader = YahooFinanceLoader()
    data = loader.load_data('AAPL', '2020-01-01', '2024-07-01')

    strategy = MovingAverageCrossoverStrategy(40, 80)

    signals = strategy.generate_signals(data)

    engine = SimulationEngine(10000, 0.1)

    portfolio = engine.simulate_trades(signals)

    # mask = signals['positions'] != 0.0
    # print(signals[mask])
    # print(portfolio)

    visualizer = Visualizer()
    # visualizer.plot_portfolio_value(portfolio)
    # visualizer.plot_signals(signals)
    visualizer.all_visualizations(portfolio, signals)
