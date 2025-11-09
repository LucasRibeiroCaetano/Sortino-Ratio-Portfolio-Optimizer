# main.py

import config
import data
import otimizer
import plots
import pandas as pd

def main():
    print("Initializing Sortino Ratio Portfolio Optimizer...")
    
    # 1. Load Data
    data_raw = data.get_data(config.TICKERS, config.START_DATE, config.END_DATE)
    if data_raw is None:
        print("Data loading failed. Exiting.")
        return
        
    daily_returns = data.calculate_returns(data_raw)
    
    # Get the list of successfully downloaded tickers
    successful_tickers = data_raw.columns.tolist() 

    # 2. Optimize Portfolio
    results_df = otimizer.run_monte_carlo(
        daily_returns,
        config.NUM_PORTFOLIOS,
        config.RISK_FREE_RATE
    )
    if results_df is None:
        print("Optimization failed. Exiting.")
        return
        
    best_portfolio = otimizer.find_best_portfolio(results_df)

    # 3. Display Results
    print("\n--- Optimal Portfolio Found (Maximum Sortino Ratio) ---")
    print(f"Annualized Return:       {(best_portfolio['Retorno'] * 100):.2f}%")
    print(f"Annualized Volatility:   {(best_portfolio['Volatilidade'] * 100):.2f}%")
    print(f"Sortino Ratio:           {best_portfolio['Sortino']:.2f}")
    
    print("\nOptimal Allocation (Weights):")

    allocation = pd.Series(best_portfolio['Weights'], index=successful_tickers) 
    print((allocation[allocation > 0.01] * 100).map(lambda x: f'{x:.2f}%'))

    # 4. Visualize Graphics in One Window
    print("\nGenerating unified plot window...")
    plots.plot_all_in_one(
        daily_returns, 
        results_df, 
        best_portfolio, 
        successful_tickers, # Use only tickers with data
        config.START_DATE, 
        config.END_DATE
    )
    
    print("--- Optimization Completed ---")

if __name__ == "__main__":
    main()