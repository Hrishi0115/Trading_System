import pandas as pd
import numpy as np

class MetricsCalculator:
    # a static method is a method that belongs to a class rather than an instance of the class - no access to instance or class variable (self / cls)
    @staticmethod
    def calculate_total_return(portfolio: pd.DataFrame) -> float:
        # Total Return: the overall return of the portfolio over the backtesting period
        total_return = (portfolio['total'].iloc[-1] / portfolio['total'].iloc[0]) - 1
        return total_return
    
    @staticmethod
    def calculate_cagr(portfolio: pd.DataFrame, periods_per_year: int = 252) -> float:
        # CAGR (Compound Annual Growth Rate): the annual growth rate of the portfolio
        num_years = len(portfolio) / periods_per_year
        cagr = (portfolio['total'].iloc[-1] / portfolio['total'].iloc[0]) ** (1 / num_years) - 1
        return cagr
    
    @staticmethod
    def calculate_volatility(portfolio: pd.DataFrame, periods_per_year: int = 252) -> float:
        # Volatility: the standard deviation of the portfolio returns, including risk
        daily_returns = portfolio['total'].pct_change().dropna()
        volatility = daily_returns.std() * np.sqrt(periods_per_year)
        return volatility
    
    @staticmethod
    def calculate_sharpe_ratio(portfolio: pd.DataFrame, risk_free_rate: float = 0.0, periods_per_year: int = 252) -> float:
        # Sharpe Ratio: the risk-adjusted return of the portfolio
        daily_returns = portfolio['total'].pct_change().dropna()
        excess_returns = daily_returns - risk_free_rate / periods_per_year
        sharpe_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(periods_per_year)
        return sharpe_ratio
    
    @staticmethod
    def calculate_max_drawdown(portfolio: pd.DataFrame) -> float:
        # Max Drawdown: the maximum observed loss from a peak to a trough
        cumulative_returns = portfolio['total'] / portfolio['total'].iloc[0]
        peak = cumulative_returns.expanding(min_periods=1).max()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()
        return max_drawdown
    
# Example usage
if __name__ == "__main__":
    # Sample data for testing
    dates = pd.date_range(start='2020-01-01', periods=252)
    total_values = 10000 * (1 + np.random.randn(252).cumsum() / 100)
    portfolio = pd.DataFrame({'total': total_values}, index=dates)

    metrics = MetricsCalculator()
    print("Total Return:", metrics.calculate_total_return(portfolio))
    print("CAGR:", metrics.calculate_cagr(portfolio))
    print("Volatility:", metrics.calculate_volatility(portfolio))
    print("Sharpe Ratio:", metrics.calculate_sharpe_ratio(portfolio))
    print("Max Drawdown:", metrics.calculate_max_drawdown(portfolio))