# Crypto Project

This is the final project for CFRM 521, Machine Learning for Finance.

## Install and download data

Three lines of code to get source:

```
git clone https://github.com/athompson1991/crypto-project.git
cd crypto-project
pip install -r requirements.txt
```

You need to drop a config.json file into the top level directory, make it look like this:

```json
{
  "public_key": "your_key",
  "private_key": "your_other_key",
  "debug": {
  	"symbols": ["USDT", "BTC", "ETH", "LTC"],
	"start": "2019-01-01",
	"end": "2019-01-03",
	"granularity": "15m"
  },
  "prod": {
	"symbols": ["USDT", "BTC", "ETH", "LTC", "DASH", "BNB", "TRX", "ZEC", "XRP", "EOS", "XMR", "ADA"],
	"start": "2018-01-01",
	"end": "2019-06-01",
	"granularity": "5m"
  }
}
```

Once that's all in place, you can run the script like so:

```
python download_script.py
```
