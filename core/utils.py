import os
import pandas as pd
import numpy as np

from sklearn.preprocessing import FunctionTransformer

def zero_to_one(x):
    return np.exp(x)/(1+np.exp(x))

def to_infinity(x):
    np.log(x/(1-x))

def get_dfs(dir):
  files = os.listdir(dir)
  symbols = [f[:-4] for f in files if f[-4:] == ".csv"]
  dfs = {f[:-4]: pd.read_csv(dir + "/" + f, index_col="time") for f in files if f[-4:]==".csv"}
  return dfs

def get_good_dfs(df_dict, n):
  good_dfs = {}
  for k, v in df_dict.items():
    if v.shape[0] > n:
        good_dfs[k] = v
  return good_dfs

def get_close_prices(good_dfs):
  for k, v in good_dfs.items():
    good_dfs[k].index = pd.to_datetime(good_dfs[k].index, unit="ms", utc=True)

  closes_ls = [good_dfs[k]['close'] for k, v in good_dfs.items()]
  closes_df = pd.concat(closes_ls, axis=1).dropna()
  closes_df.columns = list(good_dfs.keys())
  return closes_df

def calc_log_prices(closes):
  log_prices = FunctionTransformer(func = np.log).fit_transform(closes)
  log_df = pd.DataFrame(log_prices)
  log_df.index = closes.index
  log_df.columns = closes.columns
  return log_df

def fix_gaps_in_data(closes):
  closes_df = closes.resample('15T').max()
  closes_df.fillna(method="ffill", inplace=True)
  return closes_df

def get_pairs(good_dfs):
  dfs_keys = good_dfs.keys()
  usd_pairs = list(filter(lambda x:  x[-4:] == 'USDT', list(dfs_keys)))
  btc_pairs = list(filter(lambda x:  x[-3:] == 'BTC', list(dfs_keys)))
  eth_pairs = list(filter(lambda x:  x[-3:] == 'ETH', list(dfs_keys)))
  bnb_pairs = list(filter(lambda x:  x[-3:] == 'BNB', list(dfs_keys)))
  pairs = {'USD': usd_pairs, 'BTC': btc_pairs, 'ETH': eth_pairs, 'BNB': bnb_pairs}
  return pairs

def calc_returns(closes):
  log_prices = FunctionTransformer(func = np.log).fit_transform(closes)
  returns = pd.DataFrame(log_prices).diff()
  returns.columns = closes.columns
  returns = returns.drop(returns.index[0])
  return returns


def rename_columns(df, tag):
    new_column_names = [col + '_' + tag for col in df.columns]
    df.columns = new_column_names
    return df

def rename_columns(df, tag):
    new_column_names = [col + '_' + tag for col in df.columns]
    df.columns = new_column_names
    return df

def calculate_lags(features, target, m):
  target_lags = {}
  for i in range(0, m):
      code = 'y' + str(i)
      lag = target.shift(-i)
      target_lags[code] = lag

  y = pd.DataFrame(target_lags)

  features_df = pd.concat(features, axis=1).dropna()
  feature_lags = []
  for i in range(0, m):
      lag_df = features_df.shift(i)
      lag_df.columns = [c + '_lag' + str(i) for c in list(features_df.columns)]
      feature_lags.append(lag_df)

  all_lags = pd.concat(feature_lags, axis=1)
  full_df = pd.concat([all_lags, y], axis=1).dropna()
  full_df = full_df.replace([np.inf, -np.inf], 0)
  return full_df
