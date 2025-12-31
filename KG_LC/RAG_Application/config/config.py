"""Configuration module."""

import os
from typing import Optional

class Config:
    """Configuration settings for RAG Application."""

    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    # Document Processing
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    MAX_CHUNK_PER_DOCUMENT: int = int(os.getenv("MAX_CHUNK_PER_DOCUMENT", "1000"))

    # RAG Settings
    RETRIEVAL_K: int = int(os.getenv("RETRIEVAL_K", "4"))
    RETRIEVAL_K_FALLBACK: int = int(os.getenv("RETRIEVAL_K_FALLBACK", "8"))

    # Quality Assessment
    QUALITY_THRESHOLD: float = float(os.getenv("QUALITY_THRESHOLD", "0.6"))
    COMPLETENESS_WEIGHT: float = 0.3
    SPECIFICITY_WEIGHT: float = 0.25
    RELEVANCE_WEIGHT: float = 0.25
    CONFIDENCE_WEIGHT: float = 0.2

    # Hallucination Detection
    HALLUCINATION_THRESHOLD: float = float(os.getenv("HALLUCINATION_THRESHOLD", "0.5"))
    CHECK_HALLUCINATION: bool = os.getenv("CHECK_HALLUCINATION", "true").lower() == "true"

    # Fallback Strategy
    ENABLE_FALLBACK: bool = os.getenv("ENABLE_FALLBACK", "true").lower() == "true"
    FALLBACK_STRATEGIES: list = ["increase_context", "strict_matching", "query_expansion"]

    # Index Settings
    INDEX_PERSIST_DIR: str = os.getenv("INDEX_PERSIST_DIR", "indexes")
    SESSION_DIR: str = os.getenv("SESSION_DIR", "sessions")
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    EXPORT_DIR: str = os.getenv("EXPORT_DIR", "exports")

    # Streamlit Settings
    STREAMLIT_THEME: str = os.getenv("STREAMLIT_THEME", "light")
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))

    @classmethod
    def validate(cls):
        """Validate configuration."""
        errors = []

        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required")

        if not all(0 < weight <= 1 for weight in [
            cls.COMPLETENESS_WEIGHT,
            cls.SPECIFICITY_WEIGHT,
            cls.RELEVANCE_WEIGHT,
            cls.CONFIDENCE_WEIGHT
        ]):
            errors.append("All weight values must be between 0 and 1")

        if not (0 <= cls.QUALITY_THRESHOLD <= 1):
            errors.append("QUALITY_THRESHOLD must be between 0 and 1")

        if not (0 <= cls.HALLUCINATION_THRESHOLD <= 1):
            errors.append("HALLUCINATION_THRESHOLD must be between 0 and 1")

        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))

        return True
