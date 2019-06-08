from core.rolling_analysis import RollingAnalyzer
from core.utils import get_dfs, get_good_dfs, get_close_prices, fix_gaps_in_data, calc_returns, \
calc_log_prices, get_pairs, rename_columns
from sklearn.preprocessing import FunctionTransformer

import warnings
import numpy
import pandas as pd
import os


if __name__ == "__main__":
  warnings.simplefilter(action='ignore', category=FutureWarning)

  full_pathname = "/Users/alex/ml_class/project"

  m = 100

  start_date = '2019-01-01'
  end_date = '2019-03-01'

  print("getting data")
  dfs = get_dfs(full_pathname + "/data")
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
  filtered_log_df = log_df[start_date:end_date]

  print("calculating returns")
  returns = calc_returns(closes_usdt)
  print("-------------------")

  print("Now rolling analysis")
  rolling_analyzer = RollingAnalyzer(filtered_log_df, 100)

  print("Make the dfs")
  rolling_analyzer.make_dfs()
  rolling_analyzer.make_pairs()

  print("Calculating stats")
  rolling_analyzer.calc_all_returns_stats()

  print("Running all the regressions")
  rolling_analyzer.run_all_regressions()
  rolling_analyzer.run_regressions('ETHUSDT', 'BTCUSDT')

  print("Calculating dickey fullers")
  rolling_analyzer.calc_dickey_fuller('ETHUSDT', 'BTCUSDT')

  print("Exporting")
  mean_returns_df = rename_columns(rolling_analyzer.export_returns_stats_df(stat='mean_return'), 'mean')
  volatility_df = rename_columns(rolling_analyzer.export_returns_stats_df(stat='volatility'), 'vol')
  dickey_fuller_df = rename_columns(rolling_analyzer.export_dickey_fuller_df(), 'pval')
  betas_df = rename_columns(rolling_analyzer.export_betas_df(), 'betas')

  if not os.path.exists("../../features"):
    os.mkdir("../../features")

  mean_returns_df.to_csv(full_pathname + "/features/mean_returns.csv")
  volatility_df.to_csv(full_pathname + "/features/volatility.csv")
  dickey_fuller_df.to_csv(full_pathname + "/features/dickey_fuller.csv")
  betas_df.to_csv(full_pathname + "/features/betas.csv")


