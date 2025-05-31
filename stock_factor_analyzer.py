# stock_factor_analyzer.py

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import talib
import warnings
warnings.filterwarnings('ignore')

class StockFactorAnalyzer:
    def __init__(self, tickers, period='2y'):
        """
        Initialize the analyzer with stock tickers and data period
        
        Args:
            tickers: List of stock symbols
            period: Data period ('1y', '2y', '5y', 'max')
        """
        self.tickers = tickers
        self.period = period
        self.data = {}
        self.factor_scores = pd.DataFrame()
        
    def fetch_data(self):
        """Fetch historical data and company info for all tickers"""
        print("Fetching data...")
        
        for ticker in self.tickers:
            try:
                stock = yf.Ticker(ticker)
                
                # Get historical price data
                hist_data = stock.history(period=self.period)
                
                # Get company info
                info = stock.info
                
                # Get financials
                financials = stock.financials
                balance_sheet = stock.balance_sheet
                
                self.data[ticker] = {
                    'history': hist_data,
                    'info': info,
                    'financials': financials,
                    'balance_sheet': balance_sheet
                }
                
                print(f"✓ Fetched data for {ticker}")
                
            except Exception as e:
                print(f"✗ Error fetching {ticker}: {e}")
                
    def calculate_technical_factors(self, ticker):
        """Calculate technical analysis factors"""
        try:
            hist = self.data[ticker]['history']
            close = hist['Close'].values
            high = hist['High'].values
            low = hist['Low'].values
            volume = hist['Volume'].values
            
            factors = {}
            
            # Price momentum factors
            factors['momentum_1m'] = (close[-1] / close[-21] - 1) * 100 if len(close) > 21 else 0
            factors['momentum_3m'] = (close[-1] / close[-63] - 1) * 100 if len(close) > 63 else 0
            factors['momentum_6m'] = (close[-1] / close[-126] - 1) * 100 if len(close) > 126 else 0
            factors['momentum_12m'] = (close[-1] / close[-252] - 1) * 100 if len(close) > 252 else 0
            
            # Volatility
            returns = pd.Series(close).pct_change().dropna()
            factors['volatility_30d'] = returns.tail(30).std() * np.sqrt(252) * 100
            factors['volatility_90d'] = returns.tail(90).std() * np.sqrt(252) * 100
            
            # Technical indicators
            factors['rsi'] = talib.RSI(close)[-1] if len(close) > 14 else 50
            factors['macd_signal'] = 1 if talib.MACD(close)[0][-1] > talib.MACD(close)[1][-1] else 0
            
            # Moving average ratios
            sma_20 = talib.SMA(close, 20)[-1] if len(close) > 20 else close[-1]
            sma_50 = talib.SMA(close, 50)[-1] if len(close) > 50 else close[-1]
            factors['price_to_sma20'] = (close[-1] / sma_20 - 1) * 100
            factors['price_to_sma50'] = (close[-1] / sma_50 - 1) * 100
            
            # Volume analysis
            avg_volume_30d = np.mean(volume[-30:]) if len(volume) > 30 else np.mean(volume)
            factors['volume_ratio'] = volume[-1] / avg_volume_30d if avg_volume_30d > 0 else 1
            
            return factors
            
        except Exception as e:
            print(f"Error calculating technical factors for {ticker}: {e}")
            return {}
    
    def calculate_fundamental_factors(self, ticker):
        """Calculate fundamental analysis factors"""
        try:
            info = self.data[ticker]['info']
            factors = {}
            
            # Valuation ratios
            factors['pe_ratio'] = info.get('trailingPE', 0)
            factors['pb_ratio'] = info.get('priceToBook', 0)
            factors['ps_ratio'] = info.get('priceToSalesTrailing12Months', 0)
            factors['peg_ratio'] = info.get('pegRatio', 0)
            factors['ev_ebitda'] = info.get('enterpriseToEbitda', 0)
            
            # Profitability ratios
            factors['roe'] = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0
            factors['roa'] = info.get('returnOnAssets', 0) * 100 if info.get('returnOnAssets') else 0
            factors['profit_margin'] = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0
            factors['operating_margin'] = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else 0
            
            # Growth metrics
            factors['revenue_growth'] = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0
            factors['earnings_growth'] = info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else 0
            
            # Financial strength
            factors['debt_to_equity'] = info.get('debtToEquity', 0)
            factors['current_ratio'] = info.get('currentRatio', 0)
            factors['quick_ratio'] = info.get('quickRatio', 0)
            
            # Market metrics
            factors['market_cap'] = info.get('marketCap', 0) / 1e9  # in billions
            factors['enterprise_value'] = info.get('enterpriseValue', 0) / 1e9  # in billions
            
            return factors
            
        except Exception as e:
            print(f"Error calculating fundamental factors for {ticker}: {e}")
            return {}
    
    def calculate_quality_factors(self, ticker):
        """Calculate quality factors"""
        try:
            info = self.data[ticker]['info']
            factors = {}
            
            # Stability metrics
            factors['beta'] = info.get('beta', 1)
            factors['dividend_yield'] = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
            
            # Analyst sentiment
            factors['recommendation_score'] = info.get('recommendationMean', 3)  # 1=Strong Buy, 5=Strong Sell
            factors['target_price_upside'] = 0
            if info.get('targetMeanPrice') and info.get('currentPrice'):
                factors['target_price_upside'] = (info['targetMeanPrice'] / info['currentPrice'] - 1) * 100
            
            return factors
            
        except Exception as e:
            print(f"Error calculating quality factors for {ticker}: {e}")
            return {}
    
    def score_factors(self, factors_df):
        """Score factors on a 1-10 scale"""
        scored_df = factors_df.copy()
        
        # Define scoring rules for each factor
        scoring_rules = {
            # Momentum factors (higher is better)
            'momentum_1m': 'percentile',
            'momentum_3m': 'percentile', 
            'momentum_6m': 'percentile',
            'momentum_12m': 'percentile',
            
            # Valuation factors (lower is better for most)
            'pe_ratio': 'inverse_percentile_capped',
            'pb_ratio': 'inverse_percentile_capped',
            'ps_ratio': 'inverse_percentile_capped',
            'peg_ratio': 'inverse_percentile_capped',
            'ev_ebitda': 'inverse_percentile_capped',
            
            # Profitability (higher is better)
            'roe': 'percentile',
            'roa': 'percentile',
            'profit_margin': 'percentile',
            'operating_margin': 'percentile',
            'revenue_growth': 'percentile',
            'earnings_growth': 'percentile',
            
            # Financial strength
            'debt_to_equity': 'inverse_percentile_capped',
            'current_ratio': 'percentile',
            'quick_ratio': 'percentile',
            
            # Technical factors
            'rsi': 'mean_reversion',  # 50 is optimal
            'volatility_30d': 'inverse_percentile',
            'price_to_sma20': 'momentum_bias',
            'price_to_sma50': 'momentum_bias',
            
            # Quality factors
            'dividend_yield': 'percentile',
            'recommendation_score': 'inverse_percentile',
            'target_price_upside': 'percentile',
        }
        
        for factor, rule in scoring_rules.items():
            if factor in scored_df.columns:
                scored_df[f'{factor}_score'] = self.apply_scoring_rule(factors_df[factor], rule)
        
        return scored_df
    
    def apply_scoring_rule(self, series, rule):
        """Apply different scoring rules"""
        series = series.replace([np.inf, -np.inf], np.nan)
        
        if rule == 'percentile':
            return pd.qcut(series.rank(method='first'), 10, labels=range(1, 11)).astype(float)
        
        elif rule == 'inverse_percentile':
            return pd.qcut((-series).rank(method='first'), 10, labels=range(1, 11)).astype(float)
        
        elif rule == 'inverse_percentile_capped':
            # Cap extreme values before inverse ranking
            capped = series.clip(upper=series.quantile(0.95))
            return pd.qcut((-capped).rank(method='first'), 10, labels=range(1, 11)).astype(float)
        
        elif rule == 'mean_reversion':
            # For RSI - score higher when closer to 50
            distance_from_50 = np.abs(series - 50)
            return pd.qcut((-distance_from_50).rank(method='first'), 10, labels=range(1, 11)).astype(float)
        
        elif rule == 'momentum_bias':
            # Slight bias toward positive momentum
            adjusted = series + 2  # small positive bias
            return pd.qcut(adjusted.rank(method='first'), 10, labels=range(1, 11)).astype(float)
        
        else:
            return pd.Series([5] * len(series), index=series.index)  # neutral score
    
    def calculate_composite_scores(self, scored_df):
        """Calculate composite factor scores"""
        score_columns = [col for col in scored_df.columns if col.endswith('_score')]
        
        # Define factor groups with weights
        factor_groups = {
            'value_score': {
                'pe_ratio_score': 0.3,
                'pb_ratio_score': 0.2,
                'ps_ratio_score': 0.2,
                'peg_ratio_score': 0.2,
                'ev_ebitda_score': 0.1
            },
            'momentum_score': {
                'momentum_1m_score': 0.1,
                'momentum_3m_score': 0.3,
                'momentum_6m_score': 0.4,
                'momentum_12m_score': 0.2
            },
            'quality_score': {
                'roe_score': 0.3,
                'roa_score': 0.2,
                'profit_margin_score': 0.2,
                'current_ratio_score': 0.15,
                'debt_to_equity_score': 0.15
            },
            'growth_score': {
                'revenue_growth_score': 0.5,
                'earnings_growth_score': 0.5
            },
            'technical_score': {
                'rsi_score': 0.2,
                'price_to_sma20_score': 0.3,
                'price_to_sma50_score': 0.3,
                'volatility_30d_score': 0.2
            }
        }
        
        # Calculate composite scores
        for composite_name, factors in factor_groups.items():
            weighted_score = 0
            total_weight = 0
            
            for factor, weight in factors.items():
                if factor in scored_df.columns:
                    weighted_score += scored_df[factor].fillna(5) * weight
                    total_weight += weight
            
            if total_weight > 0:
                scored_df[composite_name] = weighted_score / total_weight
        
        # Overall composite score
        composite_cols = ['value_score', 'momentum_score', 'quality_score', 'growth_score', 'technical_score']
        available_composites = [col for col in composite_cols if col in scored_df.columns]
        
        if available_composites:
            scored_df['overall_score'] = scored_df[available_composites].mean(axis=1)
        
        return scored_df
    
    def analyze_stocks(self):
        """Main analysis function"""
        print("Starting factor analysis...")
        
        # Fetch data
        self.fetch_data()
        
        if not self.data:
            print("No data available for analysis")
            return None
        
        # Calculate factors for each stock
        all_factors = {}
        
        for ticker in self.data.keys():
            print(f"Analyzing {ticker}...")
            
            factors = {}
            factors.update(self.calculate_technical_factors(ticker))
            factors.update(self.calculate_fundamental_factors(ticker))
            factors.update(self.calculate_quality_factors(ticker))
            
            all_factors[ticker] = factors
        
        # Create DataFrame
        factors_df = pd.DataFrame(all_factors).T
        
        # Score factors
        scored_df = self.score_factors(factors_df)
        
        # Calculate composite scores
        final_df = self.calculate_composite_scores(scored_df)
        
        self.factor_scores = final_df
        
        return final_df
    
    def get_rankings(self, sort_by='overall_score', top_n=10):
        """Get top ranked stocks"""
        if self.factor_scores.empty:
            print("No analysis completed yet. Run analyze_stocks() first.")
            return None
        
        rankings = self.factor_scores.sort_values(sort_by, ascending=False)
        
        # Select key columns for display
        display_cols = ['overall_score', 'value_score', 'momentum_score', 'quality_score', 'growth_score', 'technical_score']
        available_cols = [col for col in display_cols if col in rankings.columns]
        
        return rankings[available_cols].head(top_n).round(2)
    
    def get_detailed_analysis(self, ticker):
        """Get detailed factor breakdown for a specific stock"""
        if ticker not in self.factor_scores.index:
            print(f"No data available for {ticker}")
            return None
        
        stock_data = self.factor_scores.loc[ticker]
        
        # Organize by factor categories
        result = {
            'Overall Score': stock_data.get('overall_score', 'N/A'),
            'Composite Scores': {
                'Value': stock_data.get('value_score', 'N/A'),
                'Momentum': stock_data.get('momentum_score', 'N/A'),
                'Quality': stock_data.get('quality_score', 'N/A'),
                'Growth': stock_data.get('growth_score', 'N/A'),
                'Technical': stock_data.get('technical_score', 'N/A')
            }
        }
        
        return result


# Example usage
if __name__ == "__main__":
    # Import tickers from the companies file
    from companies import TICKERS
    
    # Initialize analyzer
    analyzer = StockFactorAnalyzer(TICKERS, period='2y')
    
    # Run analysis
    results = analyzer.analyze_stocks()
    
    if results is not None:
        print("\n" + "="*50)
        print("TOP 10 RANKED STOCKS")
        print("="*50)
        print(analyzer.get_rankings(top_n=10))
        
        print("\n" + "="*50)
        print("DETAILED BREAKDOWN FOR TOP STOCK")
        print("="*50)
        top_stock = analyzer.get_rankings(top_n=1).index[0]
        detailed_analysis = analyzer.get_detailed_analysis(top_stock)
        
        print(f"\nStock: {top_stock}")
        print(f"Overall Score: {detailed_analysis['Overall Score']:.2f}")
        print("\nComposite Scores:")
        for category, score in detailed_analysis['Composite Scores'].items():
            if score != 'N/A':
                print(f"  {category}: {score:.2f}")