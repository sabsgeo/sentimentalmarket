from market_data_tracker import MarketDataTracker
from trading_data import TradingData
import pandas as pd
from config import all_configs
import talib

class StartTrading():
    
    def __init__(self, coin):
        self.market_data_tracker = MarketDataTracker(coin)
    
    def stratagy_integration(self, marker_data: TradingData):
        # print(marker_data.all_data["5m"])
        FAST_P = all_configs.TECHNICAL_INDICATOR_CONF.get(
            "MACD").get("MACD_FAST")
        SLOW_P = all_configs.TECHNICAL_INDICATOR_CONF.get(
            "MACD").get("MACD_SLOW")
        MACD_SIG = all_configs.TECHNICAL_INDICATOR_CONF.get(
            "MACD").get("MACD_SIGNAL")
        
        # np_closes = numpy.array(self.closes[unit_time])
        analysis = talib.MACD(marker_data.all_data["5m"]["close_price"].values, fastperiod=FAST_P, slowperiod=SLOW_P, signalperiod=MACD_SIG)
        print(analysis)
        # print(marker_data.all_data["5m"])
        
        
    def trade(self):
        self.market_data_tracker.start_data_collection(self.stratagy_integration)