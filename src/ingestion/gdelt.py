import logging
import requests
from typing import List
from src.ingestion.models import NormalizedArticle
from src.ingestion.cleaner import clean_text, generate_article_id, normalize_timestamp
from src.ingestion.company_mapper import extract_company_and_ticker

logger = logging.getLogger(__name__)

GDELT_DOC_API_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

def fetch_gdelt_news(query: str = "finance OR economy OR stocks OR bank", max_records: int = 15, timeout: int = 8) -> List[NormalizedArticle]:
    """
    Ingests live articles from GDELT 2.0 DOC API.
    URL: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
    Returns a list of NormalizedArticle objects.
    """
    params = {
        "query": query,
        "mode": "artlist",
        "format": "json",
        "maxrecords": max_records,
        "sort": "DateDesc"
    }
    
    articles: List[NormalizedArticle] = []
    
    try:
        response = requests.get(GDELT_DOC_API_URL, params=params, timeout=timeout)
        if response.status_code != 200:
            logger.warning(f"GDELT API returned status {response.status_code}")
            return articles
            
        data = response.json()
        raw_items = data.get("articles", [])
        
        for item in raw_items:
            title = clean_text(item.get("title", ""))
            if not title:
                continue
            url = item.get("url", "").strip()
            art_id = generate_article_id(title, url)
            pub_date = normalize_timestamp(item.get("seendate", ""))
            
            # GDELT doesn't provide full content in artlist mode, so title + meta serves as text
            content = clean_text(f"{title}. Source: {item.get('domain', 'GDELT')}")
            company, ticker = extract_company_and_ticker(f"{title} {content}")
            
            article = NormalizedArticle(
                article_id=art_id,
                source="GDELT",
                title=title,
                content=content,
                url=url,
                published_at=pub_date,
                company=company,
                ticker=ticker
            )
            articles.append(article)
            
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to query GDELT API: {e}")
    except Exception as e:
        logger.error(f"Unexpected error parsing GDELT data: {e}")
        
    return articles
