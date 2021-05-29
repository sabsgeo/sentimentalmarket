import decorators


class _Const(object):

    @decorators.constant
    def EMPTY_UNIT_ARRAY():
        return {
            "1m": [],
            "15m": [],
            "1h": [],
            "4h": []
        }

    @decorators.constant
    def EMPTY_UNIT_DICT():
        return {
            "1m": {},
            "15m": {},
            "1h": {},
            "4h": {}
        }
    
    @decorators.constant
    def ONE_MIN_STRING():
        return "1m"


all_constants = _Const()
