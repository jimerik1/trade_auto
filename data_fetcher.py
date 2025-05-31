# data_fetcher.py
"""Async data fetching with caching and error handling"""

import asyncio
import aiohttp
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import pickle
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging
from concurrent.futures import ThreadPoolExecutor

from config import DataConfig

logger = logging.getLogger(__name__)

class DataFetcher:
    """Handles all data fetching with async operations and caching"""
    
    def __init__(self, config: DataConfig):
        self.config = config
        self.cache_dir = Path(config.cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.executor = ThreadPoolExecutor(max_workers=config.batch_size)
        
    def _get_cache_path(self, ticker: str, data_type: str) -> Path:
        """Get cache file path for a ticker and data type"""
        return self.cache_dir / f"{ticker}_{data_type}.pkl"
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Check if cache file is valid and not expired"""
        if not cache_path.exists():
            return False
        
        if not self.config.use_cache:
            return False
            
        # Check expiry
        file_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        expiry_time = file_time + timedelta(hours=self.config.cache_expiry_hours)
        
        return datetime.now() < expiry_time
    
    def _save_to_cache(self, data: any, ticker: str, data_type: str):
        """Save data to cache"""
        cache_path = self._get_cache_path(ticker, data_type)
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)
            
    def _load_from_cache(self, ticker: str, data_type: str) -> Optional[any]:
        """Load data from cache"""
        cache_path = self._get_cache_path(ticker, data_type)
        if self._is_cache_valid(cache_path):
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        return None
    
    async def fetch_price_data(self, ticker: str, period: str = '5y') -> Optional[pd.DataFrame]:
        """Fetch price data for a single ticker"""
        # Check cache first
        cached_data = self._load_from_cache(ticker, f"prices_{period}")
        if cached_data is not None:
            logger.debug(f"Loaded {ticker} prices from cache")
            return cached_data
            
        try:
            # Use thread executor for yfinance (not truly async)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                self.executor,
                self._fetch_yf_prices,
                ticker,
                period
            )
            
            if data is not None and not data.empty:
                self._save_to_cache(data, ticker, f"prices_{period}")
                logger.info(f"Fetched {ticker} price data: {len(data)} days")
                return data
            else:
                logger.warning(f"No price data for {ticker}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching price data for {ticker}: {e}")
            return None
    
    def _fetch_yf_prices(self, ticker: str, period: str) -> pd.DataFrame:
        """Fetch prices using yfinance"""
        stock = yf.Ticker(ticker)
        data = stock.history(period=period, auto_adjust=self.config.adjust_prices)
        
        # Add some data quality checks
        if data.empty:
            return data
            
        # Remove any rows with NaN in critical columns
        data = data.dropna(subset=['Close', 'Volume'])
        
        # Remove any duplicate indices
        data = data[~data.index.duplicated(keep='first')]
        
        # Sort by date
        data = data.sort_index()
        
        return data
    
    async def fetch_fundamental_data(self, ticker: str) -> Optional[Dict]:
        """Fetch fundamental data for a single ticker"""
        # Check cache first
        cached_data = self._load_from_cache(ticker, "fundamentals")
        if cached_data is not None:
            logger.debug(f"Loaded {ticker} fundamentals from cache")
            return cached_data
            
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                self.executor,
                self._fetch_yf_fundamentals,
                ticker
            )
            
            if data:
                self._save_to_cache(data, ticker, "fundamentals")
                logger.info(f"Fetched {ticker} fundamental data")
                return data
            else:
                logger.warning(f"No fundamental data for {ticker}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching fundamental data for {ticker}: {e}")
            return None
    
    def _fetch_yf_fundamentals(self, ticker: str) -> Dict:
        """Fetch fundamentals using yfinance"""
        stock = yf.Ticker(ticker)
        
        # Get all available data
        info = stock.info or {}
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cashflow = stock.cashflow
        
        # Clean and validate the data
        clean_info = {}
        for key, value in info.items():
            # Skip None values and empty strings
            if value is not None and value != '':
                # Handle special cases
                if key in ['trailingPE', 'forwardPE', 'pegRatio'] and value == 0:
                    continue  # Skip zero P/E ratios
                clean_info[key] = value
        
        return {
            'info': clean_info,
            'financials': financials.to_dict() if financials is not None and not financials.empty else {},
            'balance_sheet': balance_sheet.to_dict() if balance_sheet is not None and not balance_sheet.empty else {},
            'cashflow': cashflow.to_dict() if cashflow is not None and not cashflow.empty else {}
        }
    
    async def fetch_multiple_tickers(self, tickers: List[str], period: str = '5y') -> Dict[str, Dict]:
        """Fetch data for multiple tickers concurrently"""
        all_data = {}
        
        # Process in batches
        for i in range(0, len(tickers), self.config.batch_size):
            batch = tickers[i:i + self.config.batch_size]
            
            # Create tasks for price and fundamental data
            price_tasks = [self.fetch_price_data(ticker, period) for ticker in batch]
            fundamental_tasks = [self.fetch_fundamental_data(ticker) for ticker in batch]
            
            # Run concurrently
            price_results = await asyncio.gather(*price_tasks, return_exceptions=True)
            fundamental_results = await asyncio.gather(*fundamental_tasks, return_exceptions=True)
            
            # Combine results
            for ticker, price_data, fundamental_data in zip(batch, price_results, fundamental_results):
                if isinstance(price_data, Exception):
                    logger.error(f"Price fetch failed for {ticker}: {price_data}")
                    price_data = None
                if isinstance(fundamental_data, Exception):
                    logger.error(f"Fundamental fetch failed for {ticker}: {fundamental_data}")
                    fundamental_data = None
                    
                if price_data is not None:
                    all_data[ticker] = {
                        'prices': price_data,
                        'fundamentals': fundamental_data or {}
                    }
            
            # Brief pause between batches to avoid rate limiting
            if i + self.config.batch_size < len(tickers):
                await asyncio.sleep(0.5)
        
        return all_data
    
    def validate_data_quality(self, data: Dict[str, Dict]) -> Dict[str, Dict]:
        """Validate and clean the fetched data"""
        clean_data = {}
        
        for ticker, ticker_data in data.items():
            prices = ticker_data.get('prices')
            
            if prices is None or prices.empty:
                logger.warning(f"Skipping {ticker}: No price data")
                continue
                
            # Check minimum data points (default to 252 trading days = 1 year)
            min_data_points = 252
            if len(prices) < min_data_points:
                logger.warning(f"Skipping {ticker}: Only {len(prices)} days of data (need at least {min_data_points})")
                continue
                
            # Check for too many missing values
            missing_pct = prices['Close'].isna().sum() / len(prices)
            if missing_pct > 0.1:  # More than 10% missing
                logger.warning(f"Skipping {ticker}: {missing_pct:.1%} missing values")
                continue
                
            # Check for stale data
            last_date = prices.index[-1]
            # Convert to timezone-naive for comparison
            if hasattr(last_date, 'tz_localize'):
                last_date_naive = last_date.tz_localize(None)
            else:
                last_date_naive = last_date
            
            days_old = (datetime.now() - last_date_naive).days
            if days_old > 5:  # More than 5 days old
                logger.warning(f"Warning: {ticker} data is {days_old} days old")
            
            clean_data[ticker] = ticker_data
            
        logger.info(f"Data validation complete: {len(clean_data)}/{len(data)} tickers passed")
        return clean_data
    
    def get_aligned_prices(self, data: Dict[str, Dict], 
                          start_date: Optional[str] = None,
                          end_date: Optional[str] = None) -> pd.DataFrame:
        """Get aligned price data for all tickers"""
        price_dict = {}
        
        for ticker, ticker_data in data.items():
            prices = ticker_data['prices']['Close']
            price_dict[ticker] = prices
            
        # Create aligned DataFrame
        aligned_prices = pd.DataFrame(price_dict)
        
        # Apply date filters if provided
        if start_date:
            aligned_prices = aligned_prices[aligned_prices.index >= pd.to_datetime(start_date)]
        if end_date:
            aligned_prices = aligned_prices[aligned_prices.index <= pd.to_datetime(end_date)]
            
        # Forward fill missing values (up to 5 days)
        aligned_prices = aligned_prices.fillna(method='ffill', limit=5)
        
        return aligned_prices
    
    def close(self):
        """Clean up resources"""
        self.executor.shutdown(wait=True)