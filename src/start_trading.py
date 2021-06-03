from market_data_tracker import MarketDataTracker

class StartTrading():
    
    def __init__(self, coin):
        self.market_data_tracker = MarketDataTracker(coin)
    
    def my_stratagy(self, marker_data):
        print(marker_data)
        
    def trade(self):
        self.market_data_tracker.start_data_collection(self.my_stratagy)
        # This to make sure to try till success
        # while True:
        #     self.market_data_tracker.start_data_collection()
        #     # This to update check the status at regular intervals
        #     while self.market_data_tracker.start_trading:
        #         time.sleep(.5)
        #         threading.Thread(target=self.snd_inst.send).start()
        #     # adding this delay to give time for all the websocke to get closed before restart
        #     time.sleep(5)