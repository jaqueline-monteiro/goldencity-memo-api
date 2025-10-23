"""Configuration module for the GoldenCity Memo API.

This module centralizes all configuration settings and provides
a clean way to manage environment-specific configurations.
"""

import logging
import os
from typing import List


class Settings:
    """Application settings and configuration."""

    def __init__(self):
        # API Configuration
        self.API_TITLE: str = "GoldenCity Memo API"
        self.API_DESCRIPTION: str = "A high-performance RESTful API for memo management"
        self.API_VERSION: str = "1.0.0"

        # Server Configuration
        self.HOST: str = os.getenv("HOST", "0.0.0.0")
        self.PORT: int = int(os.getenv("PORT", "8000"))

        # CORS Configuration
        self.ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")

        # Logging Configuration
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logging() -> None:
    """Configure application logging."""
    _settings = Settings()
    logging.basicConfig(
        level=getattr(logging, _settings.LOG_LEVEL.upper()),
        format=_settings.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
        ]
    )

    # Set specific loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


settings = Settings()
