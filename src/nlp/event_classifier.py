import re
from typing import Tuple, Dict

EVENT_TAXONOMY: Dict[str, list] = {
    "MARKET_CRASH": [
        "flash crash", "circuit breaker", "market crash", "panic selling", "liquidity freeze",
        "market rout", "tumbled across major indices", "algorithmic cascade", "sell-off"
    ],
    "BANKRUPTCY": [
        "chapter 11", "bankruptcy", "insolvent", "insolvency", "liquidation",
        "liquidity run", "receivership", "debt haircut", "reorganization"
    ],
    "CREDIT_EVENT": [
        "credit rating downgrade", "downgraded", "margin calls", "debt default", "credit default",
        "speculative grade", "default risk", "mortgage-backed securities", "loan default"
    ],
    "GEOPOLITICAL": [
        "geopolitical", "taiwan strait", "military posturing", "war", "sanctions", "blockade",
        "trade war", "embargo", "airspace restriction", "defense conflict"
    ],
    "REGULATORY": [
        "antitrust", "doj", "ftc", "sec investigation", "enforcement action", "monopoly lawsuit",
        "regulatory fine", "divestiture", "mandatory spin-off", "compliance violation"
    ],
    "MACROECONOMIC": [
        "stagflation", "inflation", "recession", "monetary tightening", "gdp contraction",
        "wage-price spiral", "economic slowdown", "federal reserve chair warned"
    ],
    "INTEREST_RATE": [
        "interest rate", "rate hike", "rate cut", "basis points", "holds key policy rate",
        "policy rate", "deposit facility rate", "benchmark rate", "central bank"
    ],
    "MERGER_ACQUISITION": [
        "acquisition", "merger", "takeover", "buyout", "finalizes acquisition",
        "completed the acquisition", "all-cash acquisition", "tender offer"
    ],
    "EARNINGS": [
        "quarterly earnings", "revenue beat", "posts record", "operating cash flow",
        "q4 earnings", "q3 earnings", "q2 earnings", "q1 earnings", "net profit",
        "surpassed consensus", "financial results"
    ],
    "PRODUCT_LAUNCH": [
        "unveils", "launches", "product launch", "autonomous fleet", "robotaxi",
        "next-generation", "announced official", "new chip architecture", "flagship"
    ]
}

class EventClassifier:
    """
    Classifies unstructured financial headlines and text into structured event categories:
    GEOPOLITICAL, MACROECONOMIC, CREDIT_EVENT, MERGER_ACQUISITION, PRODUCT_LAUNCH,
    EARNINGS, REGULATORY, BANKRUPTCY, INTEREST_RATE, MARKET_CRASH, OTHER.
    """
    
    def classify(self, text: str) -> Tuple[str, float]:
        """
        Evaluates input text against financial event taxonomy.
        Returns:
            (event_type, confidence)
        """
        if not text:
            return "OTHER", 0.50
            
        text_lower = text.lower()
        best_event = "OTHER"
        highest_score = 0
        total_matches = 0
        
        scores: Dict[str, int] = {}
        for event, keywords in EVENT_TAXONOMY.items():
            score = 0
            for kw in keywords:
                # Count occurrences with word boundaries where suitable
                matches = len(re.findall(r'\b' + re.escape(kw) + r'\b', text_lower))
                score += (matches * 2) if matches > 0 else 0
                if kw in text_lower and matches == 0:
                    score += 1
            if score > 0:
                scores[event] = score
                total_matches += score
                if score > highest_score:
                    highest_score = score
                    best_event = event

        if highest_score == 0:
            return "OTHER", 0.55
            
        # Confidence calculation based on relative dominance of the winning category
        confidence = min(0.98, max(0.65, round(highest_score / max(1, total_matches * 0.8), 2)))
        return best_event, confidence
