# main.py
"""Main script to coordinate the factor-based stock analysis and backtesting"""

import asyncio
import pandas as pd
import numpy as np
from datetime import datetime
import argparse
import sys
from pathlib import Path
import json

from config import Config, DEFAULT_CONFIG
from data_fetcher import DataFetcher
from factor_calculator import FactorCalculator
from portfolio_optimizer import PortfolioOptimizer
from backtester import Backtester
from short_term_signal_generator import ShortTermSignalGenerator
import utils
from companies import TICKERS

import logging
logger = logging.getLogger(__name__)

class FactorAnalysisSystem:
    """Main system coordinating all components"""
    
    def __init__(self, config: Config):
        self.config = config
        utils.setup_logging(config.log_level, config.log_file)
        
        self.data_fetcher = DataFetcher(config.data)
        self.factor_calculator = FactorCalculator(config.factors, config.weights)
        self.portfolio_optimizer = PortfolioOptimizer(config.portfolio)
        self.backtester = Backtester(config.backtest)
        
        # Short-term components
        self.short_factor_calc = FactorCalculator(config.short_factors, config.weights)
        self.signal_generator = ShortTermSignalGenerator(self.short_factor_calc, config.signals)
        
    async def fetch_data(self, tickers: list) -> dict:
        """Fetch all required data"""
        logger.info(f"Fetching data for {len(tickers)} tickers...")
        
        # Fetch data
        data = await self.data_fetcher.fetch_multiple_tickers(tickers, period='5y')
        
        # Validate data quality
        clean_data = self.data_fetcher.validate_data_quality(data)
        
        # Log data quality issues
        issues = utils.validate_data_integrity(clean_data)
        for issue_type, issue_list in issues.items():
            if issue_list:
                logger.warning(f"{issue_type}: {len(issue_list)} issues")
                
        return clean_data
    
    def calculate_factors(self, data: dict) -> pd.DataFrame:
        """Calculate all factors"""
        logger.info("Calculating factors...")
        
        # Get aligned price data
        prices = self.data_fetcher.get_aligned_prices(data)
        
        # Calculate different factor types
        factor_dfs = []
        
        # Momentum factors
        momentum_factors = self.factor_calculator.calculate_momentum_factors(prices)
        if not momentum_factors.empty:
            factor_dfs.append(momentum_factors)
        
        # Volatility factors
        volatility_factors = self.factor_calculator.calculate_volatility_factors(prices)
        if not volatility_factors.empty:
            factor_dfs.append(volatility_factors)
        
        # Technical factors
        technical_factors = self.factor_calculator.calculate_technical_factors(data)
        if not technical_factors.empty:
            factor_dfs.append(technical_factors)
        
        # Combine all time-series factors
        if factor_dfs:
            all_factors = pd.concat(factor_dfs, axis=1)
        else:
            all_factors = pd.DataFrame()
        
        # Add fundamental factors for each date
        fundamental_factors_list = []
        for date in prices.index[-252:]:  # Last year of dates
            fundamental_factors = self.factor_calculator.calculate_fundamental_factors(data, date)
            if not fundamental_factors.empty:
                fundamental_factors['date'] = date
                fundamental_factors_list.append(fundamental_factors)
        
        if fundamental_factors_list:
            fundamental_df = pd.concat(fundamental_factors_list)
            fundamental_df = fundamental_df.set_index(['date', fundamental_df.index])
        
        logger.info(f"Calculated {len(all_factors.columns)} factors")
        
        return all_factors
    
    def run_analysis(self, tickers: list) -> dict:
        """Run complete analysis pipeline"""
        # Fetch data asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(self.fetch_data(tickers))
        loop.close()
        
        if not data:
            logger.error("No data available for analysis")
            return None
        
        # Calculate factors
        factors = self.calculate_factors(data)
        
        # Get prices for score calculation
        prices = self.data_fetcher.get_aligned_prices(data)
        
        # Calculate composite scores
        # For now, create a simple score based on momentum (most reliable factor)
        # We'll use the most recent momentum values as scores
        momentum_cols = [col for col in factors.columns if 'momentum' in col]
        if momentum_cols:
            # Average momentum across different windows for each ticker
            ticker_scores = {}
            for ticker in prices.columns:
                ticker_momentum_cols = [col for col in momentum_cols if ticker in col]
                if ticker_momentum_cols:
                    ticker_scores[ticker] = factors[ticker_momentum_cols].mean(axis=1)
            
            scores = pd.DataFrame(ticker_scores)
        else:
            # Fallback: use price returns as scores
            scores = prices.pct_change(21).rolling(252).mean()
        
        # Get current rankings
        latest_scores = scores.iloc[-1] if not scores.empty else pd.Series()
        rankings = latest_scores.sort_values(ascending=False)
        
        # Run backtest (reuse prices from above)
        backtest_results = self.backtester.run_backtest(
            prices, 
            scores,
            self.portfolio_optimizer
        )
        
        # Clean up
        self.data_fetcher.close()
        
        return {
            'data': data,
            'factors': factors,
            'scores': scores,
            'rankings': rankings,
            'backtest': backtest_results
        }
    
    def display_results(self, results: dict):
        """Display analysis results"""
        if not results:
            return
            
        rankings = results['rankings']
        backtest = results['backtest']
        
        print("\n" + "="*60)
        print("TOP RANKED STOCKS (by Composite Score)")
        print("="*60)
        
        top_20 = rankings.head(20)
        for i, (ticker, score) in enumerate(top_20.items(), 1):
            print(f"{i:2d}. {ticker:6s} Score: {score:6.2f}")
        
        print("\n" + "="*60)
        print("BACKTEST RESULTS")
        print("="*60)
        print(self.backtester.generate_report(backtest))
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        # Save backtest results
        utils.save_results(backtest, results_dir / f"backtest_{timestamp}.json")
        
        # Save plots
        utils.plot_backtest_results(backtest, results_dir / f"backtest_{timestamp}.png")
        
        # Export to Excel
        utils.export_to_excel(backtest, results_dir / f"backtest_{timestamp}.xlsx")
        
        logger.info(f"Results saved to {results_dir}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Factor-based Stock Analysis System")
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--tickers', nargs='+', help='List of tickers to analyze')
    parser.add_argument('--list', type=str, help='Ticker list name from companies.py')
    parser.add_argument('--backtest-only', action='store_true', help='Run backtest only')
    parser.add_argument('--export', type=str, help='Export format (json, excel, csv)')
    parser.add_argument('--weekly-signals', action='store_true', help='Emit one-week trade recommendations only')
    
    args = parser.parse_args()
    
    # Load config
    if args.config:
        config_data = utils.load_config(args.config)
        config = Config.from_dict(config_data)
    else:
        config = DEFAULT_CONFIG
    
    # Get tickers
    if args.tickers:
        tickers = args.tickers
    elif args.list:
        # Import the specified list from companies.py
        from companies import __dict__ as companies_dict
        if args.list in companies_dict:
            tickers = companies_dict[args.list]
        else:
            print(f"Error: List '{args.list}' not found in companies.py")
            print("Available lists:", [k for k in companies_dict.keys() if isinstance(companies_dict[k], list)])
            sys.exit(1)
    else:
        # Use default from companies.py
        tickers = TICKERS
    
    # Initialize system
    system = FactorAnalysisSystem(config)
    
    # Run analysis
    try:
        if args.weekly_signals:
            # Run weekly signal generation only
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            data = loop.run_until_complete(system.fetch_data(tickers))
            loop.close()
            
            signals = system.signal_generator.generate_signals(data)
            if not signals.empty:
                print("\n" + "="*60)
                print("WEEKLY TRADING SIGNALS")
                print("="*60)
                print(signals.to_string(index=False))
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                utils.save_results({'weekly_signals': signals.to_dict('records')},
                                   Path('results') / f"signals_{timestamp}.json")
            else:
                print("No signals generated today.")
        else:
            # Run full analysis
            results = system.run_analysis(tickers)
            system.display_results(results)
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()