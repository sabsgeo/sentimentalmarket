
import sys

from sentimentalmarket import MarketDataTracker
from rsi_and_engulfing_candles import RsiEngulfingCandles

if __name__ == "__main__":
    market_data = MarketDataTracker("/src/trading_configs.json")
    market_data.start_trading(RsiEngulfingCandles)
