import pandas as pd
import warnings
from core.utils import calculate_lags
from core.cross_validation import make_train_test
from core.dimension_reduction import do_pca_reduce

if __name__ == "__main__":
  project_dir = '/Users/alex/ml_class/project/'
  warnings.simplefilter(action='ignore', category=FutureWarning)

  print("Reading data frames")
  dickey_fuller_df = pd.DataFrame.from_csv(project_dir + '/features/dickey_fuller.csv')
  mean_returns_df = pd.DataFrame.from_csv(project_dir + '/features/mean_returns.csv')
  volatility_df = pd.DataFrame.from_csv(project_dir + '/features/volatility.csv')
  betas_df =pd.DataFrame.from_csv(project_dir + '/features/betas.csv')

  features = [dickey_fuller_df, mean_returns_df, volatility_df, betas_df]

  print("Making lags")
  lagged_data = calculate_lags(features, dickey_fuller_df, 100)
  train_test = make_train_test(lagged_data['full_df'], target=lagged_data['target'].keys())

  print("PCA")
  pca_reduction = do_pca_reduce(train_test)
  

