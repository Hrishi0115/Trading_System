import unittest
import pandas as pd
import numpy as np
from backtesting_engine.trading_strategies.moving_average_crossover import MovingAverageCrossoverStrategy

class TestSimpleMovingAverageCrossoverStrategy(unittest.TestCase):
    def setUp(self):
        # Setup some sample data
        date_range = pd.date_range(start='2020-01-01', periods=200, freq='D')
        self.data = pd.DataFrame({
            'Date': date_range,
            'Close': np.random.random(200) * 100
        })
        self.data.set_index('Date', inplace=True)
        self.strategy = MovingAverageCrossoverStrategy(short_window=40, long_window=100)

    def test_generate_signals(self):
        signals = self.strategy.generate_signals(self.data)
        self.assertIsInstance(signals, pd.DataFrame, "Signals should be a DataFrame")
        self.assertIn('price_per_share', signals.columns, "Signals DataFrame should have a 'price' column")
        self.assertIn('short_mavg', signals.columns, "Signals DataFrame should have a 'short_mavg' column")
        self.assertIn('long_mavg', signals.columns, "Signals DataFrame should have a 'long_mavg' column")
        self.assertIn('signal', signals.columns, "Signals DataFrame should have a 'signal' column")
        self.assertIn('positions', signals.columns, "Signals DataFrame should have a 'positions' column")

if __name__ == "__main__":
    unittest.main()
