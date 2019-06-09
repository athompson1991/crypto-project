from sklearn.decomposition import PCA
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def rebuild_df(pca_df, pipeline):
    rebuilt_df = pd.DataFrame(pipeline.inverse_transform(pca_df))
    rebuilt_df.index = pca_df.index
    rebuilt_df.columns = ['y' + str(i) for i in range(rebuilt_df.shape[1])]
    return rebuilt_df

def do_pca_reduce(dataset):
  pca_pipeline = Pipeline([
      ('scale', StandardScaler()),
      ('pca', PCA(n_components=0.9))
  ])

  x_train_pca_reduced = pd.DataFrame(pca_pipeline.fit_transform(dataset['train']['x']))
  y_train_pca_reduced = pd.DataFrame(pca_pipeline.fit_transform(dataset['train']['y']))
  x_test_pca_reduced = pd.DataFrame(pca_pipeline.fit_transform(dataset['test']['x']))
  y_test_pca_reduced = pd.DataFrame(pca_pipeline.fit_transform(dataset['test']['y']))
  
  x_train_pca_reduced.index = dataset['train']['x'].index
  y_train_pca_reduced.index = dataset['train']['y'].index
  x_test_pca_reduced.index = dataset['test']['x'].index
  y_test_pca_reduced.index = dataset['test']['y'].index

  out = {
    'pipeline': pca_pipeline,
    'original_data': dataset,
    'pca_data': {
      'train': {'x': x_train_pca_reduced, 'y': y_train_pca_reduced},
      'test': {'x': x_test_pca_reduced, 'x': x_test_pca_reduced}
    }
  }
  return out