import decorators
from config import all_configs


class _Const(object):

    @decorators.constant
    def EMPTY_UNIT_ARRAY():
        _ = {}
        for unit_time in all_configs.TECHNICAL_INDICATOR_CONF.get("TIME_WINDOW"):
            _[unit_time] = []
        return dict(_)

    @decorators.constant
    def EMPTY_UNIT_DICT():
        _ = {}
        for unit_time in all_configs.TECHNICAL_INDICATOR_CONF.get("TIME_WINDOW"):
            _[unit_time] = {}
        return dict(_)

    @decorators.constant
    def TIME_WINDOW_IN_MSEC():
        return {"1m": 60000, "5m": 300000, "15m": 900000, "1h": 3600000, "4h": 14400000, "1d": 86400000}


all_constants = _Const()
