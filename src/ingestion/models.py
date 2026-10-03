from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime

class RawArticle(BaseModel):
    source: str
    title: str
    content: Optional[str] = ""
    url: Optional[str] = ""
    published_at: Optional[str] = None
    raw_payload: Optional[dict] = None

class NormalizedArticle(BaseModel):
    article_id: str = Field(description="Unique deterministic hash of article title and source/url")
    source: str = Field(description="Originating data source, e.g., GDELT, NewsAPI, or DemoFeed")
    title: str = Field(description="Cleaned headline/title")
    content: str = Field(default="", description="Cleaned full text or summary snippet")
    url: str = Field(default="", description="Canonical article link")
    published_at: str = Field(description="ISO 8601 UTC normalized timestamp YYYY-MM-DDTHH:MM:SSZ")
    company: Optional[str] = Field(default="Unknown", description="Extracted corporate entity name")
    ticker: Optional[str] = Field(default="UNKNOWN", description="Mapped stock exchange ticker symbol")
