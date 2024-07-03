# Holds configuration settings for the trading strategies. This can include parameters like moving average windows, position
# sizing rules, and any other settings required by the strategies.

from abc import ABC, abstractmethod

class StrategyConfig(ABC):
    @abstractmethod
    def get_config(self):
        pass

class MovingAverageCrossoverConfig(StrategyConfig):
    def __init__(self, short_window=40, long_window=100):
        self.short_window = short_window
        self.long_window = long_window

    def get_config(self):
        return {
            "short_window": self.short_window,
            "long_window": self.long_window,
        }
