import json
import logging
from pathlib import Path
from typing import List, Optional
from src.config import settings
from src.ingestion.models import NormalizedArticle
from src.ingestion.gdelt import fetch_gdelt_news
from src.ingestion.newsapi import fetch_newsapi_articles
from src.ingestion.cleaner import deduplicate_articles
from src.database.db import SessionLocal, ArticleDB, init_db

logger = logging.getLogger(__name__)

class IngestionPipeline:
    def __init__(self, mode: Optional[str] = None):
        self.mode = (mode or settings.MODE).upper()
        init_db()

    def run(self, query: str = "finance OR market OR economy", persist: bool = True) -> List[NormalizedArticle]:
        """
        Executes ingestion based on current mode ('LIVE' or 'DEMO').
        Returns list of validated, deduplicated NormalizedArticle objects.
        """
        articles: List[NormalizedArticle] = []

        if self.mode == "LIVE":
            logger.info("Executing LIVE data ingestion from GDELT and NewsAPI...")
            gdelt_results = fetch_gdelt_news(query=query, max_records=15)
            newsapi_results = fetch_newsapi_articles(query=query, page_size=15)
            
            combined = gdelt_results + newsapi_results
            logger.info(f"Retrieved {len(gdelt_results)} GDELT and {len(newsapi_results)} NewsAPI articles.")
            
            # If live APIs returned 0 items (e.g. offline / rate limit), gracefully fallback to sample data
            if not combined:
                logger.warning("Live feeds returned no articles (offline or rate limited). Falling back to DEMO sample feed.")
                return self._load_sample_data(persist=persist)
                
            # Deduplicate by article_id
            dict_articles = [art.model_dump() for art in combined]
            deduped_dicts = deduplicate_articles(dict_articles, key_func=lambda a: a["article_id"])
            articles = [NormalizedArticle(**d) for d in deduped_dicts]
            
        else:
            logger.info("Executing DEMO data ingestion from local repository dataset...")
            articles = self._load_sample_data(persist=persist)

        if persist:
            self._save_to_db(articles)

        return articles

    def _load_sample_data(self, persist: bool = True) -> List[NormalizedArticle]:
        """Loads vetted sample news from data/sample_news.json."""
        sample_path = settings.SAMPLE_NEWS_PATH
        if not sample_path.exists():
            logger.error(f"Sample news file not found at {sample_path}")
            return []

        with open(sample_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        articles = [NormalizedArticle(**item) for item in data]
        return articles

    def _save_to_db(self, articles: List[NormalizedArticle]):
        """Persists articles into SQLite database with upsert / ignore existing."""
        session = SessionLocal()
        try:
            for art in articles:
                existing = session.query(ArticleDB).filter(ArticleDB.article_id == art.article_id).first()
                if not existing:
                    db_art = ArticleDB(
                        article_id=art.article_id,
                        source=art.source,
                        title=art.title,
                        content=art.content,
                        url=art.url,
                        published_at=art.published_at,
                        company=art.company or "General Market",
                        ticker=art.ticker or "MACRO"
                    )
                    session.add(db_art)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database persistence error: {e}")
        finally:
            session.close()
