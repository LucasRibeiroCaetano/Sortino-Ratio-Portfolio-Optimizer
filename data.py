# data.py

import yfinance as yf
import pandas as pd

def get_data(tickers, start_date, end_date):
    """
    Downloads adjusted close data from Yahoo Finance, 
    forcing auto_adjust=False to ensure the 'Adj Close' column is present 
    for accurate historical analysis.
    """
    print(f"Downloading data for {len(tickers)} assets...")
    
    price_data = []
    successful_tickers = []
    
    for ticker in tickers:
        try:
            # Crucial: auto_adjust=False to keep the Adj Close column
            data = yf.download(
                ticker, 
                start=start_date, 
                end=end_date, 
                auto_adjust=False, 
                progress=False     
            )['Adj Close']
            
            if not data.empty:
                data.name = ticker 
                price_data.append(data)
                successful_tickers.append(ticker)
            else:
                print(f"Warning: No data found for ticker {ticker}.")
        except Exception as e:
            # BTC-USD, por exemplo, pode falhar em períodos muito longos.
            print(f"Error downloading data for {ticker}: {e}")
            
    if not price_data:
        print("Error: No asset data was successfully downloaded.")
        return None
        
    final_data = pd.concat(price_data, axis=1)
    final_data.columns = successful_tickers
    
    # Drop rows with any missing price (NaN) across all assets
    final_data = final_data.dropna()

    print(f"Success: Clean data downloaded for {len(final_data)} trading days.")
    return final_data

def calculate_returns(data):
    """
    Calculates daily percentage returns from price data.
    """
    if data is None:
        return None
    daily_returns = data.pct_change().dropna()
    return daily_returns