import os
import pandas as pd
import numpy as np

from sklearn.preprocessing import FunctionTransformer

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

