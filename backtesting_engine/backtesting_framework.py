#  contains the overall structure and logic to set up and run the backtesting framework. It might include methods to initialize
#  and manage the entire backtesting process, bringing together all the other modules
from data_loader import YahooFinanceLoader
from simulation_engine import SimulationEngine
from metrics_calculator import MetricsCalculator
from visualization import Visualizer

# testing a strategy's performance for a given stock over a specified time

class BacktestingFramework:
    def __init__(self, strategy, initial_capital, fraction_per_trade, loader=YahooFinanceLoader, risk_free_rate=None):
        # strategy is given
        self.strategy = strategy
        
        # initialize data loader
        self.data_loader = loader()

        # initialize simulation engine
        self.simulation_engine = SimulationEngine(initial_capital, fraction_per_trade)

        # initialize metrics calculator
        self.metrics_calculator = MetricsCalculator(risk_free_rate=risk_free_rate) if risk_free_rate is not None else MetricsCalculator()

        # initialize visualizer
        self.visualizer = Visualizer()

    def run_backtest(self, symbol, start_date, end_date):
        # Step 1: Load historical data
        data = self.data_loader.load_data(symbol, start_date, end_date) # will need to add a timeframe parameter to specify trading frequency, e.g. minute, hour, day, etc.
        # if no start and end date is specified run backtest for the past two years
        # implement here ...

        # Step 2: Generate signals
        signals = self.strategy.generate_signals(data)

        # Step 3: Simulate trades
        portfolio = self.simulation_engine.simulate_trades(signals)

        # Step 4: Calculate metrics
        metrics = self.metrics_calculator.calculate_all_metrics(portfolio)

        # Step 5: Visualize results
        self.visualizer.all_visualizations(portfolio, signals)

        return metrics

# Example usage
if __name__ == "__main__":
    # Import configuration
    from strategy_config import MovingAverageCrossoverConfig
    from trading_strategies.moving_average_crossover import MovingAverageCrossoverStrategy
    
    # Initialize configuration
    config = MovingAverageCrossoverConfig(short_window=40, long_window=100)
    strategy = MovingAverageCrossoverStrategy(**config.get_config()) # is this needed?

    # Create the framework with the appropriate strategy config
    framework = BacktestingFramework(strategy, 10000, 0.1)
    # separate order sizing from engine to strategy?
    
    # Run the backtest
    backtest = framework.run_backtest("NVDA", "2020-01-01", "2022-01-01")
    print(backtest)

# Improvements
# Order Sizing:
# Separating order sizing from the engine to the strategy can provide more flexibility and adhere to the single responsibility principle.
# Each strategy can have its own logic for determining position sizes.

# Error Handling and Validation:
# Adding error handling and validation (e.g., checking if the data loader returns valid data) can make the framework more robust.

# Documentation:
# Ensure that each method and class is well-documented, making it easier for others (and your future self) to understand and use the code.