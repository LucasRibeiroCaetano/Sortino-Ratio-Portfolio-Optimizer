# main.py

import config
import data
import otimizer
import plots
import pandas as pd
import sys 
from datetime import date 

def print_help_and_exit(error_message=None, exit_code=0):
    """Prints usage instructions for CLI arguments and exits."""
    if error_message:
        print(f"Error: {error_message}\n")
    
    print("Usage: python main.py [-t <TICKER1> ...] [-s <YYYY-MM-DD>] [-e <YYYY-MM-DD>] [-h | --help]")
    print("\nOptions:")
    print("  -t  Space-separated list of tickers (e.g., AAPL MSFT). Overrides config.TICKERS.")
    print("  -s  Start date for data download (Format: YYYY-MM-DD). Overrides config.START_DATE.")
    print("  -e  End date for data download (Format: YYYY-MM-DD). Overrides config.END_DATE.")
    print("  -h, --help Show this help message and exit.")
    sys.exit(exit_code)

def parse_cli_args():
    """Parses command-line arguments for tickers, start_date, and end_date, validating input flags."""
    
    # Set initial values from config.py
    ticker_list = config.TICKERS
    start_date = config.START_DATE
    end_date = config.END_DATE
    
    # Check for help flag aliases (exit_code=0)
    if '-h' in sys.argv or '--help' in sys.argv:
        print_help_and_exit()
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg == '-t':
            # Tickers must follow the flag
            i += 1
            command_line_tickers = []
            while i < len(args) and not args[i].startswith('-'):
                command_line_tickers.append(args[i])
                i += 1
                
            if command_line_tickers:
                ticker_list = command_line_tickers
            else:
                # Error: -t provided but no values followed (e.g., python main.py -t -s 2020-01-01)
                print_help_and_exit("-t flag used, but no tickers were specified after it.", exit_code=1)
            continue
            
        elif arg == '-s':
            try:
                new_start_date = args[i + 1]
                # Simple format check (YYYY-MM-DD)
                if len(new_start_date) == 10 and new_start_date[4] == '-' and new_start_date[7] == '-':
                    start_date = new_start_date
                else:
                    print_help_and_exit(f"Invalid format for start date '{new_start_date}'. Must be YYYY-MM-DD.", exit_code=1)
                i += 2
            except IndexError:
                # Error: -s provided but no value followed
                print_help_and_exit("'-s' flag used, but no date specified.", exit_code=1)
            continue
            
        elif arg == '-e':
            try:
                new_end_date = args[i + 1]
                if len(new_end_date) == 10 and new_end_date[4] == '-' and new_end_date[7] == '-':
                    end_date = new_end_date
                else:
                    print_help_and_exit(f"Invalid format for end date '{new_end_date}'. Must be YYYY-MM-DD.", exit_code=1)
                i += 2
            except IndexError:
                # Error: -e provided but no value followed
                print_help_and_exit("'-e' flag used, but no date specified.", exit_code=1)
            continue
            
        elif arg.startswith('-'):
            # Catch all unrecognized flags (e.g., --ticker, -x)
            print_help_and_exit(f"Unrecognized command line option '{arg}'.", exit_code=1)
            
        else:
            # Catch bare values (e.g., python main.py AAPL)
            print_help_and_exit(f"Unrecognized argument '{arg}'. Value must follow a valid flag (-t, -s, -e).", exit_code=1)
            
    # Log the final configuration before starting
    print("-" * 40)
    print(f"Final Configuration:")
    print(f"  Tickers: {ticker_list}")
    print(f"  Start Date: {start_date}")
    print(f"  End Date: {end_date}")
    print("-" * 40)
    
    return ticker_list, start_date, end_date

def main():
    
    # Parse CLI arguments and get final configuration
    ticker_list, start_date, end_date = parse_cli_args()

    # Log the effective configuration (based on default or override)
    # This section was previously in the parsing function, moving it here.
    if ticker_list == config.TICKERS:
        print(f"Using default tickers from config: {ticker_list}")
    else:
        print(f"Using command line tickers: {ticker_list}")

    print("Initializing Sortino Ratio Portfolio Optimizer...")
    
    # 1. Load Data
    data_raw = data.get_data(ticker_list, start_date, end_date)
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
        start_date, 
        end_date
    )
    
    print("--- Optimization Completed ---")

if __name__ == "__main__":
    main()