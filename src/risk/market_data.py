import json
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.config import settings

logger = logging.getLogger(__name__)

TRACKED_TICKERS = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "JPM", "V", "NFLX"]

class MarketDataProvider:
    """
    Public market intelligence provider using yfinance.
    Tracks 10 major benchmark equities, calculates annualized volatility and returns,
    and maintains offline fallback cache.
    """
    
    def __init__(self, cache_path: Optional[Path] = None):
        self.cache_path = cache_path or (settings.DATA_DIR / "market_cache.json")
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict[str, Any]:
        if self.cache_path.exists():
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to read market cache: {e}")
        return {}

    def get_ticker_metrics(self, ticker: str, use_live: bool = False) -> Dict[str, Any]:
        """
        Retrieves market metrics for a single ticker.
        If use_live=True, tries yfinance; otherwise falls back gracefully to cached data.
        """
        ticker = ticker.upper()
        
        if use_live:
            try:
                import yfinance as yf
                t = yf.Ticker(ticker)
                hist = t.history(period="1mo")
                if not hist.empty and len(hist) > 5:
                    latest_price = float(hist["Close"].iloc[-1])
                    prev_close = float(hist["Close"].iloc[-2])
                    change_pct = round(((latest_price - prev_close) / prev_close) * 100.0, 2)
                    
                    # Daily returns & annualized volatility (252 trading days)
                    daily_returns = hist["Close"].pct_change().dropna()
                    daily_vol = float(daily_returns.std())
                    ann_vol = round(daily_vol * np.sqrt(252) * 100.0, 2)
                    
                    info = t.info or {}
                    return {
                        "ticker": ticker,
                        "company_name": info.get("shortName", ticker),
                        "current_price": round(latest_price, 2),
                        "previous_close": round(prev_close, 2),
                        "change_pct": change_pct,
                        "currency": info.get("currency", "USD"),
                        "annualized_volatility_pct": ann_vol,
                        "high_52w": info.get("fiftyTwoWeekHigh", round(latest_price * 1.15, 2)),
                        "low_52w": info.get("fiftyTwoWeekLow", round(latest_price * 0.75, 2)),
                        "market_cap": str(info.get("marketCap", "N/A")),
                        "pe_ratio": round(float(info.get("trailingPE", 25.0)), 1)
                    }
            except Exception as e:
                logger.warning(f"Live yfinance query for {ticker} failed: {e}. Falling back to cached market intelligence.")

        # Fallback to local cache
        if ticker in self.cache:
            return self.cache[ticker]
            
        # Default placeholder if unlisted
        return {
            "ticker": ticker,
            "company_name": ticker,
            "current_price": 100.0,
            "previous_close": 100.0,
            "change_pct": 0.0,
            "currency": "USD",
            "annualized_volatility_pct": 20.0,
            "high_52w": 120.0,
            "low_52w": 80.0,
            "market_cap": "N/A",
            "pe_ratio": 20.0
        }

    def get_all_tracked_metrics(self, use_live: bool = False) -> List[Dict[str, Any]]:
        """Retrieves metrics for all 10 tracked companies."""
        return [self.get_ticker_metrics(t, use_live=use_live) for t in TRACKED_TICKERS]
