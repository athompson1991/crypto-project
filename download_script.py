from binance.client import Client
import pandas as pd
import json

def configure():
    with open('config.json') as f:
        config = json.load(f)
    return config

def get_ohlc(client, symbol):
    history = client.get_historical_klines(
        symbol,
        Client.KLINE_INTERVAL_15MINUTE,
        "1 Jan, 2018",
        "1 June, 2019"
    )
    times = [t[0] for t in history]
    open = [t[1] for t in history]
    high = [t[2] for t in history]
    low = [t[3] for t in history]
    close = [t[4] for t in history]
    volume = [t[5] for t in history]

    df = pd.DataFrame({
        'time': times,
        'open': open,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })
    return df

if __name__ == "__main__":
    print("Configuring")
    config = configure()
    client = Client(
        config['public_key'],
        config['private_key']
    )
    exchange_info = client.get_exchange_info()
    symbols = exchange_info["symbols"]
    print("Getting symbols")
    get_symbols = config["symbols"]
    get_pairs = []
    for i in get_symbols:
        for j in get_symbols:
            if i != j:
                get_pairs.append(i + j)
    for symbol in symbols:
        pair = symbol['baseAsset'] + symbol['quoteAsset']
        if pair in get_pairs:
            print(pair)
            ohlc = get_ohlc(client, pair)
            filename = 'data/' + pair + '.csv'
            ohlc.to_csv(filename)


