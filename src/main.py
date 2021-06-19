
import sys

from sentimentalmarket import MarketDataTracker
from arg_parser import parse_args
from rsi_and_engulfing_candles import RsiEngulfingCandles

coin, bot_key, channel_id = parse_args(sys.argv)

if __name__ == "__main__":
    market_data = MarketDataTracker(coin)
    market_data.start_trading(RsiEngulfingCandles, "/src/trading_configs.json")
