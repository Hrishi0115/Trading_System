import pandas as pd
import numpy as np
from backtesting_engine.risk_management import RiskManager

class SimulationEngine:
    def __init__(self, initial_capital: float, fraction_per_trade: float, transaction_cost: float = 0.0, slippage: float = 0.0, \
                 stop_loss_percentage: float = None, take_profit_percentage: float = None):
        self.initial_capital = initial_capital
        self.fraction_per_trade = fraction_per_trade
        self.transaction_cost = transaction_cost
        self.slippage = slippage
        self.cash = float(initial_capital)
        self.position_value = 0.0
        self.num_shares = 0.0
        self.portfolio_value = float(initial_capital)
        self.risk_manager = RiskManager(stop_loss_percentage, take_profit_percentage) if stop_loss_percentage is not None or take_profit_percentage is not None else None
        self.buy_price = None  # Track the buy price for risk management

    def simulate_trades(self, signals: pd.DataFrame) -> pd.DataFrame:
        portfolio = pd.DataFrame(index=signals.index, dtype=float)
        portfolio['num_of_shares'] = 0.0
        portfolio['price_per_share'] = np.nan    
        portfolio['value_of_shares'] = 0.0
        portfolio['cash'] = float(self.cash)
        portfolio['total'] = float(self.cash)
        portfolio['order'] = None

        for i in range(len(signals)):
            position = signals['positions'].iloc[i]
            price = signals['price'].iloc[i]

            # Apply stop loss/take profit if holding shares    
            if self.num_shares > 0 and self.risk_manager is not None:
                condition = self.risk_manager.check_conditions(self.buy_price, price, self.num_shares)
                if condition == 'stop_loss' or condition == 'take_profit':
                    position = -1.0  # Override to sell signal

            if position == 1.0:  # Buy signal
                num_shares_to_buy = (self.cash * self.fraction_per_trade) / price
                cost = num_shares_to_buy * price * (1 + self.transaction_cost + self.slippage)
                self.cash -= cost
                self.num_shares += num_shares_to_buy
                self.buy_price = price  # Set buy price for risk management
                portfolio.loc[signals.index[i], 'order'] = 'buy'

            elif position == -1.0 and self.num_shares > 0:  # Sell signal
                num_shares_to_sell = self.num_shares
                revenue = num_shares_to_sell * price * (1 - self.transaction_cost - self.slippage)
                self.cash += revenue
                self.num_shares -= num_shares_to_sell
                self.buy_price = None  # Reset buy price after selling
                portfolio.loc[signals.index[i], 'order'] = 'sell'

            self.position_value = self.num_shares * price
            portfolio.loc[signals.index[i], 'cash'] = float(self.cash)
            portfolio.loc[signals.index[i], 'num_of_shares'] = float(self.num_shares)
            portfolio.loc[signals.index[i], 'price_per_share'] = price
            portfolio.loc[signals.index[i], 'value_of_shares'] = float(self.position_value)
            portfolio.loc[signals.index[i], 'total'] = float(self.cash + self.position_value)

        self.portfolio_value = portfolio['total'].iloc[-1]
        return portfolio