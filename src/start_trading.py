from market_data_tracker import MarketDataTracker

class StartTrading():
    
    def __init__(self, coin):
        self.market_data_tracker = MarketDataTracker(coin)
    
    def my_stratagy(self, marker_data):
        print(marker_data)
        
    def trade(self):
        self.market_data_tracker.start_data_collection(self.my_stratagy)