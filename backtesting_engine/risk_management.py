# Contains logic for applying risk management rules, such as stop-loss and take-profit levels.
# This module ensures trades are executed within the risk parameters set by the strategy.

import pandas as pd

class RiskManager:
    def __init__(self, stop_loss_percentage: float = None, take_profit_percentage: float = None):
        self.stop_loss_percentage = stop_loss_percentage
        self.take_profit_percentage = take_profit_percentage

    def check_conditions(self, buy_price: float, current_price: float, position: int) -> str:
        # since we may consider short selling later - may be appropriate to switch `buy_price` to `order_price`
        if position > 0: # Long position
            if self.stop_loss_percentage is not None and current_price <= buy_price * (1 - self.stop_loss_percentage):
                return 'stop_loss'
            
            elif self.take_profit_percentage is not None and current_price >= buy_price * (1 + self.take_profit_percentage):
                return 'take_profit'
            
        elif position < 0: # short position (if applicable)
            if self.stop_loss_percentage is not None and current_price >= buy_price * (1 - self.stop_loss_percentage):
                return 'stop_loss'
            
            elif self.take_profit_percentage is not None and current_price <= buy_price * (1 + self.take_profit_percentage):
                return 'take_profit'
        
        return 'hold'
    
