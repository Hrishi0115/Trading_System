from backtesting_engine.data_loader import YahooFinanceLoader
from backtesting_engine.simulation_engine import SimulationEngine
from backtesting_engine.metrics_calculator import MetricsCalculator
from backtesting_engine.visualization import Visualizer

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
        self.visualizer.all_visualizations(portfolio, signals, symbol)

        return metrics
