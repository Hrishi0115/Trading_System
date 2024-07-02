import unittest
import pandas as pd
import numpy as np
from backtesting_engine.visualization import Visualizer

class TestVisualizer(unittest.TestCase):

    def setUp(self):
        # Create a simple test portfolio DataFrame
        dates = pd.date_range('2020-01-01', periods=100)
        self.portfolio = pd.DataFrame(index=dates)
        self.portfolio['total'] = np.cumsum(np.random.random(100) - 0.5) * 1000

        # Create a simple test signals DataFrame
        self.signals = pd.DataFrame(index=dates)
        self.signals['price'] = np.cumsum(np.random.random(100) - 0.5) * 100
        self.signals['short_mavg'] = self.signals['price'].rolling(window=10).mean()
        self.signals['long_mavg'] = self.signals['price'].rolling(window=40).mean()
        self.signals['signal'] = np.where(self.signals['short_mavg'] > self.signals['long_mavg'], 1.0, 0.0)
        self.signals['positions'] = self.signals['signal'].diff()

    def test_plot_portfolio_value(self):
        visualizer = Visualizer()
        try:
            visualizer.plot_portfolio_value(self.portfolio)
        except Exception as e:
            self.fail(f"plot_portfolio_value() raised {e} unexpectedly!")

    def test_plot_signals(self):
        visualizer = Visualizer()
        try:
            visualizer.plot_signals(self.signals)
        except Exception as e:
            self.fail(f"plot_signals() raised {e} unexpectedly!")

    def test_all_visualizations(self):
        visualizer = Visualizer()
        try:
            visualizer.all_visualizations(self.portfolio, self.signals)
        except Exception as e:
            self.fail(f"all_visualizations() raised {e} unexpectedly!")

if __name__ == '__main__':
    unittest.main()
