from typing import Tuple

# Base severity scores by event category for scenario stress analysis
BASE_EVENT_SEVERITY = {
    "MARKET_CRASH": 8.5,
    "BANKRUPTCY": 8.2,
    "GEOPOLITICAL": 7.6,
    "CREDIT_EVENT": 7.3,
    "MACROECONOMIC": 6.8,
    "REGULATORY": 6.5,
    "MERGER_ACQUISITION": 5.5,
    "INTEREST_RATE": 5.0,
    "EARNINGS": 4.5,
    "PRODUCT_LAUNCH": 4.0,
    "OTHER": 3.0
}

HIGH_SEVERITY_KEYWORDS = [
    "catastrophic", "freeze", "default", "haircut", "margin calls", "blockade",
    "emergency", "panic", "cascade", "unprecedented", "sweeping", "run on"
]

def calculate_impact_score(event_type: str, sentiment_score: float, text: str = "") -> Tuple[float, bool]:
    """
    Computes an AI-derived financial event impact score on a calibrated scale from 1.0 to 10.0.
    
    METHODOLOGY & ASSUMPTIONS:
    1. Base Severity: Rooted in historical market disruption potential of the event category.
    2. Sentiment Modifier: Negative sentiment amplifies downside risk (+1.8 * |sentiment|),
       whereas positive sentiment tempers downside shock potential (-0.8 * sentiment).
    3. Keyword Severity Multiplier: Critical systemic stress keywords add +0.4 to +1.0.
    4. Bounding: Clamped strictly between 1.0 and 10.0, rounded to 1 decimal place.
    
    DISCLAIMER:
    This score is an AI-derived scenario severity indicator for portfolio stress testing,
    NOT a guaranteed statistical market prediction.
    
    Returns:
        (impact_score, is_high_impact)
        is_high_impact is True if impact_score > 7.0
    """
    base = BASE_EVENT_SEVERITY.get(event_type, 3.0)
    
    # Sentiment adjustment
    if sentiment_score < 0:
        sentiment_adj = 1.8 * abs(sentiment_score)
    else:
        sentiment_adj = -0.8 * sentiment_score
        
    # Keyword intensity check
    keyword_adj = 0.0
    if text:
        text_lower = text.lower()
        matches = sum(1 for kw in HIGH_SEVERITY_KEYWORDS if kw in text_lower)
        if matches > 0:
            keyword_adj = min(1.2, 0.4 * matches)
            
    raw_score = base + sentiment_adj + keyword_adj
    final_score = round(max(1.0, min(10.0, raw_score)), 1)
    
    is_high_impact = final_score > 7.0
    return final_score, is_high_impact
