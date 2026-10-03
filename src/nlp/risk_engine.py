import json
import logging
from datetime import datetime, timezone
from typing import List, Optional
from src.config import settings
from src.ingestion.models import NormalizedArticle
from src.ingestion.company_mapper import extract_company_and_ticker
from src.nlp.models import RiskSignal
from src.nlp.sentiment import FinBERTSentimentAnalyzer
from src.nlp.event_classifier import EventClassifier
from src.nlp.impact_scorer import calculate_impact_score
from src.database.db import SessionLocal, RiskSignalDB, init_db

logger = logging.getLogger(__name__)

class NLPRiskEngine:
    """
    Core AI/NLP Financial Risk Engine.
    Converts unstructured financial news/social media articles into structured risk signals:
    - Sentiment score: -1.0 to +1.0 via FinBERT [P(positive) - P(negative)]
    - Event Classification: Geopolitical, Macroeconomic, Credit Event, etc.
    - Impact Score: 1 to 10 calibrated scenario severity indicator.
    """
    
    def __init__(self):
        init_db()
        self.sentiment_analyzer = FinBERTSentimentAnalyzer()
        self.event_classifier = EventClassifier()

    def process_article(self, article: NormalizedArticle) -> RiskSignal:
        """Processes a single normalized article into a structured RiskSignal."""
        combined_text = f"{article.title}. {article.content}".strip()
        
        # 1. Company & Ticker extraction (if not already assigned)
        company = article.company
        ticker = article.ticker
        if not company or company == "Unknown" or ticker == "UNKNOWN":
            company, ticker = extract_company_and_ticker(combined_text)

        # 2. FinBERT Sentiment Analysis
        sentiment_score, sent_conf, _, _ = self.sentiment_analyzer.analyze(combined_text)

        # 3. Event Classification
        event_type, event_conf = self.event_classifier.classify(combined_text)

        # 4. Impact Scoring (1 to 10)
        impact_score, _ = calculate_impact_score(event_type, sentiment_score, combined_text)

        # 5. Composite Confidence
        composite_confidence = round((sent_conf * 0.5) + (event_conf * 0.5), 2)

        # 6. Structured Risk Signal
        signal = RiskSignal(
            article_id=article.article_id,
            company=company,
            ticker=ticker,
            sentiment_score=sentiment_score,
            event_type=event_type,
            impact_score=impact_score,
            confidence=composite_confidence,
            source=article.source,
            processed_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        return signal

    def process_batch(self, articles: List[NormalizedArticle], persist: bool = True) -> List[RiskSignal]:
        """Processes multiple articles into risk signals, persists to database, and writes JSON."""
        signals: List[RiskSignal] = []
        for art in articles:
            try:
                sig = self.process_article(art)
                signals.append(sig)
            except Exception as e:
                logger.error(f"Error processing article {art.article_id}: {e}")

        if persist and signals:
            self._save_to_db(signals)
            self._export_to_json(signals)

        return signals

    def _save_to_db(self, signals: List[RiskSignal]):
        """Persists risk signals to SQLite database."""
        session = SessionLocal()
        try:
            for sig in signals:
                db_signal = RiskSignalDB(
                    article_id=sig.article_id,
                    company=sig.company,
                    ticker=sig.ticker,
                    sentiment_score=sig.sentiment_score,
                    event_type=sig.event_type,
                    impact_score=sig.impact_score,
                    confidence=sig.confidence,
                    source=sig.source,
                    processed_at=sig.processed_at
                )
                session.add(db_signal)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to persist risk signals to DB: {e}")
        finally:
            session.close()

    def _export_to_json(self, signals: List[RiskSignal]):
        """Exports risk signals to data/risk_signals.json for easy inspection and API consumption."""
        out_path = settings.DATA_DIR / "risk_signals.json"
        try:
            data = [s.model_dump() for s in signals]
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Exported {len(signals)} risk signals to {out_path}")
        except Exception as e:
            logger.error(f"Failed to write risk signals JSON: {e}")
