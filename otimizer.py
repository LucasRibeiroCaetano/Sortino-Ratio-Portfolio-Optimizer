# otimizer.py

import numpy as np
import pandas as pd
from tqdm import tqdm

def run_monte_carlo(daily_returns, num_portfolios, risk_free_rate):
    """
    Executes the Monte Carlo simulation to find the portfolio
    with the maximum Sortino Ratio.
    """
    if daily_returns is None:
        return None

    tickers = daily_returns.columns
    num_tickers = len(tickers)
    
    # Annualized mean returns 
    mean_returns = daily_returns.mean() * 252
    
    results = []

    print("Running Monte Carlo simulation...")
    for i in tqdm(range(num_portfolios), desc="Simulating Portfolios"):
        
        # 1. Generate random weights
        weights = np.random.random(num_tickers)
        weights /= np.sum(weights) # Normalize weights
        
        # 2. Calculate Portfolio Annualized Return
        port_return = np.sum(mean_returns * weights)
        
        # 3. Calculate Portfolio Daily Returns (time series)
        port_daily_returns = (daily_returns * weights).sum(axis=1)
        
        # 4. Calculate Downside Deviation
        target_return = risk_free_rate / 252
        downside_returns = port_daily_returns[port_daily_returns < target_return]
        
        if len(downside_returns) == 0:
            downside_dev = 0
        else:
            downside_variance = (downside_returns - target_return).pow(2).sum() / len(port_daily_returns)
            downside_dev = np.sqrt(downside_variance) * np.sqrt(252)

        # 5. Calculate Sortino Ratio
        if downside_dev == 0:
            port_sortino = np.inf 
        else:
            port_sortino = (port_return - risk_free_rate) / downside_dev
            
        # 6. Calculate Total Volatility
        port_volatility = port_daily_returns.std() * np.sqrt(252)

        # Store results, including the weights array
        results.append([port_return, port_volatility, port_sortino, weights])
    
    # Convert results to DataFrame.
    results_df = pd.DataFrame(
        results,
        columns=['Retorno', 'Volatilidade', 'Sortino', 'Weights']
    )
    
    return results_df

def find_best_portfolio(results_df):
    """
    Finds the portfolio with the highest Sortino Ratio.
    """
    if results_df is None:
        return None
    
    max_sortino_port = results_df.iloc[results_df['Sortino'].idxmax()]
    
    return max_sortino_port