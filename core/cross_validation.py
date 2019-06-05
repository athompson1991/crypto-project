def make_train_test(df, ratio = 0.2, target='BTCUSDT_ETHUSDT'):
    split_point = int((1 - ratio) * df.shape[0])
    y = df[target]
    x = df.drop([target], axis=1)
    y_train = y[0:split_point]
    x_train = x[0:split_point]
    y_test = y[(split_point + 1):]
    x_test = x[(split_point + 1):]
    out = {'train': {'x': x_train, 'y': y_train},
           'test': {'x': x_test, 'y': y_test}
          }
    return out

def time_series_kfolds(df, folds=3):
    subset_row_n = int(df.shape[0] / folds)
    out = []
    for i in range (0, folds):
        subset = df[i * subset_row_n:(i+1) * subset_row_n]
        out.append(subset)
    return out