import datetime
import json
import pandas as pd
import os
import numpy as np
from sklearn.pipeline import Pipeline
import numpy
from functools import reduce
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from sklearn.preprocessing import StandardScaler

import statsmodels.tsa.stattools as ts

import warnings

class RollingAnalyzer:
    
    def __init__(self, prices, m):
        self.prices = prices
        self.returns = pd.DataFrame(prices).diff()
        self.n = prices.shape[0]
        self.m = m
        self.rolled_dfs = None
        self.regressions = {}
        self.pairs = []
    
    def make_dfs(self):
        roll_range = range(0, self.n - self.m)
        self.rolled_dfs = [pd.DataFrame(self.prices.iloc[i:(i+self.m), :]) for i in roll_range]
    
    def run_regressions(self, asset_1, asset_2):
        code = asset_1 + '_' + asset_2
        self.regressions[code] = []
        for df in self.rolled_dfs:
            date_range = df.index[0], df.index[df.shape[0]-1]
            x = df[asset_1].values.reshape(-1, 1)
            y = df[asset_2].values
            linear_regression = LinearRegression().fit(x, y)
            residuals = y - linear_regression.predict(x)
            reg_dict = {
                'date_range': date_range,
                'regression': linear_regression,
                'residuals': residuals,
            }
            self.regressions[code].append(reg_dict)
        
    def asset_loop(self):
        for i in range(0, self.prices.shape[1]):
            pair_i = self.prices.columns[i]
            for j in range(0, i):
                pair_j = self.prices.columns[j]
                if pair_i != pair_j:
                    self.pairs.append((pair_i, pair_j))
    
    def run_all_regressions(self):
        if not self.pairs:
            print("Must make pairs")
        else:
            for pair in self.pairs:
                print(pair)
                self.run_regressions(pair[0], pair[1])
    
    def calc_dickey_fuller(self, asset_1, asset_2):
        code = asset_1 + '_' + asset_2
        if code not in self.regressions.keys():
            print('Assets not regressed yet')
        else:
            for regression in self.regressions[code]:
                regression['dickey_fuller'] = ts.adfuller(regression['residuals'])
                
    def calc_all_dickey_fullers(self):
        if not self.pairs:
            print("Must make pairs")
        else:
            for pair in self.pairs:
                print(pair)
                self.calc_dickey_fuller(pair[0], pair[1])
                
    def export_df(self):
        dickey_fullers = {}
        date_index = []
        for k, v in self.regressions.items():
            dickey_fullers[k] = v['dickey_fuller']
            date_index.append(v['date_range'][0])
        out_df = pd.from_dict(dickey_fuller)
        out_df.index = date_index
        return(out_df)
        