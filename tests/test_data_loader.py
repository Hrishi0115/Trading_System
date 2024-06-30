import unittest
import pandas as pd
from backtesting_engine.data_loader import YahooFinanceLoader

# What is unit testing?

# Unit testing involves for individual units of code (e.g., functions or methods) to ensure they work as expected. The `unitest` module in Python is a built-in framework
# for writing and running tests.

# Components of a Unit Test

# 1. Test Framework: `unitest` is the framework we're using to write and run our tests
# 2. Test Case: A class that inherits from `unitest.TestCase`. This class contains one or more test methods
# 3. Test Method: A method within the test case class that tests a specific aspect of the code
# 4. Assertions: Statements that check if certain conditions are true. If an assertion fails, the test fails

# The test class `TestYahooFinanceLoader` is inheriting from `unitest.TestCase` - the base class provided by the `unitest` module.

class TestYahooFinanceLoader(unittest.TestCase):
    def setUp(self):
        self.loader = YahooFinanceLoader()
        self.symbol = "AAPL"
        self.start_date = "2021-01-01"
        self.end_date = "2021-12-31"

    def test_load_data(self):
        data = self.loader.load_data(self.symbol, self.start_date, self.end_date)
        self.assertIsInstance(data, pd.DataFrame, "Loaded data should be a DataFrame")
        self.assertFalse(data.empty, "Loaded data should not be empty") # TODO: # some instances where data should be none however, for example if the function
        # is called during a weekend, public holiday, etc. - so maybe this test case could be made more robust - by checking if it empty only when it shouldn't be
        self.assertIn('Date', data.columns, "DataFrame should have a 'Date' column")
        self.assertIn('Close', data.columns, "DataFrame should have a 'Close' column")

    # add other tests below like the following:

    def test_load_data_invalid_symbol(self):
        invalid_symbol = "INVALID"
        data = self.loader.load_data(invalid_symbol, self.start_date, self.end_date)
        self.assertIsInstance(data, pd.DataFrame, "Loaded data should be a DataFrame")
        self.assertTrue(data.empty, "Loaded data for an invalid symbol should be empty")

    # def test_load_data_date_range(self):
    #     # Check if the date range is respected
    #     data = self.loader.load_data(self.symbol, self.start_date, self.end_date)
    #     self.assertGreaterEqual(data['Date'].min(), pd.to_datetime(self.start_date), "Data start date should be greater than or equal to start_date")
    #     self.assertLessEqual(data['Date'].max(), pd.to_datetime(self.end_date), "Data end date should be less than or equal to end_date")

        # this test does not function properly


if __name__ == "__main__":
    unittest.main()