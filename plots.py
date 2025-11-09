# plots.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotx as mpx

def setup_style():
    """
    Sets up the 'github-dark' style from matplotx, 
    with 'ggplot' as the fallback style, using the requested lookup structure.
    """
    try:
        plt.style.use(mpx.styles.github["dark"]) 
    except Exception:
        plt.style.use("ggplot") 
        print("Warning: 'github-dark' style not found. Using 'ggplot' fallback.")


def plot_all_in_one(daily_returns, results_df, best_portfolio, tickers, start_date, end_date):
    """
    Generates a single figure with three subplots using the custom layout:
    Line 1: Portfolio Performance (70% width) | Pie (30% Width)
    Line 2: Monte Carlo Simulation (100% width)
    """
    setup_style()
    
    weights = best_portfolio['Weights']
    
    # --- Data Preparation ---
    pie_weights = pd.Series(weights, index=tickers)
    pie_weights = pie_weights[pie_weights > 0.01]
    
    port_daily_returns = (daily_returns * weights).sum(axis=1)
    cumulative_returns = (1 + port_daily_returns).cumprod()
    cumulative_returns_pct = (cumulative_returns - 1) * 100
    
    # ----------------------------------------------------
    # 2. Setup the figure and the custom 2-row layout
    # ----------------------------------------------------
    
    # Increase figure height slightly for better vertical separation
    fig = plt.figure(figsize=(24, 16)) 
    fig.suptitle('Sortino Ratio Portfolio Optimization Analysis', fontsize=24, y=0.98)
    
    # Ax1: Portfolio Performance (Line 1, takes 2/3 of the width)
    ax1 = plt.subplot2grid((2, 3), (0, 0), colspan=2)
    
    # Ax2: Pie Chart (Line 1, takes 1/3 of the width)
    ax2 = plt.subplot2grid((2, 3), (0, 2))
    
    # Ax0: Monte Carlo Simulation (Line 2, takes all 3 columns)
    ax0 = plt.subplot2grid((2, 3), (1, 0), colspan=3)


    # --- Plot 1: Portfolio Performance (Line Plot) ---
    cumulative_returns_pct.plot(ax=ax1, label='Portfolio Performance', color='cyan')
    ax1.set_title(f'Cumulative Return ({start_date} to {end_date})')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Cumulative Return (%)')
    ax1.grid(True, linestyle='--', alpha=0.5)

    # --- Plot 2: Portfolio Composition (Pie Chart) ---
    ax2.pie(
        pie_weights, 
        labels=pie_weights.index, 
        autopct='%1.1f%%',
        startangle=90
    )
    ax2.set_title('Max Sortino Portfolio Composition')

    # --- Plot 3: Monte Carlo Simulation Scatter (Efficient Frontier) ---
    scatter = ax0.scatter(
        results_df['Volatilidade'], 
        results_df['Retorno'], 
        c=results_df['Sortino'], 
        cmap='viridis', 
        marker='.', 
        s=10, 
        alpha=0.4,
        label='Simulated Portfolios'
    )
    # Add colorbar to the scatter plot (ax0)
    cbar = fig.colorbar(scatter, ax=ax0)
    cbar.set_label('Sortino Ratio')
    
    # Highlight the Max Sortino portfolio
    ax0.scatter(
        best_portfolio['Volatilidade'], 
        best_portfolio['Retorno'], 
        marker='*', 
        color='gold', 
        s=500, 
        label='Max Sortino Portfolio'
    )
    
    ax0.set_title('Monte Carlo Simulation Scatter (Efficient Frontier)')
    ax0.set_xlabel('Annual Volatility (Risk)')
    ax0.set_ylabel('Annual Expected Return')
    ax0.legend(loc='upper left') # Garante que a legenda está num bom local interno
    ax0.grid(True, linestyle='--', alpha=0.5)
    
    # Apply layout adjustments
    plt.tight_layout()
    # Ajuste: Aumentar a margem inferior (bottom=0.07 é um bom valor para legendas inferiores)
    plt.subplots_adjust(top=0.9, hspace=0.3, bottom=0.07) 
    
    plt.show()