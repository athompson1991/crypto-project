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

def rolled_mse(true_values, predicted, transform = True):
    mse_list = []
    rebuilt = rebuild_df(predicted)
    for i in range(true_values.shape[0]):
        temp_true = true_values.iloc[i, :]
        temp_pred = rebuilt.iloc[i, :]
        if transform:
            temp_true = zero_to_one(temp_true)
            temp_pred = zero_to_one(temp_pred)
        temp_mse = mean_squared_error(temp_true, temp_pred)
        mse_list.append(temp_mse)
    return mse_list

def overall_rolled_mse(true_values, predicted, transform=True):
    mse_list = rolled_mse(true_values, predicted, transform)
    return np.mean(mse_list)

def time_series_cross_val_split(x, y, predict_n=100):
    n = x.shape[0]
    split = n - predict_n
    in_sample_x = x.iloc[:(split - 1), :]
    in_sample_y = y.iloc[:(split - 1)]
    out_of_sample_x = x.iloc[split:, :]
    out_of_sample_y = y.iloc[split:, :]
    out = {
        'in': {'x': in_sample_x, 'y': in_sample_y},
        'out': {'x': out_of_sample_x, 'y': out_of_sample_y}
    }
    return out
