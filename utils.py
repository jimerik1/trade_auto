# utils.py
"""Utility functions and helpers"""

import pandas as pd
import numpy as np
import logging
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Union
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

logger = logging.getLogger(__name__)

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """Setup logging configuration"""
    handlers = [logging.StreamHandler()]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

def load_config(config_path: Union[str, Path]) -> Dict:
    """Load configuration from YAML or JSON file"""
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        if config_path.suffix == '.yaml' or config_path.suffix == '.yml':
            return yaml.safe_load(f)
        elif config_path.suffix == '.json':
            return json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {config_path.suffix}")

def save_results(results: Dict, output_path: Union[str, Path]):
    """Save backtest results to file"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert DataFrames to dict for JSON serialization
    serializable_results = {}
    for key, value in results.items():
        if isinstance(value, pd.DataFrame):
            serializable_results[key] = {
                'data': value.to_dict(),
                'index': value.index.tolist()
            }
        elif isinstance(value, pd.Series):
            serializable_results[key] = value.to_dict()
        else:
            serializable_results[key] = value
    
    with open(output_path, 'w') as f:
        json.dump(serializable_results, f, indent=2, default=str)

def plot_backtest_results(results: Dict, save_path: Optional[Union[str, Path]] = None):
    """Create visualization of backtest results"""
    portfolio_values = results['portfolio_values']
    metrics = results['metrics']
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Backtest Results', fontsize=16)
    
    # 1. Portfolio value over time
    ax1 = axes[0, 0]
    portfolio_values['value'].plot(ax=ax1)
    ax1.set_title('Portfolio Value Over Time')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Portfolio Value ($)')
    ax1.grid(True, alpha=0.3)
    
    # 2. Drawdown chart
    ax2 = axes[0, 1]
    returns = portfolio_values['value'].pct_change()
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    drawdown.plot(ax=ax2, color='red')
    ax2.fill_between(drawdown.index, 0, drawdown.values, alpha=0.3, color='red')
    ax2.set_title('Drawdown')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Drawdown (%)')
    ax2.grid(True, alpha=0.3)
    
    # 3. Monthly returns heatmap
    ax3 = axes[1, 0]
    monthly_returns = returns.resample('M').sum()
    monthly_returns_pivot = monthly_returns.groupby([monthly_returns.index.year, 
                                                    monthly_returns.index.month]).sum().unstack()
    sns.heatmap(monthly_returns_pivot, cmap='RdYlGn', center=0, 
                annot=True, fmt='.1%', ax=ax3)
    ax3.set_title('Monthly Returns Heatmap')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Year')
    
    # 4. Performance metrics
    ax4 = axes[1, 1]
    ax4.axis('off')
    metrics_text = f"""
    Performance Summary:
    
    Total Return: {metrics['total_return']:.1%}
    CAGR: {metrics['cagr']:.1%}
    Volatility: {metrics['volatility']:.1%}
    Sharpe Ratio: {metrics['sharpe_ratio']:.2f}
    Max Drawdown: {metrics['max_drawdown']:.1%}
    Win Rate: {metrics['win_rate']:.1%}
    """
    ax4.text(0.1, 0.5, metrics_text, fontsize=12, verticalalignment='center')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

def create_tear_sheet(results: Dict, save_path: Optional[Union[str, Path]] = None):
    """Create a comprehensive tear sheet"""
    # This would create a more detailed analysis report
    # For now, using the basic plot function
    return plot_backtest_results(results, save_path)

def validate_data_integrity(data: Dict[str, Dict]) -> Dict[str, List[str]]:
    """Validate data integrity and return issues"""
    issues = {
        'missing_prices': [],
        'missing_fundamentals': [],
        'stale_data': [],
        'suspicious_values': []
    }
    
    for ticker, ticker_data in data.items():
        # Check for missing data
        if ticker_data.get('prices') is None or ticker_data['prices'].empty:
            issues['missing_prices'].append(ticker)
            
        if not ticker_data.get('fundamentals'):
            issues['missing_fundamentals'].append(ticker)
            
        # Check for stale data
        if ticker_data.get('prices') is not None and not ticker_data['prices'].empty:
            last_date = ticker_data['prices'].index[-1]
            # Convert to timezone-naive for comparison
            if hasattr(last_date, 'tz_localize'):
                last_date_naive = last_date.tz_localize(None)
            else:
                last_date_naive = last_date
            
            days_old = (datetime.now() - last_date_naive).days
            if days_old > 5:
                issues['stale_data'].append(f"{ticker}: {days_old} days old")
        
        # Check for suspicious values
        info = ticker_data.get('fundamentals', {}).get('info', {})
        if info.get('trailingPE', 0) < 0:
            issues['suspicious_values'].append(f"{ticker}: negative P/E")
        if info.get('marketCap', 0) < 1e6:  # Less than $1M
            issues['suspicious_values'].append(f"{ticker}: tiny market cap")
    
    return issues

def get_sector_mapping(tickers: List[str], data: Dict[str, Dict]) -> Dict[str, str]:
    """Extract sector mapping from data"""
    sector_map = {}
    
    for ticker in tickers:
        info = data.get(ticker, {}).get('fundamentals', {}).get('info', {})
        sector = info.get('sector', 'Unknown')
        sector_map[ticker] = sector
    
    return sector_map

def calculate_correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    """Calculate and clean correlation matrix"""
    # Calculate correlation
    corr_matrix = returns.corr()
    
    # Clean up numerical issues
    corr_matrix = corr_matrix.fillna(0)
    np.fill_diagonal(corr_matrix.values, 1.0)
    
    # Ensure symmetry
    corr_matrix = (corr_matrix + corr_matrix.T) / 2
    
    return corr_matrix

def export_to_excel(results: Dict, output_path: Union[str, Path]):
    """Export results to Excel with multiple sheets"""
    output_path = Path(output_path)
    
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        # Portfolio values
        results['portfolio_values'].to_excel(writer, sheet_name='Portfolio Values')
        
        # Metrics
        metrics_df = pd.DataFrame([results['metrics']])
        metrics_df.to_excel(writer, sheet_name='Metrics', index=False)
        
        # Transactions
        if 'transactions' in results and results['transactions']:
            transactions_df = pd.DataFrame(results['transactions'])
            transactions_df.to_excel(writer, sheet_name='Transactions', index=False)
        
        # Weights history
        if 'weights_history' in results and results['weights_history']:
            weights_df = pd.DataFrame(results['weights_history'])
            weights_df.to_excel(writer, sheet_name='Weights History', index=False)
    
    logger.info(f"Results exported to {output_path}")

def format_number(value: float, format_type: str = 'general') -> str:
    """Format numbers for display"""
    if pd.isna(value):
        return 'N/A'
    
    if format_type == 'percent':
        return f"{value:.1%}"
    elif format_type == 'currency':
        return f"${value:,.0f}"
    elif format_type == 'decimal':
        return f"{value:.2f}"
    else:
        return f"{value:.3g}"