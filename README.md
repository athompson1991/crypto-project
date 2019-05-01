# Crypto Project

This is the final project for CFRM 521, Machine Learning for Finance.

## Install and download data

From the shell, make a python venv:

```
python -m venv crypto-venv
source crypto-venv/bin/activate
```

Three lines of code to get source and install modules:

```
git clone https://github.com/athompson1991/crypto-project.git
cd crypto-project
pip install -r requirements.txt
```

Everything is configured using a file named config.json and I have included an example. 
Simply replace the API keys with your own information and rename the file from 
example_config.json to config.json and it should be good to go.

Once that's all in place, you can run the script like so:

```
python download_script.py
```
