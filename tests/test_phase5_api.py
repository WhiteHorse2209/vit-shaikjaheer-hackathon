import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_api_health():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert "finbert" in str(data["models"]).lower()

def test_api_ingest_demo():
    res = client.post("/api/ingest", json={"mode": "DEMO"})
    assert res.status_code == 200
    data = res.json()
    assert data["count"] >= 10
    assert len(data["articles"]) >= 10

def test_api_get_news():
    res = client.get("/api/news")
    assert res.status_code == 200
    news = res.json()
    assert len(news) >= 10
    first = news[0]
    assert "article_id" in first
    assert "company" in first
    assert "ticker" in first

def test_api_nlp_process():
    res = client.post("/api/nlp/process")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] >= 10
    assert len(data["signals"]) >= 10
    for s in data["signals"]:
        assert -1.0 <= s["sentiment_score"] <= 1.0
        assert 1.0 <= s["impact_score"] <= 10.0

def test_api_get_risk_signals():
    res = client.get("/api/risk-signals")
    assert res.status_code == 200
    signals = res.json()
    assert len(signals) >= 10

def test_api_portfolio():
    res = client.get("/api/portfolio")
    assert res.status_code == 200
    port = res.json()
    assert port["total_value"] == 100_000_000.0
    assert "Equities" in port["asset_classes"]
    assert "Bonds" in port["asset_classes"]
    assert "Loans" in port["asset_classes"]
    assert "Derivatives" in port["asset_classes"]

def test_api_market_data():
    res = client.get("/api/market-data")
    assert res.status_code == 200
    mkt = res.json()
    assert mkt["count"] == 10
    assert len(mkt["data"]) == 10

def test_api_stress_scenarios():
    res = client.get("/api/stress-scenarios")
    assert res.status_code == 200
    scenarios = res.json()
    assert len(scenarios) >= 5

def test_api_stress_evaluate_all():
    res = client.post("/api/stress-test/evaluate-all")
    assert res.status_code == 200
    data = res.json()
    assert data["triggered_count"] >= 3
    assert data["total_simulated_loss"] > 0
    assert len(data["results"]) >= 10

def test_api_analyze_custom_headline():
    payload = {
        "title": "Catastrophic algorithmic flash crash and liquidity freeze wipes $500B off mega-cap equities",
        "content": "Automated selling cascade triggered exchange circuit breakers, freezing derivative spreads and inflicting severe losses across tech portfolios.",
        "source": "Breaking Market Alert"
    }
    res = client.post("/api/nlp/analyze-text", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "signal" in data
    assert "stress_test" in data
    assert data["signal"]["sentiment_score"] < 0
    assert data["signal"]["impact_score"] > 7.0
    assert data["stress_test"]["triggered"] is True

def test_dashboard_html_serve():
    res = client.get("/")
    assert res.status_code == 200
    assert "AI/NLP Financial Risk Engine" in res.text
    assert "portfolioChart" in res.text
