from binance.client import Client
import pandas as pd
import json

def configure():
    with open('config.json') as f:
        config = json.load(f)
    return config

def get_ohlc(client, **kwargs):
    history = client.get_historical_klines(
        kwargs['symbol'],
        kwargs['granularity'],
        kwargs['start'],
        kwargs['end']
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

def make_trading_pairs(tickers):
    get_pairs = []
    for i in tickers:
        for j in tickers:
            if i != j:
                get_pairs.append(i + j)
    return get_pairs
 

if __name__ == "__main__":
    print("Configuring")
    is_debug = True
    config = configure()
    client = Client(
        config['public_key'],
        config['private_key']
    )
    if is_debug:
        sub_config = config['debug']
    else:
        sub_config = config['prod']
    exchange_info = client.get_exchange_info()
    exchange_symbols = exchange_info["symbols"]
    print("Getting symbols")
    get_symbols = sub_config["symbols"]
    get_pairs = make_trading_pairs(get_symbols)
    for symbol in exchange_symbols:
        pair = symbol['baseAsset'] + symbol['quoteAsset']
        if pair in get_pairs:
            print(pair)
            ohlc = get_ohlc(
                client,
                symbol=pair,
                start=sub_config['start'],
                end=sub_config['end'],
                granularity=sub_config['granularity']
            )
            filename = 'data/' + pair + '.csv'
            ohlc.to_csv(filename)

