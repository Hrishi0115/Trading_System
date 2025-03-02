import pandas as pd
import numpy as np
from backtesting_engine.utility import get_risk_free_rate

class MetricsCalculator:
    def __init__(self, risk_free_rate: float = get_risk_free_rate(), periods_per_year: int = 252):
        # theoretical rate of return of an investment with zero risk - represents the return on an investment that is considered free any of any risk of financial loss.
        # the most common proxy for the risk-free rate is the yield on government bonds, such as US Treasury Bills, Bonds, etc.
        # 
        self.risk_free_rate = risk_free_rate
        self.periods_per_year = periods_per_year

    def calculate_total_return(self, portfolio: pd.DataFrame) -> float:
        # Total Return: the overall return of the portfolio over the backtesting period
        total_return = (portfolio['total'].iloc[-1] / portfolio['total'].iloc[0]) - 1
        return total_return
    
    def calculate_cagr(self, portfolio: pd.DataFrame) -> float:
        # CAGR (Compound Annual Growth Rate): the annual growth rate of the portfolio
        num_years = len(portfolio) / self.periods_per_year
        cagr = (portfolio['total'].iloc[-1] / portfolio['total'].iloc[0]) ** (1 / num_years) - 1
        return cagr
    
    def calculate_volatility(self, portfolio: pd.DataFrame) -> float:
        # Volatility: the standard deviation of the portfolio returns, including risk
        daily_returns = portfolio['total'].pct_change().dropna()
        volatility = daily_returns.std() * np.sqrt(self.periods_per_year)
        return volatility
    
    def calculate_sharpe_ratio(self, portfolio: pd.DataFrame) -> float:
        # Sharpe Ratio: the risk-adjusted return of the portfolio
        daily_returns = portfolio['total'].pct_change().dropna()
        excess_returns = daily_returns - self.risk_free_rate / self.periods_per_year
        sharpe_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(self.periods_per_year)
        return sharpe_ratio
    
    def calculate_max_drawdown(self, portfolio: pd.DataFrame) -> float:
        # Max Drawdown: the maximum observed loss from a peak to a trough
        cumulative_returns = portfolio['total'] / portfolio['total'].iloc[0]
        peak = cumulative_returns.expanding(min_periods=1).max()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()
        return max_drawdown
    
    def calculate_all_metrics(self, portfolio: pd.DataFrame) -> dict:
        # Calculate all metrics and return as a dictionary
        metrics = {
            "total_return": self.calculate_total_return(portfolio),
            "cagr": self.calculate_cagr(portfolio),
            "volatility": self.calculate_volatility(portfolio),
            "sharpe_ratio": self.calculate_sharpe_ratio(portfolio),
            "max_drawdown": self.calculate_max_drawdown(portfolio),
            "value": portfolio['total'].iloc[-1]
        }
        return metrics
    
# Example usage
if __name__ == "__main__":
    # Sample data for testing
    dates = pd.date_range(start='2020-01-01', periods=252)
    total_values = 10000 * (1 + np.random.randn(252).cumsum() / 100)
    portfolio = pd.DataFrame({'total': total_values}, index=dates)

    metrics = MetricsCalculator()
    print("Total Return:", metrics.calculate_total_return(portfolio))
    # print("CAGR:", metrics.calculate_cagr(portfolio))
    # print("Volatility:", metrics.calculate_volatility(portfolio))
    # print("Sharpe Ratio:", metrics.calculate_sharpe_ratio(portfolio))
    # print("Max Drawdown:", metrics.calculate_max_drawdown(portfolio))
    print(metrics.calculate_all_metrics(portfolio)['total_return'])