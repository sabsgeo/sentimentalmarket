import numpy as np
import pandas as pd

def __is_support(df,i):
  support = df['low_price'][i] < df['low_price'][i-1]  and df['low_price'][i] < df['low_price'][i+1] \
  and df['low_price'][i+1] < df['low_price'][i+2] and df['low_price'][i-1] < df['low_price'][i-2]

  return support

def __is_resistance(df,i):
  resistance = df['high_price'][i] > df['high_price'][i-1]  and df['high_price'][i] > df['high_price'][i+1] \
  and df['high_price'][i+1] > df['high_price'][i+2] and df['high_price'][i-1] > df['high_price'][i-2] 

  return resistance

def __is_far_from_level(l, s,levels):
  return np.sum([abs(l-x[1]) < s  for x in levels]) == 0

def cal_support_and_resistance(df):
    """
    Base code from here
    https://github.com/gianlucamalato/machinelearning/blob/master/Support_and_resistance.ipynb
    """
    df.reset_index(drop = True, inplace=True)
    levels = []
    s =  np.mean(df['high_price'] - df['low_price'])
    for index, row in df.iterrows():
      if index >=2 and index <= len(df.index) - 3:
        if __is_support(df,index):
          l = df['low_price'][index]

          if __is_far_from_level(l, s, levels):
            levels.append((row,l))

        elif __is_resistance(df,index):
          l = df['high_price'][index]

          if __is_far_from_level(l, s, levels):
            levels.append((row,l))
    final_levels = pd.DataFrame()
    for _ in levels:
      __ = _[0]
      __['level'] = _[1]
      final_levels = final_levels.append(__, ignore_index = True)
    final_levels = final_levels.sort_values('level')
    final_levels.reset_index(drop = True, inplace=True)
    
    return final_levels
    