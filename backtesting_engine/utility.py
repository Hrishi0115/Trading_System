# general-purpose utility module which stores various helper functions

import yfinance as yf

def get_risk_free_rate():
    """
    Fetches the current yield for the 10-Year Treasury Note
    and returns it as a percentage.
    Used to determine risk-free rate.
    """
    treasury_data = yf.Ticker("^TNX")
    treasury_history = treasury_data.history(period="1d")  # Get the latest data

    current_yield = treasury_history['Close'].iloc[-1] / 100  # Convert to a percentage

    return current_yield