import pytest
from src.nlp.models import RiskSignal
from src.risk.stress_testing import StressTestEngine, StressTestResult
from src.database.db import SessionLocal, StressTestRunDB, init_db

def test_stress_test_trigger_threshold():
    engine = StressTestEngine()
    
    # 1. High-impact signal (> 7.0)
    high_sig = RiskSignal(
        article_id="test-crash-1",
        company="Alphabet Inc.",
        ticker="GOOGL",
        sentiment_score=-0.85,
        event_type="MARKET_CRASH",
        impact_score=8.8,
        confidence=0.92,
        source="WSJ",
        processed_at="2026-10-02T12:00:00Z"
    )
    res_high = engine.evaluate_signal(high_sig, persist=True)
    assert res_high.triggered is True
    assert res_high.portfolio_before == 100_000_000.0
    # MARKET_CRASH shocks: Eq -15%, Bond -5%, Loan -5%, Deriv -18%
    # Loss: 40*0.15 + 25*0.05 + 20*0.05 + 15*0.18 = 6.0 + 1.25 + 1.0 + 2.7 = 10.95M
    assert res_high.simulated_loss == 10_950_000.0
    assert res_high.portfolio_after == 89_050_000.0
    assert res_high.loss_pct == 10.95
    assert "Equities" in res_high.asset_breakdown
    assert res_high.asset_breakdown["Equities"]["shock_pct"] == -15.0

    # 2. Sub-threshold signal (<= 7.0)
    low_sig = RiskSignal(
        article_id="test-earn-2",
        company="Apple Inc.",
        ticker="AAPL",
        sentiment_score=0.65,
        event_type="EARNINGS",
        impact_score=4.5,
        confidence=0.88,
        source="CNBC",
        processed_at="2026-10-02T12:05:00Z"
    )
    res_low = engine.evaluate_signal(low_sig, persist=False)
    assert res_low.triggered is False
    assert res_low.simulated_loss == 0.0
    assert res_low.portfolio_after == 100_000_000.0
    assert "Sub-threshold" in res_low.trigger_reason

def test_stress_test_history_and_persistence():
    init_db()
    engine = StressTestEngine()
    
    geo_sig = RiskSignal(
        article_id="test-geo-hist",
        company="NVIDIA Corporation",
        ticker="NVDA",
        sentiment_score=-0.75,
        event_type="GEOPOLITICAL",
        impact_score=8.2,
        confidence=0.90,
        source="FT",
        processed_at="2026-10-02T13:00:00Z"
    )
    res = engine.evaluate_signal(geo_sig, persist=True)
    assert res.triggered is True
    
    history = engine.get_history(limit=5)
    assert len(history) > 0
    recent_run = history[0]
    assert "run_id" in recent_run
    assert recent_run["event_type"] in ["GEOPOLITICAL", "MARKET_CRASH"]
    assert recent_run["simulated_loss"] > 0
