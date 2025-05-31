# portfolio_optimizer.py
"""Portfolio optimization and construction"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from scipy.optimize import minimize
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform

from config import PortfolioConfig

logger = logging.getLogger(__name__)

class PortfolioOptimizer:
    """Portfolio optimization using various methods"""
    
    def __init__(self, config: PortfolioConfig):
        self.config = config
        
    def optimize_portfolio(self, expected_returns: pd.Series, 
                         covariance_matrix: pd.DataFrame,
                         current_weights: Optional[pd.Series] = None) -> pd.Series:
        """Main portfolio optimization function"""
        
        if self.config.optimization_method == "equal_weight":
            return self._equal_weight(expected_returns)
        elif self.config.optimization_method == "risk_parity":
            return self._risk_parity(covariance_matrix)
        elif self.config.optimization_method == "mean_variance":
            return self._mean_variance(expected_returns, covariance_matrix)
        elif self.config.optimization_method == "hierarchical_risk_parity":
            return self._hierarchical_risk_parity(covariance_matrix)
        else:
            logger.warning(f"Unknown optimization method: {self.config.optimization_method}")
            return self._equal_weight(expected_returns)
    
    def _equal_weight(self, expected_returns: pd.Series) -> pd.Series:
        """Simple equal weighting"""
        n_assets = len(expected_returns)
        weights = pd.Series(1.0 / n_assets, index=expected_returns.index)
        return self._apply_constraints(weights)
    
    def _risk_parity(self, covariance_matrix: pd.DataFrame) -> pd.Series:
        """Risk parity optimization"""
        n_assets = len(covariance_matrix)
        
        # Initial guess
        x0 = np.ones(n_assets) / n_assets
        
        # Objective function: minimize difference in risk contributions
        def objective(weights):
            portfolio_vol = np.sqrt(weights @ covariance_matrix @ weights)
            marginal_contrib = covariance_matrix @ weights
            contrib = weights * marginal_contrib / portfolio_vol
            
            # Target equal risk contribution
            target_contrib = 1.0 / n_assets
            return np.sum((contrib - target_contrib) ** 2)
        
        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0},  # Sum to 1
        ]
        
        # Bounds
        bounds = [(0, self.config.max_position_size) for _ in range(n_assets)]
        
        # Optimize
        result = minimize(objective, x0, method='SLSQP', 
                         bounds=bounds, constraints=constraints)
        
        if result.success:
            weights = pd.Series(result.x, index=covariance_matrix.index)
            return self._apply_constraints(weights)
        else:
            logger.warning("Risk parity optimization failed, using equal weight")
            return self._equal_weight(pd.Series(index=covariance_matrix.index))
    
    def _mean_variance(self, expected_returns: pd.Series, 
                      covariance_matrix: pd.DataFrame) -> pd.Series:
        """Mean-variance optimization with target volatility"""
        n_assets = len(expected_returns)
        
        # Initial guess
        x0 = np.ones(n_assets) / n_assets
        
        # Target return (can be adjusted)
        target_return = expected_returns.mean()
        
        # Objective: minimize portfolio variance
        def objective(weights):
            return weights @ covariance_matrix @ weights
        
        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0},  # Sum to 1
            {'type': 'ineq', 'fun': lambda x: x @ expected_returns - target_return}  # Min return
        ]
        
        # Add volatility constraint if specified
        if self.config.target_volatility > 0:
            constraints.append({
                'type': 'ineq', 
                'fun': lambda x: self.config.target_volatility**2 - x @ covariance_matrix @ x
            })
        
        # Bounds
        bounds = [(0, self.config.max_position_size) for _ in range(n_assets)]
        
        # Optimize
        result = minimize(objective, x0, method='SLSQP', 
                         bounds=bounds, constraints=constraints)
        
        if result.success:
            weights = pd.Series(result.x, index=expected_returns.index)
            return self._apply_constraints(weights)
        else:
            logger.warning("Mean-variance optimization failed, using equal weight")
            return self._equal_weight(expected_returns)
    
    def _hierarchical_risk_parity(self, covariance_matrix: pd.DataFrame) -> pd.Series:
        """Hierarchical Risk Parity (HRP) optimization"""
        # Convert covariance to correlation
        std = np.sqrt(np.diag(covariance_matrix))
        corr_matrix = covariance_matrix / np.outer(std, std)
        
        # Distance matrix
        dist_matrix = np.sqrt(2 * (1 - corr_matrix))
        
        # Hierarchical clustering
        linkage_matrix = linkage(squareform(dist_matrix), method='single')
        
        # Get sorted order
        sorted_idx = self._get_quasi_diag(linkage_matrix)
        sorted_tickers = corr_matrix.index[sorted_idx].tolist()
        
        # Recursive bisection
        weights = self._recursive_bisection(
            covariance_matrix.loc[sorted_tickers, sorted_tickers]
        )
        
        # Return weights in original order
        return self._apply_constraints(weights.loc[covariance_matrix.index])
    
    def _get_quasi_diag(self, link):
        """Get quasi-diagonal ordering from linkage matrix"""
        link = link.astype(int)
        sorted_idx = []
        clusters = {i: [i] for i in range(link.shape[0] + 1)}
        
        for i in range(link.shape[0]):
            cluster1 = int(link[i, 0])
            cluster2 = int(link[i, 1])
            
            # Form new cluster
            new_cluster = clusters[cluster1] + clusters[cluster2]
            clusters[link.shape[0] + i + 1] = new_cluster
            
            # Remove old clusters
            del clusters[cluster1]
            del clusters[cluster2]
        
        # Get final ordering
        sorted_idx = list(clusters.values())[0]
        return sorted_idx
    
    def _recursive_bisection(self, cov: pd.DataFrame) -> pd.Series:
        """Recursive bisection for HRP"""
        weights = pd.Series(1.0, index=cov.index)
        clusters = [cov.index.tolist()]
        
        while len(clusters) > 0:
            clusters = [c[1:] + [c[0]] for c in clusters]  # rotate
            
            cluster = clusters.pop()
            if len(cluster) > 1:
                # Split into two sub-clusters
                n = len(cluster) // 2
                left = cluster[:n]
                right = cluster[n:]
                
                # Calculate variance of each sub-cluster
                var_left = self._get_cluster_var(cov.loc[left, left])
                var_right = self._get_cluster_var(cov.loc[right, right])
                
                # Allocate weights inversely proportional to variance
                alpha = 1 - var_left / (var_left + var_right)
                
                weights[left] *= alpha
                weights[right] *= (1 - alpha)
                
                clusters.append(left)
                clusters.append(right)
        
        return weights
    
    def _get_cluster_var(self, cov: pd.DataFrame) -> float:
        """Calculate variance of a cluster using inverse variance weighting"""
        ivp = 1 / np.diag(cov)
        ivp /= ivp.sum()
        return np.sqrt(ivp @ cov @ ivp)
    
    def _apply_constraints(self, weights: pd.Series) -> pd.Series:
        """Apply position size constraints"""
        # Apply max position size
        weights = weights.clip(upper=self.config.max_position_size)
        
        # Apply min position size (set to 0 if below minimum)
        weights[weights < self.config.min_position_size] = 0
        
        # Renormalize
        if weights.sum() > 0:
            weights = weights / weights.sum()
        else:
            # Fallback to equal weight
            n_assets = len(weights)
            weights = pd.Series(1.0 / n_assets, index=weights.index)
        
        return weights
    
    def apply_sector_constraints(self, weights: pd.Series, 
                               sector_mapping: Dict[str, str]) -> pd.Series:
        """Apply sector concentration limits"""
        if not sector_mapping:
            return weights
            
        # Calculate sector weights
        sector_weights = {}
        for ticker, weight in weights.items():
            sector = sector_mapping.get(ticker, 'Unknown')
            sector_weights[sector] = sector_weights.get(sector, 0) + weight
        
        # Check if any sector exceeds limit
        needs_rebalancing = False
        for sector, sector_weight in sector_weights.items():
            if sector_weight > self.config.max_sector_weight:
                needs_rebalancing = True
                break
        
        if not needs_rebalancing:
            return weights
        
        # Rebalance by scaling down overweight sectors
        adjusted_weights = weights.copy()
        
        for sector, sector_weight in sector_weights.items():
            if sector_weight > self.config.max_sector_weight:
                # Scale down all positions in this sector
                scale_factor = self.config.max_sector_weight / sector_weight
                
                for ticker, weight in weights.items():
                    if sector_mapping.get(ticker) == sector:
                        adjusted_weights[ticker] *= scale_factor
        
        # Renormalize
        return adjusted_weights / adjusted_weights.sum()
    
    def calculate_turnover(self, new_weights: pd.Series, 
                          current_weights: pd.Series) -> float:
        """Calculate portfolio turnover"""
        # Align indices
        all_tickers = new_weights.index.union(current_weights.index)
        new_aligned = new_weights.reindex(all_tickers, fill_value=0)
        current_aligned = current_weights.reindex(all_tickers, fill_value=0)
        
        # Calculate turnover (sum of absolute changes / 2)
        turnover = np.abs(new_aligned - current_aligned).sum() / 2
        
        return turnover
    
    def apply_turnover_constraint(self, new_weights: pd.Series,
                                 current_weights: pd.Series) -> pd.Series:
        """Apply turnover constraint"""
        if current_weights is None or current_weights.empty:
            return new_weights
            
        turnover = self.calculate_turnover(new_weights, current_weights)
        
        if turnover <= self.config.max_turnover:
            return new_weights
        
        # Scale back changes to meet turnover constraint
        logger.info(f"Turnover {turnover:.1%} exceeds limit {self.config.max_turnover:.1%}, scaling back")
        
        # Blend old and new weights
        blend_factor = self.config.max_turnover / turnover
        
        all_tickers = new_weights.index.union(current_weights.index)
        blended_weights = pd.Series(index=all_tickers, dtype=float)
        
        for ticker in all_tickers:
            old_weight = current_weights.get(ticker, 0)
            new_weight = new_weights.get(ticker, 0)
            
            if old_weight > new_weight:
                # Selling
                blended_weights[ticker] = old_weight - blend_factor * (old_weight - new_weight)
            else:
                # Buying
                blended_weights[ticker] = old_weight + blend_factor * (new_weight - old_weight)
        
        # Renormalize
        blended_weights = blended_weights[blended_weights > 0]
        return blended_weights / blended_weights.sum()
    
    def get_portfolio_metrics(self, weights: pd.Series, 
                            expected_returns: pd.Series,
                            covariance_matrix: pd.DataFrame) -> Dict:
        """Calculate portfolio metrics"""
        # Align data
        tickers = weights.index
        weights_aligned = weights.loc[tickers]
        returns_aligned = expected_returns.loc[tickers]
        cov_aligned = covariance_matrix.loc[tickers, tickers]
        
        # Portfolio return
        portfolio_return = weights_aligned @ returns_aligned
        
        # Portfolio volatility
        portfolio_variance = weights_aligned @ cov_aligned @ weights_aligned
        portfolio_volatility = np.sqrt(portfolio_variance)
        
        # Sharpe ratio
        sharpe_ratio = (portfolio_return - self.config.risk_free_rate) / portfolio_volatility
        
        # Risk contributions
        marginal_contrib = cov_aligned @ weights_aligned
        total_contrib = weights_aligned @ marginal_contrib
        risk_contrib = weights_aligned * marginal_contrib / np.sqrt(total_contrib)
        
        # Concentration metrics
        effective_n = 1 / (weights_aligned ** 2).sum()  # Effective number of assets
        max_weight = weights_aligned.max()
        
        return {
            'expected_return': portfolio_return,
            'volatility': portfolio_volatility,
            'sharpe_ratio': sharpe_ratio,
            'risk_contributions': risk_contrib.to_dict(),
            'effective_n_assets': effective_n,
            'max_weight': max_weight,
            'n_positions': (weights_aligned > 0).sum()
        }