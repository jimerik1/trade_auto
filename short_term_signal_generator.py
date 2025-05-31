# short_term_signal_generator.py
"""
Generate 1-week trade ideas based on short-term factors and recent ranking moves.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ShortTermSignalGenerator:
    def __init__(self, factor_calc, config):
        """
        factor_calc  : FactorCalculator – will be called with short-term config
        config       : SignalConfig
        """
        self.factor_calc = factor_calc
        self.cfg = config

    # ---------- Public API ----------
    def generate_signals(self, data: dict) -> pd.DataFrame:
        """
        Returns a DataFrame with columns:
        [ 'action', 'ticker', 'entry_price', 'stop', 'target', 'comment' ]
        """
        today = datetime.now().date()
        if today.strftime("%A") != self.cfg.scan_day:
            logger.info(f"Today is {today:%A}, skipping weekly scan.")
            return pd.DataFrame()

        prices = self._aligned_closes(data).iloc[-self.factor_calc.config.min_data_points:]
        if prices.empty:
            logger.warning("No price data for short-term scan.")
            return pd.DataFrame()

        # --- 1) compute short-term factors ---------------------------
        st_mom   = self.factor_calc.calculate_momentum_factors(prices)
        st_vol   = self.factor_calc.calculate_volatility_factors(prices)
        factors  = pd.concat([st_mom, st_vol], axis=1).dropna(how="all")

        # --- 2) latest composite scores ------------------------------
        # For short-term signals, we'll use a simpler scoring approach
        # Average the momentum and volatility z-scores
        
        # Debug: print DataFrame structure
        logger.info(f"Factors DataFrame shape: {factors.shape}")
        logger.info(f"Factors DataFrame columns (first 5): {list(factors.columns[:5]) if len(factors.columns) > 0 else 'No columns'}")
        logger.info(f"Factors DataFrame index (first 5): {factors.index[:5].tolist() if len(factors) > 0 else 'Empty'}")
        
        # Get latest values for each ticker
        latest_factors = factors.iloc[-1] if not factors.empty else pd.Series()
        logger.info(f"Latest factors shape: {latest_factors.shape if hasattr(latest_factors, 'shape') else 'N/A'}")
        
        # Group by ticker and calculate mean score
        ticker_scores = {}
        
        # Columns should be in format: factor_window_ticker (e.g., momentum_5d_AAPL)
        for col in factors.columns:
            col_str = str(col)
            
            # Extract ticker - it should be the last part after the last underscore
            parts = col_str.split('_')
            if len(parts) >= 3:  # e.g., momentum_5d_AAPL or volatility_20d_MSFT
                ticker = parts[-1]  # Last part is the ticker
                factor_type = '_'.join(parts[:-1])  # Everything else is the factor name
                logger.debug(f"Column: {col_str} -> Factor: {factor_type}, Ticker: {ticker}")
            else:
                logger.warning(f"Unexpected column format: {col_str}")
                continue
            
            # Ensure ticker exists in our price data
            if ticker not in prices.columns:
                logger.warning(f"Ticker {ticker} from factor column not found in price data")
                continue
                
            if ticker not in ticker_scores:
                ticker_scores[ticker] = []
            
            value = latest_factors[col]
            if pd.notna(value):  # Only add non-NaN values
                ticker_scores[ticker].append(value)
        
        logger.info(f"Extracted tickers: {list(ticker_scores.keys())}")
        logger.info(f"Score counts per ticker: {dict((t, len(s)) for t, s in ticker_scores.items())}")
        
        # Calculate mean score for each ticker
        latest = pd.Series({ticker: np.nanmean(scores) for ticker, scores in ticker_scores.items() if scores})
        latest = latest.sort_values(ascending=False)
        logger.info(f"Final composite scores (top 10):\n{latest.head(10)}")

        # --- 3) determine BUY / REDUCE -------------------------------
        top_new = latest.head(self.cfg.top_k).index
        bottom  = latest.tail(self.cfg.top_k).index

        signals = []
        for ticker in top_new:
            px = prices[ticker].iloc[-1]
            signals.append({
                "action"      : "BUY",
                "ticker"      : ticker,
                "entry_price" : px,
                "stop"        : round(px * (1 - self.cfg.stop_loss_pct), 2),
                "target"      : round(px * (1 + self.cfg.take_profit_pct), 2),
                "comment"     : "Entered weekly top-decile composite score"
            })

        for ticker in bottom:
            px = prices[ticker].iloc[-1]
            signals.append({
                "action"      : "SELL",
                "ticker"      : ticker,
                "entry_price" : px,
                "comment"     : "Dropped into bottom decile; consider trim / exit"
            })

        return pd.DataFrame(signals)

    # ---------- helpers ----------
    def _aligned_closes(self, data: dict) -> pd.DataFrame:
        close_dict = {t: d['prices']['Close'] for t, d in data.items() if 'prices' in d}
        return pd.DataFrame(close_dict).ffill(limit=2)