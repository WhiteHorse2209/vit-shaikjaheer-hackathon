import json
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, String, Float, DateTime, Text, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from src.config import settings

Base = declarative_base()

class ArticleDB(Base):
    __tablename__ = "articles"

    article_id = Column(String(64), primary_key=True, index=True)
    source = Column(String(128), nullable=False)
    title = Column(String(512), nullable=False)
    content = Column(Text, nullable=True)
    url = Column(String(1024), nullable=True)
    published_at = Column(String(64), nullable=False)
    company = Column(String(128), default="General Market")
    ticker = Column(String(32), default="MACRO")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class RiskSignalDB(Base):
    __tablename__ = "risk_signals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(String(64), index=True)
    company = Column(String(128), nullable=False)
    ticker = Column(String(32), nullable=False)
    sentiment_score = Column(Float, nullable=False)
    event_type = Column(String(64), nullable=False)
    impact_score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    source = Column(String(128), nullable=False)
    processed_at = Column(String(64), nullable=False)

class StressTestRunDB(Base):
    __tablename__ = "stress_test_runs"

    run_id = Column(String(64), primary_key=True, index=True)
    article_id = Column(String(64), nullable=True)
    event_type = Column(String(64), nullable=False)
    impact_score = Column(Float, nullable=False)
    portfolio_before = Column(Float, nullable=False)
    portfolio_after = Column(Float, nullable=False)
    simulated_loss = Column(Float, nullable=False)
    loss_pct = Column(Float, nullable=False)
    asset_breakdown_json = Column(Text, nullable=False)
    created_at = Column(String(64), nullable=False)

# Engine & Session
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Creates database schema tables if not existing."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency helper yielding database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
