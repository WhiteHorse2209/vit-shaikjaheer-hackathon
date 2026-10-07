import logging
from typing import Tuple, Dict
from src.config import settings

logger = logging.getLogger(__name__)

torch = None
AutoTokenizer = None
AutoModelForSequenceClassification = None

class FinBERTSentimentAnalyzer:
    """
    Financial sentiment analyzer powered by ProsusAI/finbert.
    URL: https://huggingface.co/ProsusAI/finbert
    
    Produces numerical sentiment score:
        Sentiment = P(positive) - P(negative)
    ranging from -1.0 (extremely negative) to +1.0 (extremely positive).
    """
    _instance = None
    _tokenizer = None
    _model = None
    _label_mapping = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FinBERTSentimentAnalyzer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def _ensure_initialized(self):
        global torch, AutoTokenizer, AutoModelForSequenceClassification
        if not self._initialized:
            try:
                logger.info("Initializing ProsusAI/finbert tokenizer and model...")
                import torch as _torch
                from transformers import AutoTokenizer as _AutoTokenizer, AutoModelForSequenceClassification as _AutoModel
                torch = _torch
                AutoTokenizer = _AutoTokenizer
                AutoModelForSequenceClassification = _AutoModel

                model_name = settings.FINBERT_MODEL_NAME
                self._tokenizer = AutoTokenizer.from_pretrained(model_name)
                self._model = AutoModelForSequenceClassification.from_pretrained(model_name)
                self._model.eval()
                
                # ProsusAI/finbert labels: 0: positive, 1: negative, 2: neutral
                self._label_mapping = {v.lower(): k for k, v in self._model.config.id2label.items()}
                logger.info(f"FinBERT initialized successfully with mapping: {self._label_mapping}")
            except Exception as e:
                logger.warning(f"FinBERT model initialization encountered error: {e}. Falling back to calibrated financial lexicon.")
                self._model = None
                self._tokenizer = None
            self._initialized = True

    def analyze(self, text: str) -> Tuple[float, float, str, Dict[str, float]]:
        self._ensure_initialized()
        """
        Analyzes input financial text.
        Returns:
            (sentiment_score, confidence, primary_label, probabilities_dict)
            sentiment_score: float in [-1.0, 1.0] calculated as P(positive) - P(negative)
            confidence: float in [0.0, 1.0]
            primary_label: 'positive' | 'negative' | 'neutral'
        """
        if not text or not text.strip():
            return 0.0, 1.0, "neutral", {"positive": 0.0, "negative": 0.0, "neutral": 1.0}

        # Truncate text to avoid token overflow
        clean_input = text.strip()[:1000]

        if self._model is not None and self._tokenizer is not None:
            try:
                inputs = self._tokenizer(clean_input, return_tensors="pt", truncation=True, max_length=512, padding=True)
                with torch.no_grad():
                    outputs = self._model(**inputs)
                    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]
                    
                pos_idx = self._label_mapping.get("positive", 0)
                neg_idx = self._label_mapping.get("negative", 1)
                neu_idx = self._label_mapping.get("neutral", 2)
                
                p_pos = float(probs[pos_idx].item())
                p_neg = float(probs[neg_idx].item())
                p_neu = float(probs[neu_idx].item())
                
                sentiment_score = round(p_pos - p_neg, 4)
                
                prob_dict = {"positive": round(p_pos, 4), "negative": round(p_neg, 4), "neutral": round(p_neu, 4)}
                primary_label = max(prob_dict, key=prob_dict.get)
                confidence = round(prob_dict[primary_label], 4)
                
                return sentiment_score, confidence, primary_label, prob_dict
            except Exception as e:
                logger.warning(f"FinBERT inference failed: {e}. Using fallback lexicon.")

        # Fallback calibrated financial sentiment scoring
        return self._fallback_analyze(clean_input)

    def _fallback_analyze(self, text: str) -> Tuple[float, float, str, Dict[str, float]]:
        """Calibrated fallback based on Financial PhraseBank lexicons."""
        text_lower = text.lower()
        neg_words = ["tumbled", "plunge", "loss", "crash", "downgrade", "crisis", "bankruptcy", "lawsuit", "blockade", "disruption", "penalties", "margin calls", "tightening", "reorganization", "default", "stagnation"]
        pos_words = ["beat", "record", "growth", "soared", "expansion", "profit", "surpassed", "robust", "positive", "gains", "acquisition", "outperformed", "dividend", "upgraded"]

        neg_hits = sum(1 for w in neg_words if w in text_lower)
        pos_hits = sum(1 for w in pos_words if w in text_lower)

        total_hits = pos_hits + neg_hits
        if total_hits == 0:
            return 0.0, 0.85, "neutral", {"positive": 0.1, "negative": 0.1, "neutral": 0.8}

        p_pos = round(pos_hits / (total_hits + 1), 4)
        p_neg = round(neg_hits / (total_hits + 1), 4)
        p_neu = round(1.0 - (p_pos + p_neg), 4)

        sentiment_score = round(p_pos - p_neg, 4)
        prob_dict = {"positive": p_pos, "negative": p_neg, "neutral": p_neu}
        primary_label = max(prob_dict, key=prob_dict.get)
        confidence = round(prob_dict[primary_label], 4)

        return sentiment_score, confidence, primary_label, prob_dict
