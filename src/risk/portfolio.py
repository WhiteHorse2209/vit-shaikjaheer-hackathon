import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
from src.config import settings

class PortfolioManager:
    """
    Manages the synthetic multi-asset portfolio:
    Equities (₹40M), Bonds (₹25M), Loans (₹20M), Derivatives (₹15M) = Total ₹100M.
    """
    
    def __init__(self, csv_path: Path = None):
        self.csv_path = csv_path or settings.PORTFOLIO_PATH
        self.df = self._load_portfolio()

    def _load_portfolio(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Portfolio file not found at {self.csv_path}")
        df = pd.read_csv(self.csv_path)
        # Ensure numerical base value
        df["base_value"] = pd.to_numeric(df["base_value"])
        return df

    def get_total_value(self) -> float:
        """Returns aggregate base portfolio value."""
        return float(self.df["base_value"].sum())

    def get_asset_class_breakdown(self) -> Dict[str, Dict[str, float]]:
        """Returns value and percentage share per asset class."""
        total = self.get_total_value()
        grouped = self.df.groupby("asset_class")["base_value"].sum().to_dict()
        breakdown = {}
        for ac, val in grouped.items():
            breakdown[ac] = {
                "base_value": float(val),
                "weight_pct": round((float(val) / total) * 100, 2)
            }
        return breakdown

    def get_holdings(self) -> List[Dict[str, Any]]:
        """Returns complete list of individual instruments."""
        return self.df.to_dict(orient="records")

    def simulate_stress_shock(self, asset_shocks_pct: Dict[str, float]) -> Dict[str, Any]:
        """
        Applies percentage shocks to each asset class.
        asset_shocks_pct: e.g. {'Equities': -10.0, 'Bonds': -5.0, 'Loans': -3.0, 'Derivatives': -12.0}
        Returns comprehensive impact calculation before and after.
        """
        asset_breakdown = {}
        total_before = 0.0
        total_after = 0.0

        for ac, info in self.get_asset_class_breakdown().items():
            base_val = info["base_value"]
            # Look up shock (case-insensitive)
            shock_pct = 0.0
            for k, v in asset_shocks_pct.items():
                if k.lower() in ac.lower() or ac.lower() in k.lower():
                    shock_pct = float(v)
                    break
                    
            delta = base_val * (shock_pct / 100.0)
            stressed_val = base_val + delta

            asset_breakdown[ac] = {
                "base_value": round(base_val, 2),
                "shock_pct": round(shock_pct, 2),
                "loss_value": round(abs(delta) if delta < 0 else -delta, 2),
                "stressed_value": round(stressed_val, 2)
            }
            total_before += base_val
            total_after += stressed_val

        simulated_loss = round(total_before - total_after, 2)
        loss_pct = round((simulated_loss / total_before) * 100.0, 2)

        return {
            "portfolio_before": round(total_before, 2),
            "portfolio_after": round(total_after, 2),
            "simulated_loss": simulated_loss,
            "loss_pct": loss_pct,
            "asset_breakdown": asset_breakdown
        }
