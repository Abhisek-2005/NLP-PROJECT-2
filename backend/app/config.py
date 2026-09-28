import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseModel):
    PROJECT_NAME: str = "Resume–Job Description Matching Using NLP"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    
    # Storage
    DATA_DIR: Path = BASE_DIR / "data"
    SAMPLE_DIR: Path = BASE_DIR / "sample_data"
    DB_PATH: Path = BASE_DIR / "data" / "resume_matcher.db"
    
    # NLP Model Settings
    # Default model: lightweight, fast, top performance for sentence embeddings
    MODEL_NAME: str = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
    ALLOW_TFIDF_FALLBACK: bool = os.getenv("ALLOW_TFIDF_FALLBACK", "True").lower() in ("true", "1", "yes")
    
    # Scoring weights (default: 45% semantic similarity, 40% skills match, 15% keyword overlap)
    SEMANTIC_WEIGHT: float = float(os.getenv("SEMANTIC_WEIGHT", "0.45"))
    SKILL_WEIGHT: float = float(os.getenv("SKILL_WEIGHT", "0.40"))
    KEYWORD_WEIGHT: float = float(os.getenv("KEYWORD_WEIGHT", "0.15"))
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

settings = Settings()

# Ensure directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
