import unittest
from unittest.mock import MagicMock
import pandas as pd
import numpy as np
from backtesting_engine.backtesting_framework import BacktestingFramework
from backtesting_engine.trading_strategies.moving_average_crossover import MovingAverageCrossoverStrategy

class TestBacktestingFramework(unittest.TestCase):

    def setUp(self):
        # Mock strategy
        self.strategy = MovingAverageCrossoverStrategy(short_window=40, long_window=100)
        self.strategy.generate_signals = MagicMock(return_value=self._generate_mock_signals())

        # Mock data loader
        self.loader = MagicMock()
        self.loader.load_data = MagicMock(return_value=self._generate_mock_data())

        # Mock simulation engine
        self.simulation_engine = MagicMock()
        self.simulation_engine.simulate_trades = MagicMock(return_value=self._generate_mock_portfolio())

        # Initialize the framework
        self.framework = BacktestingFramework(self.strategy, 10000, 0.1, loader=self.loader)

        # Replace simulation engine with mock
        self.framework.simulation_engine = self.simulation_engine

    def _generate_mock_data(self):
        dates = pd.date_range('2020-01-01', periods=100)
        data = pd.DataFrame(index=dates)
        data['Close'] = np.random.random(100) * 100
        return data

    def _generate_mock_signals(self):
        dates = pd.date_range('2020-01-01', periods=100)
        signals = pd.DataFrame(index=dates)
        signals['price'] = np.random.random(100) * 100
        signals['short_mavg'] = signals['price'].rolling(window=10).mean()
        signals['long_mavg'] = signals['price'].rolling(window=40).mean()
        signals['signal'] = np.where(signals['short_mavg'] > signals['long_mavg'], 1.0, 0.0)
        signals['positions'] = signals['signal'].diff()
        return signals

    def _generate_mock_portfolio(self):
        dates = pd.date_range('2020-01-01', periods=100)
        portfolio = pd.DataFrame(index=dates)
        portfolio['total'] = np.cumsum(np.random.random(100) - 0.5) * 1000
        return portfolio

    def test_run_backtest(self):
        metrics = self.framework.run_backtest("NVDA", "2020-01-01", "2022-01-01")
        self.assertIsInstance(metrics, dict)
        self.assertTrue("total_return" in metrics)
        self.assertTrue("cagr" in metrics)
        self.assertTrue("volatility" in metrics)
        self.assertTrue("sharpe_ratio" in metrics)
        self.assertTrue("max_drawdown" in metrics)

if __name__ == '__main__':
    unittest.main()
