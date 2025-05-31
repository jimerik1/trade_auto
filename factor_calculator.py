# factor_calculator.py
"""Factor calculation with proper z-score normalization and winsorization"""

import pandas as pd
import numpy as np
import talib
from typing import Dict, List, Optional, Tuple
import logging
from scipy import stats

from config import FactorConfig, FactorWeights

logger = logging.getLogger(__name__)

class FactorCalculator:
    """Calculate factors with proper normalization"""
    
    def __init__(self, config: FactorConfig, weights: FactorWeights):
        self.config = config
        self.weights = weights
        
    def calculate_zscore(self, series: pd.Series, window: int = None) -> pd.Series:
        """Calculate rolling z-score with proper handling of NaN values"""
        if window is None:
            window = self.config.zscore_window
            
        rolling_mean = series.rolling(window=window, min_periods=window//2).mean()
        rolling_std = series.rolling(window=window, min_periods=window//2).std()
        
        # Avoid division by zero
        rolling_std = rolling_std.replace(0, np.nan)
        
        zscore = (series - rolling_mean) / rolling_std
        
        # Winsorize extreme values
        if self.config.winsorize_sigma > 0:
            zscore = zscore.clip(
                lower=-self.config.winsorize_sigma,
                upper=self.config.winsorize_sigma
            )
            
        return zscore
    
    def calculate_momentum_factors(self, prices: pd.DataFrame) -> pd.DataFrame:
        """Calculate momentum factors for all tickers"""
        factor_list = []
        
        for window in self.config.momentum_windows:
            # Calculate returns
            returns = prices.pct_change(window)
            
            # Apply z-score normalization
            factor_name = f'momentum_{window}d'
            zscore_returns = self.calculate_zscore(returns)
            
            # Rename columns to include factor name
            zscore_returns.columns = [f'{factor_name}_{col}' for col in zscore_returns.columns]
            factor_list.append(zscore_returns)
            
            logger.debug(f"Calculated {factor_name} for {len(prices.columns)} tickers")
        
        # Concatenate all factors horizontally
        if factor_list:
            return pd.concat(factor_list, axis=1)
        else:
            return pd.DataFrame()
    
    def calculate_volatility_factors(self, prices: pd.DataFrame) -> pd.DataFrame:
        """Calculate volatility factors"""
        factor_list = []
        
        # Daily returns
        returns = prices.pct_change()
        
        for window in self.config.volatility_windows:
            # Annualized volatility
            vol = returns.rolling(window=window, min_periods=window//2).std() * np.sqrt(252)
            
            # Invert and normalize (lower volatility is better)
            factor_name = f'volatility_{window}d'
            zscore_vol = -self.calculate_zscore(vol)
            
            # Rename columns to include factor name
            zscore_vol.columns = [f'{factor_name}_{col}' for col in zscore_vol.columns]
            factor_list.append(zscore_vol)
            
            logger.debug(f"Calculated {factor_name}")
        
        # Concatenate all factors horizontally
        if factor_list:
            return pd.concat(factor_list, axis=1)
        else:
            return pd.DataFrame()
    
    def calculate_technical_factors(self, data: Dict[str, Dict]) -> pd.DataFrame:
        """Calculate technical indicators"""
        all_factors = []
        
        for ticker, ticker_data in data.items():
            prices = ticker_data['prices']
            if prices is None or prices.empty:
                continue
                
            # Convert to float64 for TA-Lib
            close = prices['Close'].values.astype(np.float64)
            high = prices['High'].values.astype(np.float64)
            low = prices['Low'].values.astype(np.float64)
            volume = prices['Volume'].values.astype(np.float64)
            
            factors = {}
            
            # RSI - normalized distance from 50 (mean reversion)
            if len(close) > 14:
                rsi = talib.RSI(close, timeperiod=14)
                rsi_distance = np.abs(rsi - 50)
                factors['rsi_mean_reversion'] = -rsi_distance  # Negative because closer to 50 is better
            
            # MACD signal strength (not just binary)
            if len(close) > 26:
                macd, signal, hist = talib.MACD(close)
                factors['macd_histogram'] = hist
            
            # Bollinger Band position
            if len(close) > 20:
                upper, middle, lower = talib.BBANDS(close, timeperiod=20)
                bb_position = (close - lower) / (upper - lower)
                factors['bb_position'] = bb_position - 0.5  # Center around 0
            
            # Volume trends
            if len(volume) > 20:
                # Convert to float64 for TA-Lib
                volume_float = volume.astype(np.float64)
                volume_sma = talib.SMA(volume_float, timeperiod=20)
                factors['volume_ratio'] = volume / volume_sma - 1
            
            # Convert to DataFrame with DatetimeIndex
            factor_df = pd.DataFrame(factors, index=prices.index)
            factor_df['ticker'] = ticker
            all_factors.append(factor_df)
        
        if not all_factors:
            return pd.DataFrame()
            
        # Combine all tickers and pivot to wide format
        combined = pd.concat(all_factors)
        
        # Pivot to have tickers as columns
        result_dfs = []
        for factor_col in [col for col in combined.columns if col != 'ticker']:
            # Create a pivot table for each factor
            factor_wide = combined.pivot_table(
                index=combined.index,
                columns='ticker',
                values=factor_col,
                aggfunc='first'
            )
            
            # Normalize across tickers for each date
            for date in factor_wide.index:
                factor_wide.loc[date] = self._cross_sectional_zscore(factor_wide.loc[date])
            
            # Rename columns to include factor name
            factor_wide.columns = [f'{factor_col}_{ticker}' for ticker in factor_wide.columns]
            result_dfs.append(factor_wide)
        
        if result_dfs:
            return pd.concat(result_dfs, axis=1)
        else:
            return pd.DataFrame()
    
    def calculate_fundamental_factors(self, data: Dict[str, Dict], 
                                    reference_date: pd.Timestamp) -> pd.DataFrame:
        """Calculate fundamental factors for a specific date"""
        factor_rows = []
        
        for ticker, ticker_data in data.items():
            fundamentals = ticker_data.get('fundamentals', {})
            info = fundamentals.get('info', {})
            
            if not info:
                continue
                
            factors = {
                'ticker': ticker,
                'date': reference_date
            }
            
            # Valuation factors (lower is better, so we'll invert later)
            factors['pe_ratio'] = info.get('trailingPE', np.nan)
            factors['forward_pe'] = info.get('forwardPE', np.nan)
            factors['pb_ratio'] = info.get('priceToBook', np.nan)
            factors['ps_ratio'] = info.get('priceToSalesTrailing12Months', np.nan)
            factors['peg_ratio'] = info.get('pegRatio', np.nan)
            factors['ev_ebitda'] = info.get('enterpriseToEbitda', np.nan)
            
            # Quality factors (higher is better)
            factors['roe'] = info.get('returnOnEquity', np.nan)
            factors['roa'] = info.get('returnOnAssets', np.nan)
            factors['profit_margin'] = info.get('profitMargins', np.nan)
            factors['operating_margin'] = info.get('operatingMargins', np.nan)
            
            # Growth factors
            factors['revenue_growth'] = info.get('revenueGrowth', np.nan)
            factors['earnings_growth'] = info.get('earningsGrowth', np.nan)
            
            # Financial health
            factors['debt_to_equity'] = info.get('debtToEquity', np.nan)
            factors['current_ratio'] = info.get('currentRatio', np.nan)
            factors['quick_ratio'] = info.get('quickRatio', np.nan)
            factors['free_cashflow_yield'] = self._calculate_fcf_yield(info)
            
            # Market factors
            factors['market_cap'] = np.log(info.get('marketCap', 1))  # Log transform
            factors['beta'] = info.get('beta', 1.0)
            
            factor_rows.append(factors)
        
        # Create DataFrame
        factors_df = pd.DataFrame(factor_rows)
        
        # Normalize factors
        normalized_df = factors_df.copy()
        
        # Define which factors to invert (lower is better)
        invert_factors = ['pe_ratio', 'forward_pe', 'pb_ratio', 'ps_ratio', 
                         'peg_ratio', 'ev_ebitda', 'debt_to_equity', 'beta']
        
        # Normalize each factor
        for col in factors_df.columns:
            if col in ['ticker', 'date']:
                continue
                
            # Handle the factor
            if col in invert_factors:
                # Invert first (handle zeros and negatives)
                values = factors_df[col]
                # Cap extreme values before inverting
                values = values.clip(lower=values.quantile(0.05), 
                                   upper=values.quantile(0.95))
                inverted = 1 / values.replace(0, np.nan)
                normalized_df[col] = self._cross_sectional_zscore(inverted)
            else:
                normalized_df[col] = self._cross_sectional_zscore(factors_df[col])
        
        return normalized_df.set_index('ticker')
    
    def _calculate_fcf_yield(self, info: Dict) -> float:
        """Calculate free cash flow yield"""
        fcf = info.get('freeCashflow', 0)
        market_cap = info.get('marketCap', 0)
        
        if market_cap > 0 and fcf is not None:
            return fcf / market_cap
        return np.nan
    
    def _cross_sectional_zscore(self, series: pd.Series) -> pd.Series:
        """Calculate cross-sectional z-score"""
        # Remove NaN values for calculation
        valid_data = series.dropna()
        
        if len(valid_data) < 3:  # Need at least 3 values
            return series
            
        mean = valid_data.mean()
        std = valid_data.std()
        
        if std == 0:
            return pd.Series(0, index=series.index)
            
        zscore = (series - mean) / std
        
        # Winsorize
        if self.config.winsorize_sigma > 0:
            zscore = zscore.clip(
                lower=-self.config.winsorize_sigma,
                upper=self.config.winsorize_sigma
            )
            
        return zscore
    
    def calculate_composite_scores(self, all_factors: pd.DataFrame) -> pd.DataFrame:
        """Calculate weighted composite scores"""
        scores = pd.DataFrame(index=all_factors.index)
        
        # Momentum composite
        momentum_factors = [col for col in all_factors.columns if 'momentum' in col]
        if momentum_factors:
            momentum_weights = [self.weights.momentum.get(f.split('_')[1], 0.25) 
                              for f in momentum_factors]
            scores['momentum_score'] = (all_factors[momentum_factors] * momentum_weights).sum(axis=1)
        
        # Value composite
        value_factors = ['pe_ratio', 'pb_ratio', 'ps_ratio', 'peg_ratio', 'ev_ebitda']
        value_factors = [f for f in value_factors if f in all_factors.columns]
        if value_factors:
            value_weights = [self.weights.value.get(f, 0.2) for f in value_factors]
            scores['value_score'] = (all_factors[value_factors] * value_weights).sum(axis=1)
        
        # Quality composite
        quality_factors = ['roe', 'roa', 'profit_margin', 'current_ratio', 'debt_to_equity']
        quality_factors = [f for f in quality_factors if f in all_factors.columns]
        if quality_factors:
            quality_weights = [self.weights.quality.get(f, 0.2) for f in quality_factors]
            scores['quality_score'] = (all_factors[quality_factors] * quality_weights).sum(axis=1)
        
        # Growth composite
        growth_factors = ['revenue_growth', 'earnings_growth']
        growth_factors = [f for f in growth_factors if f in all_factors.columns]
        if growth_factors:
            growth_weights = [self.weights.growth.get(f, 0.5) for f in growth_factors]
            scores['growth_score'] = (all_factors[growth_factors] * growth_weights).sum(axis=1)
        
        # Technical composite
        tech_factors = ['rsi_mean_reversion', 'macd_histogram', 'bb_position']
        tech_factors = [f for f in tech_factors if f in all_factors.columns]
        if tech_factors:
            scores['technical_score'] = all_factors[tech_factors].mean(axis=1)
        
        # Overall composite
        composite_factors = ['momentum_score', 'value_score', 'quality_score', 
                           'growth_score', 'technical_score']
        available_composites = [f for f in composite_factors if f in scores.columns]
        
        if available_composites:
            composite_weights = [self.weights.composite.get(f.replace('_score', ''), 0.2) 
                               for f in available_composites]
            scores['composite_score'] = (scores[available_composites] * composite_weights).sum(axis=1)
            
            # Normalize final score to 0-10 range
            scores['composite_score'] = self._normalize_to_range(scores['composite_score'], 0, 10)
        
        return scores
    
    def _normalize_to_range(self, series: pd.Series, min_val: float, max_val: float) -> pd.Series:
        """Normalize series to a specific range"""
        series_min = series.min()
        series_max = series.max()
        
        if series_max == series_min:
            return pd.Series(min_val + (max_val - min_val) / 2, index=series.index)
            
        normalized = (series - series_min) / (series_max - series_min)
        return normalized * (max_val - min_val) + min_val