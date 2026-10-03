import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Any
from src.config import settings

class ScenarioLoader:
    """
    Loads stress testing shock matrices from data/stress_scenarios.csv.
    """
    def __init__(self, csv_path: Path = None):
        self.csv_path = csv_path or settings.STRESS_SCENARIOS_PATH
        self.scenarios_df = self._load_scenarios()

    def _load_scenarios(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Stress scenarios file not found at {self.csv_path}")
        return pd.read_csv(self.csv_path)

    def get_scenario(self, event_type: str, impact_score: float) -> Optional[Dict[str, Any]]:
        """
        Retrieves stress testing parameters for a given event type.
        Returns scenario dict if impact_score >= min_impact (default 7.0), else None.
        """
        match = self.scenarios_df[self.scenarios_df["event_type"].str.upper() == event_type.upper()]
        if match.empty:
            match = self.scenarios_df[self.scenarios_df["event_type"].str.upper() == "OTHER"]
            
        row = match.iloc[0]
        min_impact = float(row["min_impact"])
        
        if impact_score < min_impact:
            return None  # Impact below threshold, no stress test triggered
            
        shocks = {
            "Equities": float(row["equity_shock_pct"]),
            "Bonds": float(row["bond_shock_pct"]),
            "Loans": float(row["loan_shock_pct"]),
            "Derivatives": float(row["derivative_shock_pct"])
        }
        
        return {
            "event_type": row["event_type"],
            "min_impact": min_impact,
            "description": row["description"],
            "assumptions": row["assumptions"],
            "shocks": shocks
        }
