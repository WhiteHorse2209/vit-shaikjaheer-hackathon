import os
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.config import settings
from src.ingestion.pipeline import IngestionPipeline
from src.ingestion.models import NormalizedArticle
from src.nlp.risk_engine import NLPRiskEngine
from src.nlp.models import RiskSignal
from src.risk.portfolio import PortfolioManager
from src.risk.scenario_loader import ScenarioLoader
from src.risk.market_data import MarketDataProvider, TRACKED_TICKERS
from src.risk.stress_testing import StressTestEngine, StressTestResult
from src.database.db import SessionLocal, ArticleDB, RiskSignalDB, StressTestRunDB, init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI/NLP Financial Risk Engine & Strategic Portfolio Stress Testing API (S&P Global & CRISIL Hackathon 2026)"
)

# Enable CORS for external dashboards or microservices
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize singletons
init_db()
portfolio_mgr = PortfolioManager()
scenario_loader = ScenarioLoader()
market_provider = MarketDataProvider()
nlp_engine = NLPRiskEngine()
stress_engine = StressTestEngine(portfolio_manager=portfolio_mgr, scenario_loader=scenario_loader)

class IngestRequest(BaseModel):
    mode: Optional[str] = None
    query: Optional[str] = "finance OR market OR economy"

class CustomTextRequest(BaseModel):
    title: str
    content: str
    source: Optional[str] = "Custom User Input"
    company: Optional[str] = None
    ticker: Optional[str] = None

@app.get("/health", tags=["System"])
def health_check():
    """Returns system status, active execution mode, and database connection state."""
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "mode": settings.MODE,
        "impact_threshold": settings.IMPACT_THRESHOLD_TRIGGER,
        "database": "sqlite/connected",
        "models": {
            "sentiment": "ProsusAI/finbert",
            "taxonomy": "11-Category Financial Taxonomy",
            "stress_engine": "Module B (Strategic Stress Testing)"
        }
    }

@app.post("/api/ingest", tags=["Phase 1: Ingestion"])
def run_ingestion(req: IngestRequest):
    """
    Ingests financial news/social media articles.
    Supports LIVE mode (GDELT + NewsAPI) and DEMO mode (local sample repository).
    """
    mode = req.mode or settings.MODE
    pipeline = IngestionPipeline(mode=mode)
    articles = pipeline.run(query=req.query, persist=True)
    return {
        "mode": mode,
        "count": len(articles),
        "articles": [a.model_dump() for a in articles]
    }

@app.get("/api/news", tags=["Phase 1: Ingestion"])
def get_ingested_news():
    """Retrieves all ingested articles from database."""
    session = SessionLocal()
    try:
        articles = session.query(ArticleDB).order_by(ArticleDB.created_at.desc()).all()
        return [
            {
                "article_id": a.article_id,
                "source": a.source,
                "title": a.title,
                "content": a.content,
                "url": a.url,
                "published_at": a.published_at,
                "company": a.company,
                "ticker": a.ticker
            }
            for a in articles
        ]
    finally:
        session.close()

@app.post("/api/nlp/process", tags=["Phase 2: NLP Risk Engine"])
def process_nlp_signals(use_database: bool = True):
    """
    Runs FinBERT sentiment, event taxonomy classification, and 1-10 impact scoring
    on all ingested articles. Saves signals to database.
    """
    pipeline = IngestionPipeline(mode=settings.MODE)
    articles = pipeline.run(persist=False)
    signals = nlp_engine.process_batch(articles, persist=True)
    return {
        "count": len(signals),
        "signals": [s.model_dump() for s in signals]
    }

@app.post("/api/nlp/analyze-text", tags=["Phase 2: NLP Risk Engine"])
def analyze_custom_headline(req: CustomTextRequest):
    """Interactive endpoint to score custom breaking news headlines on the fly."""
    from src.ingestion.cleaner import generate_article_id, normalize_timestamp
    art_id = generate_article_id(req.title)
    article = NormalizedArticle(
        article_id=art_id,
        source=req.source,
        title=req.title,
        content=req.content,
        url="https://user-submitted-event.internal",
        published_at=normalize_timestamp(None),
        company=req.company,
        ticker=req.ticker
    )
    signal = nlp_engine.process_article(article)
    stress_result = stress_engine.evaluate_signal(signal, persist=True)
    return {
        "signal": signal.model_dump(),
        "stress_test": stress_result.model_dump()
    }

@app.get("/api/risk-signals", tags=["Phase 2: NLP Risk Engine"])
def get_risk_signals():
    """Retrieves generated risk signals ordered by most recent."""
    session = SessionLocal()
    try:
        signals = session.query(RiskSignalDB).order_by(RiskSignalDB.id.desc()).all()
        return [
            {
                "article_id": s.article_id,
                "company": s.company,
                "ticker": s.ticker,
                "sentiment_score": s.sentiment_score,
                "event_type": s.event_type,
                "impact_score": s.impact_score,
                "confidence": s.confidence,
                "source": s.source,
                "processed_at": s.processed_at
            }
            for s in signals
        ]
    finally:
        session.close()

@app.get("/api/portfolio", tags=["Phase 3: Financial Intelligence"])
def get_portfolio_summary():
    """Returns baseline synthetic portfolio valuation and asset class breakdown."""
    total = portfolio_mgr.get_total_value()
    breakdown = portfolio_mgr.get_asset_class_breakdown()
    holdings = portfolio_mgr.get_holdings()
    return {
        "total_value": total,
        "currency": "INR",
        "formatted_total": f"₹{total:,.2f}",
        "asset_classes": breakdown,
        "holdings_count": len(holdings),
        "holdings": holdings
    }

@app.get("/api/market-data", tags=["Phase 3: Financial Intelligence"])
def get_market_data(use_live: bool = False):
    """Returns market metrics, daily changes, and volatility for tracked equities."""
    metrics = market_provider.get_all_tracked_metrics(use_live=use_live)
    return {
        "tracked_universe": TRACKED_TICKERS,
        "count": len(metrics),
        "data": metrics
    }

@app.get("/api/stress-scenarios", tags=["Phase 3: Financial Intelligence"])
def get_stress_scenarios():
    """Returns predefined stress testing shock matrices."""
    df = scenario_loader.scenarios_df
    return df.to_dict(orient="records")

@app.post("/api/stress-test/evaluate-all", tags=["Phase 4: Module B Stress Testing"])
def evaluate_all_stress_tests():
    """
    Evaluates all existing risk signals. For signals with impact > 7.0, triggers
    asset-level portfolio shocks and calculates simulated losses.
    """
    pipeline = IngestionPipeline(mode=settings.MODE)
    articles = pipeline.run(persist=False)
    signals = nlp_engine.process_batch(articles, persist=True)
    results = stress_engine.evaluate_batch(signals, persist=True)
    
    triggered_count = sum(1 for r in results if r.triggered)
    total_simulated_loss = sum(r.simulated_loss for r in results if r.triggered)
    
    return {
        "total_signals_evaluated": len(results),
        "triggered_count": triggered_count,
        "total_simulated_loss": round(total_simulated_loss, 2),
        "results": [r.model_dump() for r in results]
    }

@app.get("/api/stress-test/history", tags=["Phase 4: Module B Stress Testing"])
def get_stress_history(limit: int = 25):
    """Retrieves historical stress test audit trail."""
    return stress_engine.get_history(limit=limit)

# Dashboard web route
@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
def serve_dashboard():
    """Serves the interactive modern glassmorphism frontend dashboard."""
    dashboard_path = Path(__file__).resolve().parent / "dashboard.html"
    if dashboard_path.exists():
        with open(dashboard_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>AI/NLP Financial Risk Engine Dashboard</h1><p>API is active. Visit /docs for Swagger.</p>")
