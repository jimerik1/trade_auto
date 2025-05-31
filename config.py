# config.py
"""Configuration management for the stock factor analyzer"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class DataConfig:
    """Data fetching configuration"""
    cache_dir: str = "./data_cache"
    use_cache: bool = True
    cache_expiry_hours: int = 24
    batch_size: int = 10  # For async fetching
    adjust_prices: bool = True  # Use adjusted close prices
    
@dataclass
class FactorConfig:
    """Factor calculation configuration"""
    momentum_windows: List[int] = field(default_factory=lambda: [21, 63, 126, 252])
    volatility_windows: List[int] = field(default_factory=lambda: [30, 90])
    zscore_window: int = 252
    winsorize_sigma: float = 3.0
    min_data_points: int = 252  # Minimum days of data required
    
@dataclass
class FactorWeights:
    """Factor weights learned from historical data or set manually"""
    momentum: Dict[str, float] = field(default_factory=lambda: {
        '1m': 0.1,
        '3m': 0.3,
        '6m': 0.4,
        '12m': 0.2
    })
    value: Dict[str, float] = field(default_factory=lambda: {
        'pe_ratio': 0.3,
        'pb_ratio': 0.2,
        'ps_ratio': 0.2,
        'peg_ratio': 0.2,
        'ev_ebitda': 0.1
    })
    quality: Dict[str, float] = field(default_factory=lambda: {
        'roe': 0.3,
        'roa': 0.2,
        'profit_margin': 0.2,
        'current_ratio': 0.15,
        'debt_to_equity': 0.15
    })
    growth: Dict[str, float] = field(default_factory=lambda: {
        'revenue_growth': 0.5,
        'earnings_growth': 0.5
    })
    technical: Dict[str, float] = field(default_factory=lambda: {
        'rsi': 0.2,
        'price_to_sma20': 0.3,
        'price_to_sma50': 0.3,
        'volatility': 0.2
    })
    
    # Composite weights
    composite: Dict[str, float] = field(default_factory=lambda: {
        'value': 0.25,
        'momentum': 0.20,
        'quality': 0.25,
        'growth': 0.15,
        'technical': 0.15
    })

@dataclass
class BacktestConfig:
    """Backtesting configuration"""
    initial_capital: float = 1_000_000
    rebalance_frequency: str = "monthly"  # daily, weekly, monthly, quarterly
    transaction_cost: float = 0.001  # 10 bps
    slippage: float = 0.0005  # 5 bps
    max_position_size: float = 0.10  # 10% max per position
    min_position_size: float = 0.02  # 2% min per position
    benchmark: str = "SPY"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    risk_free_rate: float = 0.04  # 4% annual risk-free rate
    
@dataclass
class PortfolioConfig:
    """Portfolio construction configuration"""
    optimization_method: str = "equal_weight"  # equal_weight, risk_parity, mean_variance
    target_volatility: float = 0.15  # 15% annual volatility
    max_sector_weight: float = 0.30  # 30% max in any sector
    max_turnover: float = 0.50  # 50% monthly turnover limit
    risk_free_rate: float = 0.04  # 4% annual risk-free rate
    max_position_size: float = 0.10  # 10% max per position
    min_position_size: float = 0.02  # 2% min per position
    
@dataclass
class Config:
    """Master configuration"""
    data: DataConfig = field(default_factory=DataConfig)
    factors: FactorConfig = field(default_factory=FactorConfig)
    weights: FactorWeights = field(default_factory=FactorWeights)
    backtest: BacktestConfig = field(default_factory=BacktestConfig)
    portfolio: PortfolioConfig = field(default_factory=PortfolioConfig)
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = "factor_analyzer.log"
    
    @classmethod
    def from_dict(cls, config_dict: Dict) -> 'Config':
        """Create config from dictionary"""
        return cls(
            data=DataConfig(**config_dict.get('data', {})),
            factors=FactorConfig(**config_dict.get('factors', {})),
            weights=FactorWeights(**config_dict.get('weights', {})),
            backtest=BacktestConfig(**config_dict.get('backtest', {})),
            portfolio=PortfolioConfig(**config_dict.get('portfolio', {})),
            log_level=config_dict.get('log_level', 'INFO'),
            log_file=config_dict.get('log_file', 'factor_analyzer.log')
        )
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary"""
        return {
            'data': self.data.__dict__,
            'factors': self.factors.__dict__,
            'weights': {
                'momentum': self.weights.momentum,
                'value': self.weights.value,
                'quality': self.weights.quality,
                'growth': self.weights.growth,
                'technical': self.weights.technical,
                'composite': self.weights.composite
            },
            'backtest': self.backtest.__dict__,
            'portfolio': self.portfolio.__dict__,
            'log_level': self.log_level,
            'log_file': self.log_file
        }

# Default configuration
DEFAULT_CONFIG = Config()