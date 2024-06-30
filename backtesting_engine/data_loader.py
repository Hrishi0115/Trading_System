# Contains the abstract class for data loaders and concrete implementations like `YahooFinanceLoader`

from abc import ABC, abstractmethod
import pandas as pd
import yfinance as yf

class DataLoader(ABC):
    @abstractmethod
    def load_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        pass

class YahooFinanceLoader(DataLoader):
    def load_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        ticker = yf.Ticker(symbol) # convert symbol into ticker object

        data = ticker.history(start=start_date, end=end_date) # fetch historical data from YahooFinance

        # data.reset_index(inplace=True) keep date as the index
        # data['Date'] = pd.to_datetime(data['Date'])

        data.index = data.index.tz_localize(None) # transform date format from `YYYY-MM-DD HH:MM:SS(negative offset/-)HH:MM`
        # e.g. 2020-12-17 00:00:00-05:00
        # last part represents the offset from UTC
        # sign (-) indicates whether the offset is behind or ahead from UTC
        # to `YYYY-MM-DD` for ease of use

        return data