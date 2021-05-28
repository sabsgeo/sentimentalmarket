import decorators


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
            "TIME_WINDOW": ["1m", "15m", "1h", "4h"],
            "SUPPORTED_COINS": ['eth', 'xrp', 'matic', '1inch', 'bnb', 'ada']
        }


all_configs = _Configs()


# API_KEY = ""
# API_SECRET = ""
# TECHNICAL_INDICATOR_CONF = {
#     "RSI": {
#         "period": [6, 12, 24],
#         "OVER_SOLD": 70,
#         "UNDER_SOLD": 30
#     },
#     "TIME_WINDOW": ["1m", "15m", "1h", "4h"],
#     "SUPPORTED_COINS": ['eth', 'xrp', 'matic', '1inch', 'bnb', 'ada']
# }
