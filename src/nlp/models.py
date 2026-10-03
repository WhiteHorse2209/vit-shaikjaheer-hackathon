from pydantic import BaseModel, Field
from typing import Optional

class RiskSignal(BaseModel):
    article_id: str = Field(description="Unique identifier of originating article")
    company: str = Field(description="Corporate entity or market scope")
    ticker: str = Field(description="Stock ticker symbol or MACRO")
    sentiment_score: float = Field(description="FinBERT sentiment score: P(positive) - P(negative), range -1.0 to +1.0")
    event_type: str = Field(description="Categorical financial risk event classification")
    impact_score: float = Field(description="Severity impact metric from 1.0 to 10.0 used for scenario stress triggers")
    confidence: float = Field(description="Model classification confidence between 0.0 and 1.0")
    source: str = Field(description="Underlying news/social media source")
    processed_at: str = Field(description="ISO 8601 UTC timestamp of signal generation")
