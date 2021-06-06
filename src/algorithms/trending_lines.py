import numpy as np

def __is_support(df,i):
  support = df['low_price'][i] < df['low_price'][i-1]  and df['low_price'][i] < df['low_price'][i+1] \
  and df['low_price'][i+1] < df['low_price'][i+2] and df['low_price'][i-1] < df['low_price'][i-2]

  return support

def __is_resistance(df,i):
  resistance = df['high_price'][i] > df['high_price'][i-1]  and df['high_price'][i] > df['high_price'][i+1] \
  and df['high_price'][i+1] > df['high_price'][i+2] and df['high_price'][i-1] > df['high_price'][i-2] 

  return resistance

def __is_far_from_level(l, levels):
  return np.sum([abs(l-x) < x  for x in levels]) == 0

def cal_support_and_resistance(df):
    """
    Base code from here
    https://github.com/gianlucamalato/machinelearning/blob/master/Support_and_resistance.ipynb
    """
    levels = []
    for index, row in df.iterrows():
        if __is_support(df,index):
            l = df['low_price'][index]

            if __is_far_from_level(l, levels):
                levels.append((row,l))

        elif __is_resistance(df,index):
            l = df['high_price'][index]

            if __is_far_from_level(l, levels):
                levels.append((row,l))
    return levels
    