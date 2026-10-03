import json
import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from src.config import settings
from src.nlp.models import RiskSignal
from src.risk.portfolio import PortfolioManager
from src.risk.scenario_loader import ScenarioLoader
from src.database.db import SessionLocal, StressTestRunDB, init_db

logger = logging.getLogger(__name__)

class StressTestResult(BaseModel):
    run_id: str = Field(description="Unique execution identifier for audit trail")
    article_id: Optional[str] = None
    company: str
    ticker: str
    event_type: str
    impact_score: float
    sentiment_score: float
    triggered: bool
    trigger_reason: str
    portfolio_before: float
    portfolio_after: float
    simulated_loss: float
    loss_pct: float
    asset_breakdown: Dict[str, Any]
    scenario_description: str
    simulation_assumptions: str
    disclaimer: str
    created_at: str

class StressTestEngine:
    """
    Strategic Portfolio Stress Testing Engine (Module B).
    
    Workflow:
    Risk Signal -> Check Impact Score -> If > 7.0 -> Identify Event Type ->
    Load Predefined Scenario -> Apply Asset-Level Shocks -> Compute Valuation & Loss ->
    Record Audit Trail & History.
    """
    
    def __init__(self, portfolio_manager: Optional[PortfolioManager] = None, scenario_loader: Optional[ScenarioLoader] = None):
        init_db()
        self.portfolio_mgr = portfolio_manager or PortfolioManager()
        self.scenario_loader = scenario_loader or ScenarioLoader()

    def evaluate_signal(self, signal: RiskSignal, persist: bool = True) -> StressTestResult:
        """
        Evaluates a single risk signal. If impact > 7.0, executes stress test simulation.
        """
        is_triggered = signal.impact_score > settings.IMPACT_THRESHOLD_TRIGGER
        run_id = f"STRESS-{uuid.uuid4().hex[:8].upper()}"
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        base_portfolio_val = self.portfolio_mgr.get_total_value()

        disclaimer = (
            "HACKATHON SIMULATION ASSUMPTION: This stress test reflects scenario-based simulated "
            "sensitivity analysis under predefined crisis assumptions. It is NOT an empirical market prediction."
        )

        if not is_triggered:
            # Sub-threshold event: no stress test triggered
            breakdown = self.portfolio_mgr.get_asset_class_breakdown()
            formatted_breakdown = {
                ac: {
                    "base_value": info["base_value"],
                    "shock_pct": 0.0,
                    "loss_value": 0.0,
                    "stressed_value": info["base_value"]
                }
                for ac, info in breakdown.items()
            }
            return StressTestResult(
                run_id=run_id,
                article_id=signal.article_id,
                company=signal.company,
                ticker=signal.ticker,
                event_type=signal.event_type,
                impact_score=signal.impact_score,
                sentiment_score=signal.sentiment_score,
                triggered=False,
                trigger_reason=f"Impact score {signal.impact_score} <= {settings.IMPACT_THRESHOLD_TRIGGER} threshold. Sub-threshold event.",
                portfolio_before=base_portfolio_val,
                portfolio_after=base_portfolio_val,
                simulated_loss=0.0,
                loss_pct=0.0,
                asset_breakdown=formatted_breakdown,
                scenario_description="No stress shock applied (monitoring status).",
                simulation_assumptions="Standard portfolio operating state.",
                disclaimer=disclaimer,
                created_at=now_iso
            )

        # Triggered: retrieve scenario
        scenario = self.scenario_loader.get_scenario(signal.event_type, signal.impact_score)
        if not scenario:
            scenario = self.scenario_loader.get_scenario("OTHER", signal.impact_score)

        shocks = scenario["shocks"]
        shock_result = self.portfolio_mgr.simulate_stress_shock(shocks)

        result = StressTestResult(
            run_id=run_id,
            article_id=signal.article_id,
            company=signal.company,
            ticker=signal.ticker,
            event_type=signal.event_type,
            impact_score=signal.impact_score,
            sentiment_score=signal.sentiment_score,
            triggered=True,
            trigger_reason=f"CRITICAL: Impact score {signal.impact_score} exceeds threshold {settings.IMPACT_THRESHOLD_TRIGGER}. Stress test shock initiated.",
            portfolio_before=shock_result["portfolio_before"],
            portfolio_after=shock_result["portfolio_after"],
            simulated_loss=shock_result["simulated_loss"],
            loss_pct=shock_result["loss_pct"],
            asset_breakdown=shock_result["asset_breakdown"],
            scenario_description=scenario["description"],
            simulation_assumptions=scenario["assumptions"],
            disclaimer=disclaimer,
            created_at=now_iso
        )

        if persist:
            self._save_to_db(result)

        return result

    def evaluate_batch(self, signals: List[RiskSignal], persist: bool = True) -> List[StressTestResult]:
        """Evaluates a batch of risk signals through the stress testing engine."""
        return [self.evaluate_signal(sig, persist=persist) for sig in signals]

    def _save_to_db(self, result: StressTestResult):
        """Persists stress test execution to database."""
        session = SessionLocal()
        try:
            db_run = StressTestRunDB(
                run_id=result.run_id,
                article_id=result.article_id,
                event_type=result.event_type,
                impact_score=result.impact_score,
                portfolio_before=result.portfolio_before,
                portfolio_after=result.portfolio_after,
                simulated_loss=result.simulated_loss,
                loss_pct=result.loss_pct,
                asset_breakdown_json=json.dumps(result.asset_breakdown),
                created_at=result.created_at
            )
            session.add(db_run)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to persist stress test run: {e}")
        finally:
            session.close()

    def get_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieves recent stress test runs from database."""
        session = SessionLocal()
        try:
            runs = session.query(StressTestRunDB).order_by(StressTestRunDB.created_at.desc()).limit(limit).all()
            history = []
            for r in runs:
                history.append({
                    "run_id": r.run_id,
                    "article_id": r.article_id,
                    "event_type": r.event_type,
                    "impact_score": r.impact_score,
                    "portfolio_before": r.portfolio_before,
                    "portfolio_after": r.portfolio_after,
                    "simulated_loss": r.simulated_loss,
                    "loss_pct": r.loss_pct,
                    "asset_breakdown": json.loads(r.asset_breakdown_json),
                    "created_at": r.created_at
                })
            return history
        finally:
            session.close()
