# config.py

# --- DEFAULTS DO UTILIZADOR ---

DEFAULT_TICKERS = [
    'SPY', 'QQQ', 'IWM', 'EFA', 'EEM', 'TLT',
    'BTC-USD', 'GLD', 'DBC', 'XLE'
]
DEFAULT_START_DATE = '2000-01-01'
DEFAULT_END_DATE = '2024-12-31'

# --- CONFIGURAÇÕES DE EXECUÇÃO ---

# ATIVOS: Use os defaults. Para usar uma lista diferente, altere esta linha.
TICKERS = DEFAULT_TICKERS 

# Período de análise
START_DATE = DEFAULT_START_DATE
END_DATE = DEFAULT_END_DATE

# Taxa Livre de Risco (Risk-Free Rate, ex: 2% ao ano)
# Usada como 'target' de retorno mínimo no Sortino Ratio
RISK_FREE_RATE = 0.02

# Número de simulações Monte Carlo (25.000 é rápido e preciso)
NUM_PORTFOLIOS = 25000