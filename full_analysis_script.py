from core.rolling_analysis import RollingAnalyzer
from core.utils import get_dfs, get_good_dfs, get_close_prices, fix_gaps_in_data, calc_returns, \
calc_log_prices, get_pairs
from sklearn.preprocessing import FunctionTransformer

import warnings
import numpy
import pandas as pd


if __name__ == "__main__":
  warnings.simplefilter(action='ignore', category=FutureWarning)

  print("getting data")
  dfs = get_dfs("data")
  print("filtering to good ones")
  good_dfs = get_good_dfs(dfs, 30000)
  print("getting close prices")
  closes = get_close_prices(good_dfs)
  print("filling gaps")
  closes = fix_gaps_in_data(closes)
  print("filtering to USDT")
  pairs = get_pairs(good_dfs)
  closes_usdt = closes[pairs['USD']]

  print("calculating log prices")
  log_df = calc_log_prices(closes_usdt)
  filtered_log_df = log_df['2019-01-01':'2019-02-01']

  print("calculating returns")
  returns = calc_returns(closes_usdt)
  print("-------------------")
  print("Now rolling analysis")
  rolling_analyzer = RollingAnalyzer(filtered_log_df, 100)
  print("Make the dfs")
  rolling_analyzer.make_dfs()
  rolling_analyzer.asset_loop()
  print("Running all the regressions")
  # rolling_analyzer.run_all_regressions()
  rolling_analyzer.run_regressions('BTCUSDT', 'ETHUSDT')
  rolling_analyzer.run_regressions('BTCUSDT', 'LTCUSDT')
  rolling_analyzer.calc_returns_stats('BTCUSDT')

  print("Calculating dickey fullers")
  # rolling_analyzer.calc_dickey_fuller('BTCUSDT', 'ETHUSDT')
  # rolling_analyzer.calc_dickey_fuller('BTCUSDT', 'LTCUSDT')

  print("Exporting")
  dickey_fuller_df = rolling_analyzer.export_dickey_fuller_df()
  print(dickey_fuller_df.head())
  betas_df = rolling_analyzer.export_betas_df()
  print(betas_df.head())

  # rolling_analyzer.calc_all_dickey_fullers()


