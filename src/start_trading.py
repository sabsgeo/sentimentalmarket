from market_data_tracker import MarketDataTracker
from trading_data import TradingData
import pandas as pd
class StartTrading():
    
    def __init__(self, coin):
        self.market_data_tracker = MarketDataTracker(coin)
    
    def stratagy_integration(self, marker_data: TradingData):
        print(marker_data)
        # print(marker_data.all_data["5m"])
        
        
    def trade(self):
        self.market_data_tracker.start_data_collection(self.stratagy_integration)