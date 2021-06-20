def calc_vwap(self, session_close_price, session_high_price, session_low_price, session_volume):
    """
    Have to write the code for standard deviation too. 
    Code from https://gist.github.com/jxm262/449aed7f3ce0919e57a1f0ad8c18a9d9
    """
    vwap = (((session_low_price + session_high_price + session_close_price) / 3) * session_volume).cumsum() / session_volume.cumsum()
    return {"price": round(vwap.tolist()[-1], 2)}
