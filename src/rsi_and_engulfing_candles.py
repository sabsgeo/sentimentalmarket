from sentimentalmarket.strategy import IStrategy
from sentimentalmarket.trading_data import TradingData
import talib
    
class RsiEngulfingCandles(IStrategy):
    
    def when_to_buy(self, trading_data: TradingData, user_config):
        rsi_settings = user_config.rsi
        source = rsi_settings.source
        length = rsi_settings.length
        threshod = rsi_settings.over_sold
        
        one_hrs_df = trading_data.all_data["1h"]
        all_rsi = talib.RSI(one_hrs_df[source].to_numpy(), length)
        latest_rsi = round(all_rsi[-1], 2)
        buy = False
        if (latest_rsi < threshod):
            buy = True
    
        return [buy, f"Buy {trading_data.currency} its current value is {trading_data.current_price}"]
        
    def when_to_sell(self, trading_data: TradingData, user_config):
        rsi_settings = user_config.rsi
        source = rsi_settings.source
        length = rsi_settings.length
        threshod = rsi_settings.over_bought
        
        one_hrs_df = trading_data.all_data["1h"]
        all_rsi = talib.RSI(one_hrs_df[source].to_numpy(), length)
        latest_rsi = round(all_rsi[-1],2)
        print(latest_rsi)
        sell = False
        if (latest_rsi > threshod):
            sell = True
        
        return [sell, f"Sell {trading_data.currency} its current value is {trading_data.current_price}"]
        