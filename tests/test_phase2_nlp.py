import pytest
import os
import json
from pathlib import Path
from src.nlp.sentiment import FinBERTSentimentAnalyzer
from src.nlp.event_classifier import EventClassifier
from src.nlp.impact_scorer import calculate_impact_score
from src.nlp.risk_engine import NLPRiskEngine
from src.nlp.models import RiskSignal
from src.ingestion.pipeline import IngestionPipeline
from src.database.db import SessionLocal, RiskSignalDB, init_db

def test_sentiment_analyzer_scoring():
    analyzer = FinBERTSentimentAnalyzer()
    
    # Highly positive sentence
    pos_text = "Apple reports record revenue beat and unprecedented profit expansion."
    pos_score, pos_conf, pos_label, _ = analyzer.analyze(pos_text)
    assert -1.0 <= pos_score <= 1.0
    assert pos_score > 0.0
    assert 0.0 <= pos_conf <= 1.0
    
    # Highly negative sentence
    neg_text = "Major regional bank files for bankruptcy following catastrophic default and liquidity run."
    neg_score, neg_conf, neg_label, _ = analyzer.analyze(neg_text)
    assert -1.0 <= neg_score <= 1.0
    assert neg_score < 0.0
    assert 0.0 <= neg_conf <= 1.0

def test_event_classifier_categories():
    classifier = EventClassifier()
    
    cat1, _ = classifier.classify("Escalating geopolitical conflict and military blockade in the Taiwan Strait.")
    assert cat1 == "GEOPOLITICAL"
    
    cat2, _ = classifier.classify("Federal Reserve signals monetary tightening to combat sticky inflation and stagflation.")
    assert cat2 == "MACROECONOMIC"
    
    cat3, _ = classifier.classify("Credit rating downgrade hits corporate bonds with bank margin calls.")
    assert cat3 == "CREDIT_EVENT"
    
    cat4, _ = classifier.classify("Algorithmic cascade triggers flash crash across high-growth tech equities.")
    assert cat4 == "MARKET_CRASH"
    
    cat5, _ = classifier.classify("Fintech lender files for Chapter 11 bankruptcy reorganization.")
    assert cat5 == "BANKRUPTCY"
    
    cat6, _ = classifier.classify("DOJ and FTC file major antitrust monopoly lawsuit demanding structural divestiture.")
    assert cat6 == "REGULATORY"
    
    cat7, _ = classifier.classify("Apple posts record quarterly earnings beating consensus estimates.")
    assert cat7 == "EARNINGS"

def test_impact_scoring_logic():
    # Severe crash with negative sentiment
    crash_score, crash_high = calculate_impact_score("MARKET_CRASH", -0.85, "algorithmic cascade flash crash liquidity freeze")
    assert 1.0 <= crash_score <= 10.0
    assert crash_score > 7.0
    assert crash_high is True
    
    # Geopolitical event with negative sentiment
    geo_score, geo_high = calculate_impact_score("GEOPOLITICAL", -0.75, "military posturing and blockade threat")
    assert geo_score > 7.0
    assert geo_high is True
    
    # Routine product launch with positive sentiment
    prod_score, prod_high = calculate_impact_score("PRODUCT_LAUNCH", 0.60, "unveils new smartphone model")
    assert 1.0 <= prod_score <= 10.0
    assert prod_score < 7.0
    assert prod_high is False

def test_nlp_risk_engine_batch():
    init_db()
    # 1. Ingest sample articles
    pipeline = IngestionPipeline(mode="DEMO")
    articles = pipeline.run(persist=False)
    assert len(articles) >= 10
    
    # 2. Run NLP Risk Engine
    engine = NLPRiskEngine()
    signals = engine.process_batch(articles, persist=True)
    
    assert len(signals) == len(articles)
    
    high_impact_count = 0
    for sig in signals:
        assert isinstance(sig, RiskSignal)
        assert -1.0 <= sig.sentiment_score <= 1.0
        assert 1.0 <= sig.impact_score <= 10.0
        assert sig.company
        assert sig.ticker
        assert sig.event_type in [
            "GEOPOLITICAL", "MACROECONOMIC", "CREDIT_EVENT", "MERGER_ACQUISITION",
            "PRODUCT_LAUNCH", "EARNINGS", "REGULATORY", "BANKRUPTCY", "INTEREST_RATE",
            "MARKET_CRASH", "OTHER"
        ]
        if sig.impact_score > 7.0:
            high_impact_count += 1
            
    # Must have multiple high-impact triggers to test stress testing in Phase 4
    assert high_impact_count >= 3
    
    # Check DB persistence
    session = SessionLocal()
    db_count = session.query(RiskSignalDB).count()
    assert db_count >= len(signals)
    session.close()
    
    # Check JSON export file
    json_path = Path("data/risk_signals.json")
    assert json_path.exists()
    with open(json_path, "r", encoding="utf-8") as f:
        exported = json.load(f)
    assert len(exported) == len(signals)
