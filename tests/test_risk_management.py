import unittest
import pandas as pd
import numpy as np
from backtesting_engine.risk_management import RiskManager

class TestRiskManager(unittest.TestCase):
    def test_check_conditions_with_stop_loss(self):
        risk_manager = RiskManager(stop_loss_percentage=0.05)
        buy_price = 100
        current_price = 90
        position = 10
        condition = risk_manager.check_conditions(buy_price, current_price, position)
        self.assertEqual(condition, 'stop_loss')

        current_price = 95
        condition = risk_manager.check_conditions(buy_price, current_price, position)
        self.assertEqual(condition, 'hold')

    def test_check_conditions_with_take_profit(self):
        risk_manager = RiskManager(take_profit_percentage=0.1)
        buy_price = 100
        current_price = 110
        position = 10
        condition = risk_manager.check_conditions(buy_price, current_price, position)
        self.assertEqual(condition, 'take_profit')

        current_price = 105
        condition = risk_manager.check_conditions(buy_price, current_price, position)
        self.assertEqual(condition, 'hold')

    def test_check_conditions_with_both(self):
        risk_manager = RiskManager(stop_loss_percentage=0.05, take_profit_percentage=0.1)
        buy_price = 100
        current_price = 90
        position = 10
        condition = risk_manager.check_conditions(buy_price, current_price, position)
        self.assertEqual(condition, 'stop_loss')

        current_price = 110
        condition = risk_manager.check_conditions(buy_price, current_price, position)
        self.assertEqual(condition, 'take_profit')

        current_price = 95
        condition = risk_manager.check_conditions(buy_price, current_price, position)
        self.assertEqual(condition, 'hold')

if __name__ == "__main__":
    unittest.main()
