
import sys
import os

from sentimentalmarket import MarketDataTracker
from rsi_and_engulfing_candles import RsiEngulfingCandles

if __name__ == "__main__":
    config_path = os.path.abspath("trading_configs.json")
    market_data = MarketDataTracker(config_path)
    market_data.start_trading(RsiEngulfingCandles)
