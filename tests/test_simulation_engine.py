import unittest
import pandas as pd
import numpy as np
from backtesting_engine.simulation_engine import SimulationEngine
from backtesting_engine.trading_strategies.moving_average_crossover import MovingAverageCrossoverStrategy

class TestSimulationEngine(unittest.TestCase):
    def setUp(self):
        date_range = pd.date_range(start='2020-01-01', periods=200, freq='D')
        self.data = pd.DataFrame({
            'Date': date_range,
            'Close': np.random.random(200) * 100
        })
        self.data.set_index('Date', inplace=True)
        self.strategy = MovingAverageCrossoverStrategy(short_window=40, long_window=100)
        self.signals = self.strategy.generate_signals(self.data)
        self.engine = SimulationEngine(initial_capital=10000, fraction_per_trade=0.1, transaction_cost=0.001, slippage=0.001)

    def test_simulate_trades(self):
        portfolio = self.engine.simulate_trades(self.signals)
        self.assertIsInstance(portfolio, pd.DataFrame, "Portfolio should be a DataFrame")
        self.assertIn('cash', portfolio.columns, "Portfolio DataFrame should have a 'cash' column")
        self.assertIn('value_of_shares', portfolio.columns, "Portfolio DataFrame should have a 'value_of_shares' column")
        self.assertIn('num_of_shares', portfolio.columns, "Portfolio DataFrame should have a 'num_of_shares' column")
        self.assertIn('total', portfolio.columns, "Portfolio DataFrame should have a 'total' column")
        self.assertIn('price_per_share', portfolio.columns, "Portfolio DataFrame should have a 'price_per_share' column")

if __name__ == "__main__":
    unittest.main()
