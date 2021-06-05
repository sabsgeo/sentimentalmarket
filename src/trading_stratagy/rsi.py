
class RSIStratagy():
    
    
    
    def update_latest_rsi(self, unit_time):
        for each_rsi in all_configs.TECHNICAL_INDICATOR_CONF.get("RSI").get('period'):
            if len(self.closes[unit_time]) > each_rsi:
                np_closes = numpy.array(self.closes[unit_time])
                rsi = talib.RSI(np_closes, each_rsi)
                self.latest_rsi[unit_time][each_rsi] = round(rsi[-1],2)

    def update_latest_macd(self, unit_time):
        FAST_P = all_configs.TECHNICAL_INDICATOR_CONF.get(
            "MACD").get("MACD_FAST")
        SLOW_P = all_configs.TECHNICAL_INDICATOR_CONF.get(
            "MACD").get("MACD_SLOW")
        MACD_SIG = all_configs.TECHNICAL_INDICATOR_CONF.get(
            "MACD").get("MACD_SIGNAL")
        if (len(self.closes[unit_time]) > all_configs.TECHNICAL_INDICATOR_CONF.get("MACD").get("MACD_SLOW")):
            np_closes = numpy.array(self.closes[unit_time])
            analysis = talib.MACD(
                np_closes, fastperiod=FAST_P, slowperiod=SLOW_P, signalperiod=MACD_SIG)
            self.latest_macd[unit_time] = {
                'mac': round(analysis[0][-1], 2), 'signal': round(analysis[1][-1], 2), 'histogram': round(analysis[2][-1], 2)}
    
    def update_latest_vwap(self, unit_time):
        if (len(self.closes) > 0 and len(self.volumes) > 0 and len(self.highs) > 0 and len(self.lows) > 0 and all_constants.TIME_WINDOW_IN_MSEC[unit_time] < all_constants.TIME_WINDOW_IN_MSEC["1d"] / 2):
            today = datetime.utcnow().date()
            start = datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
            start_in_ms = start.timestamp() * 1000
            now_in_ms = time.time() * 1000
            time_index = int(now_in_ms - start_in_ms)/ all_constants.TIME_WINDOW_IN_MSEC[unit_time]
            index = math.floor(time_index) + 1
            if self.open_times[unit_time][index * -1] == int(start_in_ms):
                pass
            elif self.open_times[unit_time][(index + 1) * -1 ] == int(start_in_ms):
                index = index + 1
            elif self.open_times[unit_time][(index - 1) * -1 ] == int(start_in_ms):
                index = index - 1
            else:
                self.reset_data  = True
                logger.error("Not able to find the right index")
                
            trading_day_open_times = self.open_times[unit_time][index * -1:]
            
            if (trading_day_open_times[0] == int(start_in_ms)):
                trading_day_closes = pd.Series(self.closes[unit_time][index * -1:])
                trading_day_highs = pd.Series(self.highs[unit_time][index * -1:])
                trading_day_lows = pd.Series(self.lows[unit_time][index * -1:])
                trading_day_volumes = pd.Series(self.volumes[unit_time][index * -1:])
                vwap = (((trading_day_lows + trading_day_highs + trading_day_closes) / 3) * trading_day_volumes).cumsum() / trading_day_volumes.cumsum()
                # Here is from where I took the code
                # https://gist.github.com/jxm262/449aed7f3ce0919e57a1f0ad8c18a9d9
                self.latest_vwap[unit_time] = {"price": round(vwap.tolist()[-1], 2)}
            else:
                self.reset_data  = True
                logger.error(f"There is a issue in getting todays trading data to calculate vwap for interval {unit_time}")
