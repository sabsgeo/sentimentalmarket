from abc import ABC, abstractmethod
from sentimentalmarket.trading_data import TradingData
from sentimentalmarket.notification import notify

class IStrategy(ABC):
    
    @abstractmethod
    def when_to_buy(self, trading_data: TradingData, user_config) -> [bool, str]:
        pass
    
    @abstractmethod
    def when_to_sell(self, trading_data: TradingData, user_config) -> [bool, str]:
        pass
    
    def decide_and_notify(self, trading_data: TradingData, user_config):        
        sell, sell_message = self.when_to_sell(trading_data, user_config)
        buy, buy_message = self.when_to_buy(trading_data, user_config)
        if (sell and buy):
            pass
        elif(buy):
            notify(user_config, buy_message)
        elif(sell):
            notify(user_config, sell_message)
