import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-NLP Financial Risk Engine"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    MODE: str = os.getenv("MODE", "DEMO")  # "LIVE" or "DEMO"
    
    # API Keys (optional for DEMO mode)
    NEWSAPI_KEY: str = os.getenv("NEWSAPI_KEY", "")
    
    # Paths
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    SAMPLE_NEWS_PATH: Path = BASE_DIR / "data" / "sample_news.json"
    PORTFOLIO_PATH: Path = BASE_DIR / "data" / "portfolio.csv"
    STRESS_SCENARIOS_PATH: Path = BASE_DIR / "data" / "stress_scenarios.csv"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/data/risk_engine.db")
    
    # NLP Models
    FINBERT_MODEL_NAME: str = "ProsusAI/finbert"
    USE_GPU: bool = False
    
    # Stress Testing Threshold
    IMPACT_THRESHOLD_TRIGGER: float = 7.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
