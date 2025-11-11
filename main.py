# main.py

import config
import data
import otimizer
import plots
import pandas as pd
import sys 

def main():
    # 1. DETERMINAR LISTA DE TICKERS (Prioridade à Linha de Comandos)
    
    # Inicia com a lista default definida em config.py
    ticker_list = config.TICKERS
    print(f"Using default tickers from config: {ticker_list}")

    if '-t' in sys.argv:
        # Encontra o índice da flag '-t'
        t_index = sys.argv.index('-t')
        
        # Tickers são todos os argumentos que vêm após a flag
        command_line_tickers = sys.argv[t_index + 1:]
        
        if command_line_tickers:
            # Sobrescreve a lista default com os tickers da linha de comandos
            ticker_list = command_line_tickers
            print(f"Overriding defaults. Using tickers from command line: {ticker_list}")
        else:
            print("Warning: '-t' flag was used, but no tickers were specified after it. Using default list.")
    
    # ... (O resto da função main() continua a usar 'ticker_list')

    print("Initializing Sortino Ratio Portfolio Optimizer...")
    
    # 1. Load Data
    data_raw = data.get_data(ticker_list, config.START_DATE, config.END_DATE)
    if data_raw is None:
        print("Data loading failed. Exiting.")
        return
        
    daily_returns = data.calculate_returns(data_raw)
    
    # Obter a lista real de tickers bem-sucedidos das colunas do DataFrame
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
        successful_tickers, 
        config.START_DATE, 
        config.END_DATE
    )
    
    print("--- Optimization Completed ---")

if __name__ == "__main__":
    main()