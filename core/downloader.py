from binance.client import Client
from datetime import datetime
import pandas as pd
import json
import os

def make_trading_pairs(tickers):
    get_pairs = []
    for i in tickers:
        for j in tickers:
            if i != j:
                get_pairs.append(i +  j)
    return get_pairs

class Downloader(object):

    def __init__(self, debug):
        self.debug = debug
        self.config = None
        self.env = None
        self.client = None
        self.data = {}

    def configure(self, config_file):
        with open(config_file) as f:
            self.config = json.load(f)
        if self.debug:
            self.env = self.config['debug']
        else:
            self.env = self.config['prod']

    def make_client(self):
        self.client = Client(
            self.config['public_key'],
            self.config['private_key']
        )

    def fetch(self):
        exchange_info = self.client.get_exchange_info()
        exchange_symbols = exchange_info["symbols"]
        get_symbols = self.env["symbols"]
        get_pairs = make_trading_pairs(get_symbols)
        for symbol in exchange_symbols:
            pair = symbol['baseAsset'] + symbol['quoteAsset']
            if pair in get_pairs:
                print(pair)
                ohlc = self._get_ohlc(pair)
                self.data[pair] = ohlc

    def _get_ohlc(self, symbol):
        history = self.client.get_historical_klines(
            symbol,
            self.env['granularity'],
            self.env['start'],
            self.env['end']
        )

        timestamps = [datetime.fromtimestamp(int(t[0])/1000) for t in history]
        timestamps = [t.replace(second=0, microsecond=0) for t in timestamps]

        df = pd.DataFrame({
            'open': [t[1] for t in history],
            'high': [t[2] for t in history],
            'low': [t[3] for t in history],
            'close': [t[4] for t in history],
            'volume': [t[5] for t in history],
            'dividend': [0.0 for t in history],
            'split': [1.0 for t in history],
            'time': [t[0] for t in history],
        })
        return df

    def to_csv(self, os_target, target_dir):
        cols = ['open', 'high', 'low', 'close', 'volume', 'dividend', 'split', 'time']
        os.chdir(os_target)
        dirs = os.listdir()
        if target_dir not in dirs:
            os.mkdir(target_dir)
        else:
            for f in os.listdir(target_dir):
                f_path = os.path.join(target_dir, f)
                try:
                    if os.path.isfile(f_path):
                        os.unlink(f_path)
                except Exception as e:
                       print(e) 
        for k, v in self.data.items():
            v = v.reindex(columns=cols)
            v.to_csv(target_dir + '/' + k + '.csv', index=False)

