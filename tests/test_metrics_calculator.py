import unittest
import pandas as pd
import numpy as np
from backtesting_engine.metrics_calculator import MetricsCalculator

class TestMetricsCalculator(unittest.TestCase):
    def setUp(self):
        dates = pd.date_range(start='2020-01-01', periods=252)
        total_values = 10000 * (1 + np.random.randn(252).cumsum() / 100)
        self.portfolio = pd.DataFrame({'total': total_values}, index=dates)
        self.metrics = MetricsCalculator()

    def test_calculate_total_return(self):
        total_return = self.metrics.calculate_total_return(self.portfolio)
        self.assertIsInstance(total_return, float, "Total return should be a float")

    def test_calculate_cagr(self):
        cagr = self.metrics.calculate_cagr(self.portfolio)
        self.assertIsInstance(cagr, float, "CAGR should be a float")

    def test_calculate_volatility(self):
        volatility = self.metrics.calculate_volatility(self.portfolio)
        self.assertIsInstance(volatility, float, "Volatility should be a float")

    def test_calculate_sharpe_ratio(self):
        sharpe_ratio = self.metrics.calculate_sharpe_ratio(self.portfolio)
        self.assertIsInstance(sharpe_ratio, float, "Sharpe ratio should be a float")

    def test_calculate_max_drawdown(self):
        max_drawdown = self.metrics.calculate_max_drawdown(self.portfolio)
        self.assertIsInstance(max_drawdown, float, "Max drawdown should be a float")

if __name__ == "__main__":
    unittest.main()
