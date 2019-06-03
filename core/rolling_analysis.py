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
        self.assets = prices.columns
        self.n = prices.shape[0]
        self.m = m
        self.rolled_dfs = None
        self.rolled_returns = None
        self.rolled_regressions = {}
        self.rolled_returns_stats = {}
        self.pairs = []
    
    def make_dfs(self):
        roll_range = range(0, self.n - self.m)
        self.rolled_dfs = [pd.DataFrame(self.prices.iloc[i:(i+self.m), :]) for i in roll_range]
        self.rolled_returns = [pd.DataFrame(self.returns.iloc[i:(i+self.m), :]) for i in roll_range]
    
    def run_regressions(self, asset_1, asset_2):
        code = asset_1 + '_' + asset_2
        self.rolled_regressions[code] = []
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
            self.rolled_regressions[code].append(reg_dict)
        
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
        if code not in self.rolled_regressions.keys():
            print('Assets not regressed yet')
        else:
            for regression in self.rolled_regressions[code]:
                regression['dickey_fuller'] = ts.adfuller(regression['residuals'])
                
    def calc_all_dickey_fullers(self):
        if not self.pairs:
            print("Must make pairs")
        else:
            for pair in self.pairs:
                print(pair)
                self.calc_dickey_fuller(pair[0], pair[1])

    def calc_returns_stats(self, asset):
        self.rolled_returns_stats[asset] = []
        for df in self.rolled_returns:
            date_range = df.index[0], df.index[df.shape[0]-1]
            returns = df[asset]
            
            mean_return = np.mean(returns)
            sd_return = np.std(returns)
            sharpe = mean_return / sd_return

            stats_dict = {
                'date_range': date_range,
                'mean_return': mean_return,
                'volatility': sd_return,
                'sharpe': sharpe
            }

            self.rolled_returns_stats[asset].append(stats_dict)

    def calc_all_returns_stats(self):
        for asset in self.assets:
            self.calc_returns_stats(asset)
                
    def export_dickey_fuller_df(self):
        dickey_fullers = {}

        for key in self.rolled_regressions.keys():
            regressions = self.rolled_regressions[key]
            if 'dickey_fuller' in regressions[0].keys():
                dickey_fuller = [t['dickey_fuller'][1] for t in regressions]
                date_range = [i['date_range'][0] for i in regressions]
                dickey_fullers[key] = pd.Series(dickey_fuller, index=date_range)

        out_df = pd.DataFrame.from_dict(dickey_fullers)
        return out_df

    def export_betas_df(self):
        betas = {}
        for key in self.rolled_regressions.keys():
            regressions = self.rolled_regressions[key]
            betas_temp = np.array([r['regression'].coef_[0] for r in regressions])
            date_range = [i['date_range'][0] for i in regressions]
            betas[key] = pd.Series(betas_temp, index = date_range)
        out_df = pd.DataFrame.from_dict(betas)
        return out_df

    def export_returns_stats_df(self, stat='mean_return'):
        mean_returns = {}
        for key in self.rolled_returns_stats.keys():
            stats = self.rolled_returns_stats[key]
            mean_return_dict = {i['date_range'][0]: i[stat] for i in stats}
            mean_returns[key] = pd.Series(mean_return_dict)
        out_df = pd.DataFrame.from_dict(mean_returns)
        return out_df

        


