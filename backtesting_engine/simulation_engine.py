import pandas as pd
import numpy as np

class SimulationEngine:
    def __init__(self, initial_capital: float, fraction_per_trade: float, transaction_cost: float = 0.0, slippage: float = 0.0):
        self.initial_capital = initial_capital
        self.fraction_per_trade = fraction_per_trade
        self.transaction_cost = transaction_cost
        self.slippage = slippage
        self.cash = float(initial_capital)
        self.position_value = 0.0
        self.num_shares = 0.0
        self.portfolio_value = float(initial_capital)

    def simulate_trades(self, signals: pd.DataFrame) -> pd.DataFrame:
        # Initialize portfolio values with float dtype
        portfolio = pd.DataFrame(index=signals.index, dtype=float)
        portfolio['num_of_shares'] = 0.0
        portfolio['price_per_share'] = np.nan    
        portfolio['value_of_shares'] = 0.0
        portfolio['cash'] = float(self.cash)
        portfolio['total'] = float(self.cash)

        for i in range(len(signals)):
            position = signals['positions'].iloc[i]
            price = signals['price'].iloc[i]
            
            if position == 1.0:  # Buy signal
                # Calculate the exact number of shares to buy
                num_shares_to_buy = (self.cash * self.fraction_per_trade) / price
                cost = num_shares_to_buy * price * (1 + self.transaction_cost + self.slippage)
                self.cash -= cost
                self.num_shares += num_shares_to_buy

            elif position == -1.0 and self.num_shares > 0:  # Sell signal
                num_shares_to_sell = self.num_shares
                revenue = num_shares_to_sell * price * (1 - self.transaction_cost - self.slippage)
                self.cash += revenue
                self.num_shares -= num_shares_to_sell

            self.position_value = self.num_shares * price
            portfolio.loc[signals.index[i], 'cash'] = float(self.cash)
            portfolio.loc[signals.index[i], 'num_of_shares'] = float(self.num_shares)
            portfolio.loc[signals.index[i], 'price_per_share'] = price
            portfolio.loc[signals.index[i], 'value_of_shares'] = float(self.position_value)
            portfolio.loc[signals.index[i], 'total'] = float(self.cash + self.position_value)
        
        self.portfolio_value = portfolio['total'].iloc[-1]
        return portfolio
    
if __name__ == '__main__':
    from backtesting_engine.trading_strategies.moving_average_crossover import MovingAverageCrossoverStrategy
    from backtesting_engine.data_loader import YahooFinanceLoader

    strategy = MovingAverageCrossoverStrategy(short_window=40, long_window=100)
    loader = YahooFinanceLoader()
    data = loader.load_data('AAPL', '2020-01-01', '2022-01-01')

    signals = strategy.generate_signals(data)

    engine = SimulationEngine(initial_capital=10000, fraction_per_trade=0.1, transaction_cost=0.001, slippage=0.001)
    portfolio = engine.simulate_trades(signals)
    print(portfolio)