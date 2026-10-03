import re
import html
import hashlib
from datetime import datetime, timezone
from typing import Optional, List, Set
from dateutil import parser as date_parser

def clean_text(raw_text: Optional[str]) -> str:
    """Removes HTML tags, decodes HTML entities, and strips irregular whitespaces."""
    if not raw_text:
        return ""
    # Unescape HTML entities (&amp;, &lt;, etc.)
    text = html.unescape(raw_text)
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Replace multiple whitespace/newlines with single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def generate_article_id(title: str, url: str = "") -> str:
    """Creates a deterministic 16-character SHA-256 hash based on title and URL."""
    clean_key = f"{title.strip().lower()}|{url.strip().lower()}"
    return hashlib.sha256(clean_key.encode('utf-8')).hexdigest()[:16]

def normalize_timestamp(raw_date: Optional[str]) -> str:
    """
    Normalizes varied timestamp formats into ISO 8601 UTC standard: YYYY-MM-DDTHH:MM:SSZ.
    Handles GDELT compact format (YYYYMMDDHHMMSS), ISO strings, and standard date strings.
    """
    if not raw_date:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    raw_date = str(raw_date).strip()
    
    # Check GDELT format: 14 digits YYYYMMDDHHMMSS
    if re.match(r'^\d{14}$', raw_date):
        try:
            dt = datetime.strptime(raw_date, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            pass
            
    # Try generic dateutil parser
    try:
        dt = date_parser.parse(raw_date)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def deduplicate_articles(articles: List[dict], key_func=lambda a: a.get("article_id")) -> List[dict]:
    """Filters out duplicate articles based on a distinct key (e.g. article_id or url)."""
    seen: Set[str] = set()
    deduped = []
    for art in articles:
        key = key_func(art)
        if key and key not in seen:
            seen.add(key)
            deduped.append(art)
    return deduped
