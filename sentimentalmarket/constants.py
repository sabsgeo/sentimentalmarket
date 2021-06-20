from box import Box

__constants = {
    "SUPPORTED_TIME_WINDOW": ["1m", "5m", "15m", "1h", "4h", "1d"],
    "SUPPORTED_COINS": ['eth', 'xrp', 'matic', '1inch', 'bnb', 'ada'],
    "TIME_WINDOW_IN_MSEC": {"1m": 60000, "5m": 300000, "15m": 900000, "1h": 3600000, "4h": 14400000, "1d": 86400000}
}

all_constants = Box(__constants, frozen_box=True)
