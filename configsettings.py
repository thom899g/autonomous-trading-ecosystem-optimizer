"""
Configuration and environment settings for the Autonomous Trading Ecosystem Optimizer.
Centralizes all configuration to ensure consistency and security.
"""
import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import logging

class TradingPlatform(Enum):
    """Supported trading platforms for ecosystem optimization."""
    BINANCE = "binance"
    COINBASE = "coinbase"
    KRAKEN = "kraken"
    FTX = "ftx"
    DERIBIT = "deribit"

@dataclass
class FirebaseConfig:
    """Firebase configuration for real-time state management."""
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "trading-ecosystem-optimizer")
    credentials_path: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "./config/firebase-creds.json")
    
    # Collections
    collections = {
        "market_states": "market_synthesis_states",
        "performance_metrics": "historical_performance",
        "allocations": "resource_allocations",
        "system_logs": "ecosystem_logs"
    }

@dataclass
class DataSynthesisConfig:
    """Configuration for market signal synthesis."""
    # Time windows for analysis
    windows_seconds: List[int] = (300, 900, 3600, 7200, 21600)  # 5m, 15m, 1h, 2h, 6h
    volatility_lookback: int = 100  # periods for volatility calculation
    correlation_threshold: float = 0.7
    min_liquidity_usd: float = 10000.0
    
    # Feature generation parameters
    n_components_pca: int = 5
    cluster_count: int = 8

@dataclass
class RiskConfig:
    """Risk management configuration."""
    max_allocation_per_platform: float = 0.25  # 25% max to any single platform
    max_drawdown_threshold: float = 0.15  # 15% max drawdown
    var_confidence_level: float = 0.95
    max_correlation_exposure: float = 0.6

class Settings:
    """Main configuration singleton."""
    
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug_mode = self.environment == "development"
        
        # Component configurations
        self.firebase = FirebaseConfig()
        self.data_synthesis = DataSynthesisConfig()
        self.risk = RiskConfig()
        
        # Platform configuration
        self.enabled_platforms: List[TradingPlatform] = [
            TradingPlatform.BINANCE,
            TradingPlatform.COINBASE,
            TradingPlatform.KRAKEN
        ]
        
        # Performance tracking
        self.metrics_update_interval_sec: int = 60
        self.reallocation_check_interval_sec: int = 300
        
        # Logging configuration
        self.log_level = logging.DEBUG if self.debug_mode else logging.INFO
        
    def validate(self) -> bool:
        """Validate all configuration parameters."""
        try:
            assert 0 < self.risk.max_allocation_per_platform <= 1.0
            assert 0 < self.risk.max_drawdown_threshold < 1.0
            assert 0.5 <= self.risk.var_confidence_level < 1.0
            assert len(self.enabled_platforms) >= 2, "Need at least 2 platforms for optimization"
            
            # Check Firebase credentials exist
            if os.path.exists(self.firebase.credentials_path):
                logging.info(f"Firebase credentials found at {self.firebase.credentials_path}")
            else:
                logging.warning(f"Firebase credentials not found at {self.firebase.credentials_path}")
            
            return True
        except (AssertionError, Exception) as e:
            logging.error(f"Configuration validation failed: {e}")
            return False

# Global settings instance
settings = Settings()