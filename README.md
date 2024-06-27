# System Design

<!-- ## Project Structure

1. Strategy Editor
- Function: Provides an interface for users to create and modify trading strategies (from well-known/common or proprietary strategies or develop completely new strategies - but interface still provides support, guidance when developing strategies from scratch)
- Output: Generate strategies that can be passed to the backtesting engine

2. Backtesting Engine
- Function: Simulate trades using the provided strategies and historical data
- Input: Accept strategies from the strategy editor, or predefined strategies for testing purposes
- Output: Generate performance metrics and visualisations to evaluate the strategies

3. Trading Bot Builder (Build-a-bot)
- Function: Execute trades in real-time based on the strategies
- Input: Accept strategies from the strategy editor or predefined strategies for testing purposes
- Output: Generate performance metrics and visualisations to evaluate the strategies -->

<!-- ## Understanding Trading Strategies

#### Backtesting vs. Live Trading (Paper or Real)

1. Backtesting Strategies
- Purpose: Evaluate the performance of a trading stategy using historical data
- Implementation: Generate buy/sell signals based on historical data
- Environment: Static, using pre-existing data to simulate trades and assess performance
- Components: Implemented within the backtesting engine to test and validate strategies

2. Live Trading Strategies
- Purpose: Generate real-time buy/sell signals based on live market data
- Implementation: Continuously fetch and process live data to generate signals
- Environment: Dynamic, reacting to incoming data in real-time
- Components: Typically implemented within a trading bot or live trading system

## System Design

Given that the backtesting and live trading strategies have different requirements, it makes sense to separate the concerns while maintaining some shared logic where possible. 

#### Potential approach

1. Backtesting Strategy Class: Focused on generating signals from historical data
2. Live Trading Strategy Class: Focused on generating signals from live data, possible extending the backtesting strategy logic

 -->

## Overview
An overview of the complete system and how each component interacts:

1. Strategy Editor: Allows users to create and modify trading strategies.
2. Backtesting Engine: Evaluate the performance of trading strategies using historical data.
3. Metrics Calculator: Provides performance metrics (and visualisations) to assess the effectiveness of strategies.
4. Trading Bots (Build-a-Bot): Executes trades in real-time based on the strategies.
5. Data Loader: Fetches historical and live market data

## Components and Interactions
1. Strategy Editor
- Function: Allows users to define and modify trading strategies
- Output: Generate strategy configurations that can be used the backtesting engine and trading bots

2. Backtesting Engine
- Function: Simulates trades based on historical data to evaluate the performance of strategies
- Input: Accepts strategies from the strategy editor (or predefined/proprietary strategies offered by the editor)
- Output: Provides performance metrics and visualisations

3. Metrics Calculator (for both backtesting and paper/real live trading)
- Function: Calculates various performance metrics such as total return, Sharpe ratio, drawdown, etc
- Input: Receives trade and portfolio data from the backtesting engine
- Output: Provides a summary of performance metrics

4. Trading Bots (Build-a-Bot)
- Function: Executes trades in real-time using live market data
- Input: Accepts strategies from the strategy editor
- Output: Real-time trade execution and monitoring

5. Data Loader
- Function: Fetches historical data for backtesting and live data for trading bots
- Output: Provides data in a format suitable for strategies

## Detailed Design

1. Strategy Editor Modules:
- User interface (UI) to define strategies (intuitive drag-and-drop interface and advanced code editor - maybe even write our own custom scripting language - great educational opportunity)
- Backend to save and export strategy configurations

2. Backtesting Engine Modules:
- Strategy Loader: Load strategy configurations
- Simulation Engine: Simulates trades based on historical data
- Metrics Calculator: Computes performance metrics
- Visualisation: Plots result

3. Metrics Calculator Modules (Embedded system of the backtesting engine)
- Performance Metrics: Calculates metrics like return, Sharpe ratio, etc
- Summary Report: Generates a report of performance metrics

4. Trading Bots Modules
- Live Data Loader: Fetches live market data
- Signal Generator: Generates buy/sell signals based on live data
- Trade Executor: Executes trade in real-time

5. Data Loader Modules
- Historical Data Loader: Fetches historical market data
- Live Data Loader: Fetches live market data

## Integration Workflow

1. Create Strategy
- Users define strategies in the Strategy Editor
- Strategy configurations are saved and can be exported to the backtesting engine and trading bots

2. Backtest Strategy
- Strategy Loader loads the strategy configuration
- Data Loader fetches historical data
- Simulation Engine runs the strategy on historical data
- Metrics Calculator computes performance metrics
- Visualisation plots the backtest results
- Performance metrics and visualisations are presented to the user

3. Deploy Strategy to Trading Bot
- Strategy configuration is loaded to the trading bot
- Live Data Loader fetches real-time market data
- Signal Generator uses live data to generate buy/sell signals
- Trade Executor executes trades in real-time based on signals

## Example Classes & Methods
1. Strategy Editor
```python
class StrategyEditor:
    # UI for defining strategies
    pass

class StrategyConfig:
    # Represents strategy configuration
    pass
```

2. Backtesting Engine
```python
class BacktestingEngine:
    # runs the backtest
    def load_strategy(config: StrategyConfig):
        pass
    
    def run_backtest(data: pd.DataFrame):
        pass

    def calculate_metrics(trades: List[Trade]):
        pass

    def plot_results():
        pass
```

3. Metrics Calculator
```python
class MetricsCalculator:
    # computes performance metrics
    def calculate(trades: List[Trade]):
        pass
```

4. Trading Bot

```python
class TradingBot:
    # executes trades in real-time
    def load_strategy(config: StrategyConfig):
        pass

    def fetch_live_data():
        pass

    def generate_signals():
        pass

    def execute_trade(signal: Signal):
        pass
```

5. Data Loader
```python
class HistoricalDataLoader:
    # fetches historical data
    def load_data(symbol: str, start_date: str, end_date: str):
        pass

class LiveDataLoader:
    # fetches live data
    def fetch_data(symbol: str):
        # would also have to specify timeframe - how often data is being fetched
```


