# backtester.py
"""Backtesting engine with proper transaction costs and walk-forward analysis"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

from config import BacktestConfig
from portfolio_optimizer import PortfolioOptimizer
from factor_calculator import FactorCalculator

logger = logging.getLogger(__name__)

class Backtester:
    """Walk-forward backtesting with transaction costs"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.results = {}
        
    def run_backtest(self, prices: pd.DataFrame, 
                    factor_scores: pd.DataFrame,
                    optimizer: PortfolioOptimizer,
                    start_date: Optional[str] = None,
                    end_date: Optional[str] = None) -> Dict:
        """Run walk-forward backtest"""
        
        # Date range
        if start_date:
            prices = prices[prices.index >= pd.to_datetime(start_date)]
            factor_scores = factor_scores[factor_scores.index >= pd.to_datetime(start_date)]
        if end_date:
            prices = prices[prices.index <= pd.to_datetime(end_date)]
            factor_scores = factor_scores[factor_scores.index <= pd.to_datetime(end_date)]
            
        # Initialize portfolio
        portfolio_value = self.config.initial_capital
        current_weights = pd.Series(dtype=float)
        
        # Results storage
        portfolio_values = []
        weights_history = []
        transactions = []
        
        # Rebalancing dates
        rebalance_dates = self._get_rebalance_dates(prices.index)
        
        # Walk through time
        for i, date in enumerate(prices.index):
            # Record current value
            portfolio_values.append({
                'date': date,
                'value': portfolio_value,
                'weights': current_weights.to_dict()
            })
            
            # Check if rebalancing needed
            if date in rebalance_dates and i < len(prices) - 1:
                # Get factor scores for this date
                if date not in factor_scores.index:
                    continue
                    
                current_scores = factor_scores.loc[date]
                
                # Select top stocks based on composite score
                # If factor_scores has multiple columns, use composite_score
                if isinstance(current_scores, pd.DataFrame):
                    if 'composite_score' in current_scores.columns:
                        current_scores = current_scores['composite_score']
                    else:
                        # Use mean of all scores if no composite
                        current_scores = current_scores.mean(axis=1)
                
                # Remove NaN values
                current_scores = current_scores.dropna()
                
                n_stocks = min(30, len(current_scores))  # Max 30 stocks
                if n_stocks == 0:
                    continue
                    
                top_stocks = current_scores.nlargest(n_stocks).index
                
                # Calculate expected returns (using factor scores as proxy)
                expected_returns = current_scores.loc[top_stocks]
                
                # Get historical data for covariance
                lookback = 252  # 1 year
                hist_start = max(0, i - lookback)
                hist_prices = prices.iloc[hist_start:i+1][top_stocks]
                
                if len(hist_prices) < 60:  # Need at least 60 days
                    continue
                    
                # Calculate covariance
                returns = hist_prices.pct_change().dropna()
                covariance = returns.cov() * 252  # Annualized
                
                # Optimize new weights
                new_weights = optimizer.optimize_portfolio(
                    expected_returns, 
                    covariance,
                    current_weights
                )
                
                # Apply turnover constraint
                new_weights = optimizer.apply_turnover_constraint(
                    new_weights, 
                    current_weights
                )
                
                # Execute trades
                trades, costs = self._execute_trades(
                    current_weights,
                    new_weights,
                    prices.iloc[i],
                    portfolio_value
                )
                
                # Update portfolio
                portfolio_value -= costs
                current_weights = new_weights
                weights_history.append({
                    'date': date,
                    'weights': new_weights.to_dict()
                })
                
                if trades:
                    transactions.extend(trades)
                    
                logger.info(f"Rebalanced on {date}: {len(new_weights)} positions, costs: ${costs:.2f}")
            
            # Calculate daily P&L
            if i < len(prices) - 1 and not current_weights.empty:
                # Get returns
                current_prices = prices.iloc[i]
                next_prices = prices.iloc[i + 1]
                
                # Calculate weighted return
                available_tickers = current_weights.index.intersection(current_prices.index)
                if len(available_tickers) > 0:
                    position_values = current_weights.loc[available_tickers] * portfolio_value
                    price_returns = (next_prices.loc[available_tickers] / 
                                   current_prices.loc[available_tickers] - 1)
                    daily_pnl = (position_values * price_returns).sum()
                    portfolio_value += daily_pnl
        
        # Create results DataFrame
        portfolio_df = pd.DataFrame(portfolio_values)
        portfolio_df.set_index('date', inplace=True)
        
        # Calculate metrics
        metrics = self._calculate_metrics(portfolio_df, prices)
        
        return {
            'portfolio_values': portfolio_df,
            'weights_history': weights_history,
            'transactions': transactions,
            'metrics': metrics
        }
    
    def _get_rebalance_dates(self, dates: pd.DatetimeIndex) -> List[pd.Timestamp]:
        """Get rebalancing dates based on frequency"""
        rebalance_dates = []
        
        if self.config.rebalance_frequency == 'daily':
            rebalance_dates = dates.tolist()
        elif self.config.rebalance_frequency == 'weekly':
            # Every Monday
            rebalance_dates = [d for d in dates if d.weekday() == 0]
        elif self.config.rebalance_frequency == 'monthly':
            # First trading day of each month
            rebalance_dates = dates.to_series().groupby(pd.Grouper(freq='M')).first().tolist()
        elif self.config.rebalance_frequency == 'quarterly':
            # First trading day of each quarter
            rebalance_dates = dates.to_series().groupby(pd.Grouper(freq='Q')).first().tolist()
            
        return rebalance_dates
    
    def _execute_trades(self, current_weights: pd.Series, 
                       new_weights: pd.Series,
                       current_prices: pd.Series,
                       portfolio_value: float) -> Tuple[List[Dict], float]:
        """Execute trades and calculate costs"""
        trades = []
        total_costs = 0
        
        # Get all tickers
        all_tickers = current_weights.index.union(new_weights.index)
        
        for ticker in all_tickers:
            current_weight = current_weights.get(ticker, 0)
            new_weight = new_weights.get(ticker, 0)
            
            if abs(new_weight - current_weight) < 0.001:  # No significant change
                continue
                
            if ticker not in current_prices.index:
                logger.warning(f"No price for {ticker}, skipping trade")
                continue
                
            price = current_prices[ticker]
            
            # Calculate shares to trade
            current_value = current_weight * portfolio_value
            new_value = new_weight * portfolio_value
            trade_value = new_value - current_value
            shares = trade_value / price
            
            # Transaction costs
            trade_cost = abs(trade_value) * self.config.transaction_cost
            
            # Slippage
            if trade_value > 0:  # Buying
                slippage_cost = trade_value * self.config.slippage
            else:  # Selling
                slippage_cost = abs(trade_value) * self.config.slippage
                
            total_cost = trade_cost + slippage_cost
            total_costs += total_cost
            
            trades.append({
                'ticker': ticker,
                'shares': shares,
                'price': price,
                'value': trade_value,
                'cost': total_cost,
                'type': 'BUY' if trade_value > 0 else 'SELL'
            })
            
        return trades, total_costs
    
    def _calculate_metrics(self, portfolio_df: pd.DataFrame, 
                          prices: pd.DataFrame) -> Dict:
        """Calculate performance metrics"""
        # Returns
        returns = portfolio_df['value'].pct_change().dropna()
        
        # Annualized metrics
        trading_days = 252
        n_days = len(returns)
        annualization_factor = trading_days / n_days
        
        # CAGR
        total_return = portfolio_df['value'].iloc[-1] / portfolio_df['value'].iloc[0] - 1
        years = n_days / trading_days
        cagr = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
        
        # Volatility
        volatility = returns.std() * np.sqrt(trading_days)
        
        # Sharpe ratio
        excess_returns = returns - self.config.risk_free_rate / trading_days
        sharpe = np.sqrt(trading_days) * excess_returns.mean() / returns.std() if returns.std() > 0 else 0
        
        # Sortino ratio
        downside_returns = returns[returns < 0]
        downside_vol = downside_returns.std() * np.sqrt(trading_days)
        sortino = np.sqrt(trading_days) * excess_returns.mean() / downside_returns.std() if len(downside_returns) > 0 else 0
        
        # Maximum drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Calmar ratio
        calmar = cagr / abs(max_drawdown) if max_drawdown != 0 else 0
        
        # Win rate
        win_rate = (returns > 0).mean()
        
        # Benchmark comparison
        if self.config.benchmark and self.config.benchmark in prices.columns:
            benchmark_returns = prices[self.config.benchmark].pct_change().dropna()
            benchmark_returns = benchmark_returns.loc[returns.index]
            
            # Information ratio
            active_returns = returns - benchmark_returns
            tracking_error = active_returns.std() * np.sqrt(trading_days)
            info_ratio = active_returns.mean() * trading_days / tracking_error if tracking_error > 0 else 0
            
            # Beta
            covariance = returns.cov(benchmark_returns)
            benchmark_variance = benchmark_returns.var()
            beta = covariance / benchmark_variance if benchmark_variance > 0 else 1
            
            # Alpha
            alpha = cagr - (self.config.risk_free_rate + beta * (benchmark_returns.mean() * trading_days - self.config.risk_free_rate))
        else:
            info_ratio = 0
            beta = 1
            alpha = 0
        
        return {
            'total_return': total_return,
            'cagr': cagr,
            'volatility': volatility,
            'sharpe_ratio': sharpe,
            'sortino_ratio': sortino,
            'max_drawdown': max_drawdown,
            'calmar_ratio': calmar,
            'win_rate': win_rate,
            'information_ratio': info_ratio,
            'beta': beta,
            'alpha': alpha,
            'n_trades': len([t for t in portfolio_df.get('transactions', [])]),
            'avg_n_positions': np.mean([len(w.get('weights', {})) for _, w in portfolio_df.iterrows()])
        }
    
    def generate_report(self, results: Dict) -> str:
        """Generate a text report of backtest results"""
        metrics = results['metrics']
        
        report = f"""
Backtest Results
================

Performance Metrics:
- Total Return: {metrics['total_return']:.1%}
- CAGR: {metrics['cagr']:.1%}
- Volatility: {metrics['volatility']:.1%}
- Sharpe Ratio: {metrics['sharpe_ratio']:.2f}
- Sortino Ratio: {metrics['sortino_ratio']:.2f}
- Max Drawdown: {metrics['max_drawdown']:.1%}
- Calmar Ratio: {metrics['calmar_ratio']:.2f}
- Win Rate: {metrics['win_rate']:.1%}

Risk Metrics:
- Beta: {metrics['beta']:.2f}
- Alpha: {metrics['alpha']:.1%}
- Information Ratio: {metrics['information_ratio']:.2f}

Portfolio Statistics:
- Number of Trades: {metrics['n_trades']}
- Avg Positions: {metrics['avg_n_positions']:.0f}

Configuration:
- Initial Capital: ${self.config.initial_capital:,.0f}
- Rebalance Frequency: {self.config.rebalance_frequency}
- Transaction Cost: {self.config.transaction_cost:.1%}
- Slippage: {self.config.slippage:.1%}
"""
        return report