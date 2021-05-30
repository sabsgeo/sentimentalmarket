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
    def ONE_MIN_STRING():
        return "1m"

all_constants = _Const()
