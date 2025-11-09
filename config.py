# config.py

# --- User Defaults ---

DEFAULT_TICKERS = [
    'SPY', 'QQQ', 'IWM', 'EFA', 'EEM', 'TLT',
    'BTC-USD', 'GLD', 'DBC', 'XLE'
]
DEFAULT_START_DATE = '2000-01-01'
DEFAULT_END_DATE = '2024-12-31'

TICKERS = DEFAULT_TICKERS 
START_DATE = DEFAULT_START_DATE
END_DATE = DEFAULT_END_DATE

# Minimum acceptable Sortino Ratio for portfolios to be considered
RISK_FREE_RATE = 0.02

# Number of portfolios to simulate during optimization
NUM_PORTFOLIOS = 25000