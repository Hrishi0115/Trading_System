from abc import ABC, abstractmethod
import pandas as pd


class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on the strategy logic.

        Args:
        - data (pd.DataFrame): DataFrame containing historical price data.

        Returns:
        - pd.DataFrame: DataFrame with generated trading signals
        """
        pass