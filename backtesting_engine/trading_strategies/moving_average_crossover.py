import pandas as pd
import numpy as np
from .base_strategy import Strategy

class MovingAverageCrossoverStrategy(Strategy):
    def __init__(self, short_window: int, long_window: int):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        
        # create a new DataFrame named `signals`, using the same index (`Date`) as the `data` DataFrame, and a price column that is the same as the close price

        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['Close']

        # Calculate Long and Short Moving Averages omitting signals from incomplete windows - alternative versions provided below

        # signals['short_mavg'] = data['Close'].rolling(window=self.short_window, min_periods=1).mean()
        # signals['long_mavg'] = data['Close'].rolling(window=self.long_window, min_periods=1).mean()

        signals['short_mavg'] = data['Close'].rolling(window=self.short_window).mean()
        signals['long_mavg'] = data['Close'].rolling(window=self.long_window).mean()

        # Filter out rows where long_mavg (and short_mavg) are NaN - with moving average strategies, we ignore signals generated from incomplete windows
        
        signals.dropna(inplace=True)

        # Initialize the `signal` column with 0.0 - this column is used to store the trading signals

        signals['signal'] = 0.0

        # Generate buy/sell signals based on the crossover

        # .loc[row_indexer, column_indexer] - i.e. .loc[:, 'signal'] - : is used to select all rows, and 'signal' specfies the column(s) to be selected

        # when the short moving average is greater than the long moving average (np.where(short > long)), a buy signal (1.0) is generated and a sell signal (0.0) is generated
        # when the short moving average is lower than the long moving average

        signals['signal'] = np.where(signals['short_mavg'] > signals['long_mavg'], 1.0, 0.0)

        # # Calculate position size based on fraction of portfolio
        # portfolio_value = self.initial_capital
        # position_size = portfolio_value * self.fraction_per_trade
        # signals['position_size'] = signals['signal'] * position_size / signals['price']

        signals['positions'] = signals['signal'].diff()
        
        # create positions based on the signals
        # positions column is created by taking the difference of the signal column
        # diff() compares value i to value i - 1, therefore for first value, diff is NaN
        # and so if you visualise the short and long term - 0,0,0,0,1,1,1,1 -> short is lower than high (0.0) until value 4 implying that now short is higher than low -> so BUY!
        # position = [NaN, 0, 0, 0, 1, 0, 0, 0]
        # on the other hand
        # 1,1,1,1,0,0,... -> short is higher than low until value 5
        # positions = [NaN, 0, 0, 0, -1, 0] -> -1 is a SELL

        return signals
        
# The current implementation of the strategy with basic risk management and order sizing is primarily for testing the backtesting engine. The focus here is to ensure that
# the backtesting engine can handle the basic workflow of loading data, generating signals, simulating trades, and tracking the portfolio.

# Future Enhancements in the Strategy Editor
# When developing the strategy editor, we can introduce much more sophisticated methods for risk management and order sizing including:
# Advanced Position Sizing:
# 1. Fixed Fractional Method: Allocate a fixed percentage of the total capital to each trade.
# 2. Volatility-Based Position Sizing: Adjust position sizes based on the volatility of the asset.
# 3. Kelly Criterion: A formula to determine the optimal size of a series of bets to maximize the logarithm of wealth.
# 4. Value-at-Risk (VaR): Allocate capital based on the value-at-risk for each trade, limiting the potential loss to a certain threshold.

# Advanced Risk Management:
# 1. Dynamic Stop-Loss and Take-Profit: Adjust stop-loss and take-profit levels based on market conditions.
# 2. Trailing Stop-Loss: A stop-loss order that moves with the price to lock in profits while limiting losses.
# 3. Portfolio-Level Risk Management: Methods to manage overall portfolio risk, such as maximum drawdown limits, diversification rules, and rebalancing strategies.
