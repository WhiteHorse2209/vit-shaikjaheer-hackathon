import logging
import requests
from typing import List, Optional
from src.config import settings
from src.ingestion.models import NormalizedArticle
from src.ingestion.cleaner import clean_text, generate_article_id, normalize_timestamp
from src.ingestion.company_mapper import extract_company_and_ticker

logger = logging.getLogger(__name__)

NEWSAPI_EVERYTHING_URL = "https://newsapi.org/v2/everything"

def fetch_newsapi_articles(query: str = "stocks OR Federal Reserve OR market", page_size: int = 15, api_key: Optional[str] = None, timeout: int = 8) -> List[NormalizedArticle]:
    """
    Ingests live articles from NewsAPI v2.
    URL: https://newsapi.org/docs
    Returns a list of NormalizedArticle objects.
    """
    key = api_key or settings.NEWSAPI_KEY
    if not key or key.strip() == "":
        logger.info("NewsAPI API key not provided; skipping live NewsAPI call.")
        return []
        
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": key
    }
    
    articles: List[NormalizedArticle] = []
    
    try:
        response = requests.get(NEWSAPI_EVERYTHING_URL, params=params, timeout=timeout)
        if response.status_code != 200:
            logger.warning(f"NewsAPI returned status {response.status_code}: {response.text[:200]}")
            return articles
            
        data = response.json()
        raw_items = data.get("articles", [])
        
        for item in raw_items:
            title = clean_text(item.get("title", ""))
            if not title or "[Removed]" in title:
                continue
            content = clean_text(item.get("description", "") or item.get("content", ""))
            url = item.get("url", "").strip()
            art_id = generate_article_id(title, url)
            pub_date = normalize_timestamp(item.get("publishedAt", ""))
            
            company, ticker = extract_company_and_ticker(f"{title} {content}")
            
            source_name = item.get("source", {}).get("name", "NewsAPI")
            
            article = NormalizedArticle(
                article_id=art_id,
                source=f"NewsAPI ({source_name})",
                title=title,
                content=content,
                url=url,
                published_at=pub_date,
                company=company,
                ticker=ticker
            )
            articles.append(article)
            
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to query NewsAPI: {e}")
    except Exception as e:
        logger.error(f"Unexpected error parsing NewsAPI response: {e}")
        
    return articles
