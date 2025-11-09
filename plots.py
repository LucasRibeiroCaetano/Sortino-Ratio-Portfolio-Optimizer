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
    Line 2: Monte Carlo Simulation (70% width) (Aligned with Performance plot)
    """
    setup_style()
    
    weights = best_portfolio['Weights']
    
    # --- Data Preparation ---
    pie_weights = pd.Series(weights, index=tickers)
    pie_weights = pie_weights[pie_weights > 0.01]
    
    port_daily_returns = (daily_returns * weights).sum(axis=1)
    cumulative_returns = (1 + port_daily_returns).cumprod()
    cumulative_returns_pct = (cumulative_returns - 1) * 100
    
    # --- Colormap Selection ---
    cmap = plt.get_cmap('tab20')
    colors = cmap(np.arange(len(pie_weights)) % cmap.N) # Guaranteed unique colors

    # ----------------------------------------------------
    # 2. Setup the figure and the custom 2-row layout
    # ----------------------------------------------------
    
    fig = plt.figure(figsize=(24, 16)) 
    fig.suptitle('Sortino Ratio Portfolio Optimization', fontsize=24, y=0.98, fontweight='bold')
    
    # Ax1: Portfolio Performance (Row 0, takes 2/3 width)
    ax1 = plt.subplot2grid((2, 3), (0, 0), colspan=2)
    
    # Ax2: Pie Chart (Row 0, takes 1/3 width)
    ax2 = plt.subplot2grid((2, 3), (0, 2))
    
    # Ax0: Monte Carlo Simulation (Row 1, takes 2/3 width - Aligned with Ax1)
    ax0 = plt.subplot2grid((2, 3), (1, 0), colspan=2) 
    
    # Ax3: Empty space for Legend and Color Bar (Row 1, Col 2)
    ax3 = plt.subplot2grid((2, 3), (1, 2))
    ax3.axis('off')


    # --- Plot 1: Portfolio Performance (Line Plot) ---
    cumulative_returns_pct.plot(ax=ax1, label='Portfolio Performance', color='cyan')
    ax1.set_title(f'Cumulative Return ({start_date} to {end_date})')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Cumulative Return (%)')
    ax1.grid(True, linestyle='--', alpha=0.5)

    # --- Plot 2: Portfolio Composition (Pie Chart) ---

    # Create legend labels with ticker and percentage    
    legend_labels = [f'{ticker}: {weight*100:.1f}%' for ticker, weight in pie_weights.items()]
    
    # Plot pie chart
    wedges, texts = ax2.pie(
        pie_weights, 
        colors=colors,               # Usa cores únicas
        startangle=90,
        pctdistance=1.1, 
        labeldistance=1.1
    )
    
    # Add legend outside the pie chart
    ax2.legend(wedges, legend_labels,
              title="Allocation",
              loc="center left", 
              bbox_to_anchor=(1.05, 0, 0.5, 1))
    
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
    
    # Place colorbar in the empty subplot (ax3)
    cbar = fig.colorbar(scatter, ax=ax3, fraction=1.0, pad=0.0) 
    cbar.ax.set_visible(True)
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
    
    ax0.legend(loc='upper left') 
    ax0.grid(True, linestyle='--', alpha=0.5)
    
    # Apply layout adjustments
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, hspace=0.3, bottom=0.07) 
    
    plt.show()