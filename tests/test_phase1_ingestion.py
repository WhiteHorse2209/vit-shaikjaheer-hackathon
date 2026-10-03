

import pytest
import os
from pathlib import Path
from src.ingestion.cleaner import clean_text, normalize_timestamp, generate_article_id, deduplicate_articles
from src.ingestion.company_mapper import extract_company_and_ticker
from src.ingestion.pipeline import IngestionPipeline
from src.ingestion.models import NormalizedArticle
from src.database.db import SessionLocal, ArticleDB, init_db

def test_clean_text():
    raw_html = "<p>Fed announces <b>rate hike</b> &amp; liquidity adjustment.</p>\n\n  "
    cleaned = clean_text(raw_html)
    assert cleaned == "Fed announces rate hike & liquidity adjustment."

def test_normalize_timestamp():
    # GDELT compact 14-digit format
    gdelt_date = "20261002143000"
    norm_gdelt = normalize_timestamp(gdelt_date)
    assert norm_gdelt == "2026-10-02T14:30:00Z"
    
    # ISO string
    iso_date = "2026-10-02T14:30:00+00:00"
    norm_iso = normalize_timestamp(iso_date)
    assert norm_iso == "2026-10-02T14:30:00Z"

def test_generate_article_id():
    id1 = generate_article_id("Apple beats revenue expectations", "https://apple.com/news/1")
    id2 = generate_article_id("Apple beats revenue expectations", "https://apple.com/news/1")
    id3 = generate_article_id("Nvidia announces new AI chip", "https://nvidia.com/news/1")
    assert id1 == id2
    assert id1 != id3
    assert len(id1) == 16

def test_deduplicate_articles():
    articles = [
        {"article_id": "art-1", "title": "Article One"},
        {"article_id": "art-1", "title": "Article One Duplicate"},
        {"article_id": "art-2", "title": "Article Two"}
    ]
    deduped = deduplicate_articles(articles, key_func=lambda a: a["article_id"])
    assert len(deduped) == 2
    assert deduped[0]["title"] == "Article One"
    assert deduped[1]["title"] == "Article Two"

def test_company_ticker_mapping():
    c1, t1 = extract_company_and_ticker("NVIDIA announces next-generation Blackwell AI architecture")
    assert t1 == "NVDA"
    assert "NVIDIA" in c1

    c2, t2 = extract_company_and_ticker("Apple releases fiscal results with Tim Cook commentary")
    assert t2 == "AAPL"
    assert "Apple" in c2

    c3, t3 = extract_company_and_ticker("JPMorgan Chase sets aside provisions for commercial loan risks")
    assert t3 == "JPM"

    c4, t4 = extract_company_and_ticker("Global central banks discuss global liquidity trends")
    assert t4 == "MACRO"
    assert c4 == "General Market"

def test_demo_mode_ingestion():
    pipeline = IngestionPipeline(mode="DEMO")
    articles = pipeline.run(persist=True)
    assert len(articles) >= 10
    
    for art in articles:
        assert isinstance(art, NormalizedArticle)
        assert art.article_id
        assert art.source
        assert art.title
        assert art.published_at.endswith("Z")
        assert art.company
        assert art.ticker

def test_sqlite_persistence():
    init_db()
    session = SessionLocal()
    count = session.query(ArticleDB).count()
    assert count >= 10
    session.close()
