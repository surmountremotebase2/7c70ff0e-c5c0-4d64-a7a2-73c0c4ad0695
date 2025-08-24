from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from surmount.technical_indicators import SMA

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"  # Specify the ticker to trade
        self.short_window = 5  # Short term moving window
        self.long_window = 20  # Long term moving window

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"
    
    def run(self, data):
        # Extract closing prices for the specified ticker
        closing_prices = [entry[self.ticker]["close"] for entry in data["ohlcv"]]
        
        # Calculate short and long term moving averages
        short_sma = SMA(self.ticker, data["ohlcv"], self.short_window)
        long_sma = SMA(self.ticker, data["ohlcv"], self.long_window)
        
        # Ensure we have enough data points to make a decision
        if len(closing_prices) >= self.long_window:
            # Determine the trading signal
            if short_sma[-1] > long_sma[-1]:
                allocation = {self.ticker: 1.0}  # Buy signal
            else:
                allocation = {self.ticker: 0.0}  # Sell signal or avoid buying
        else:
            allocation = {}  # Not enough data, no action
            
        # Return the target allocation
        return TargetAllocation(allocation)