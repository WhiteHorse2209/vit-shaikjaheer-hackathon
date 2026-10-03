import re
from typing import Tuple, Optional

# Supported universe of companies with canonical tickers, formal names, and identifying keywords
COMPANY_TICKER_MAP = {
    "AAPL": {
        "name": "Apple Inc.",
        "keywords": ["apple", "apple inc", "iphone", "ipad", "macbook", "tim cook", "aapl"]
    },
    "MSFT": {
        "name": "Microsoft Corporation",
        "keywords": ["microsoft", "microsoft corp", "azure", "windows", "satya nadella", "xbox", "msft"]
    },
    "NVDA": {
        "name": "NVIDIA Corporation",
        "keywords": ["nvidia", "nvidia corp", "jensen huang", "geforce", "blackwell", "cuda", "nvda"]
    },
    "AMZN": {
        "name": "Amazon.com Inc.",
        "keywords": ["amazon", "amazon.com", "aws", "andy jassy", "jeff bezos", "prime", "amzn"]
    },
    "GOOGL": {
        "name": "Alphabet Inc.",
        "keywords": ["alphabet", "google", "sundar pichai", "youtube", "deepmind", "waymo", "googl", "goog"]
    },
    "META": {
        "name": "Meta Platforms Inc.",
        "keywords": ["meta", "meta platforms", "facebook", "instagram", "whatsapp", "mark zuckerberg", "metaverse"]
    },
    "TSLA": {
        "name": "Tesla Inc.",
        "keywords": ["tesla", "tesla inc", "elon musk", "cybertruck", "gigafactory", "tsla"]
    },
    "JPM": {
        "name": "JPMorgan Chase & Co.",
        "keywords": ["jpmorgan", "jpmorgan chase", "chase bank", "jamie dimon", "jpm"]
    },
    "V": {
        "name": "Visa Inc.",
        "keywords": ["visa", "visa inc", "visa payment", "visa network"]
    },
    "NFLX": {
        "name": "Netflix Inc.",
        "keywords": ["netflix", "netflix inc", "ted sarandos", "streaming", "nflx"]
    }
}

def extract_company_and_ticker(text: str) -> Tuple[str, str]:
    """
    Scans headline/content text for mentions of tracked entities.
    Returns (company_name, ticker). If no match found, returns ('General Market', 'MACRO').
    """
    if not text:
        return ("General Market", "MACRO")
    
    text_lower = text.lower()
    
    # Priority check: look for word boundaries around company names/tickers/keywords
    for ticker, info in COMPANY_TICKER_MAP.items():
        for kw in info["keywords"]:
            # Match word boundary
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text_lower):
                return (info["name"], ticker)
                
    return ("General Market", "MACRO")
