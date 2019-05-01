from binance.client import Client
import pandas as pd
import json
import os

def make_trading_pairs(tickers):
    get_pairs = []
    for i in tickers:
        for j in tickers:
            if i != j:
                get_pairs.append(i + j)
    return get_pairs

class Downloader(object):

    def __init__(self, debug):
        self.debug = debug
        self.config = None
        self.env = None
        self.client = None
        self.data = {}
 
    def configure(self):
        with open('config.json') as f:
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

        df = pd.DataFrame({
            'time': [t[0] for t in history],
            'open': [t[1] for t in history],
            'high': [t[2] for t in history],
            'low': [t[3] for t in history],
            'close': [t[4] for t in history],
            'volume': [t[5] for t in history]
        })
        return df

    def to_csv(self, target_dir):
        dirs = os.listdir()
        if target_dir not in dirs:
            os.mkdir(target_dir)
        for k in self.data.keys():
            self.data[k].to_csv(target_dir + '/' + k + '.csv')


