from sentimentalmarket import decorators


class _Configs(object):

    @decorators.constant
    def API_KEY():
        return ""

    @decorators.constant
    def API_SECRET():
        return ""
        
    @decorators.constant
    def TECHNICAL_INDICATOR_CONF():
        return {
            "RSI": {
                "period": [6, 12, 24],
                "OVER_SOLD": 70,
                "UNDER_SOLD": 30
            },
            "MACD": {
                "MACD_FAST": 12,
                "MACD_SLOW": 26,
                "MACD_SIGNAL": 9
            },
            "TIME_WINDOW": ["1m", "5m", "15m", "1h", "4h", "1d"],
            "SUPPORTED_COINS": ['eth', 'xrp', 'matic', '1inch', 'bnb', 'ada']
        }


all_configs = _Configs()
