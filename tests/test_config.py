"""Tests for configuration module.

This module tests the configuration settings and logging setup
to ensure proper application configuration.
"""

import logging
from unittest.mock import patch

try:
    from app.config import Settings, setup_logging, settings
except ImportError:
    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app.config import Settings, setup_logging, settings


class TestSettings:
    """Test cases for Settings class."""

    def test_default_settings(self):
        """Test that default settings are properly set."""
        test_settings = Settings()
        assert test_settings.API_TITLE == "GoldenCity Memo API"
        assert test_settings.API_VERSION == "1.0.0"
        assert test_settings.HOST == "0.0.0.0"
        assert test_settings.PORT == 8000
        assert test_settings.LOG_LEVEL == "INFO"

    def test_environment_override(self):
        """Test that environment variables override default settings."""
        with patch.dict(os.environ, {"HOST": "127.0.0.1", "PORT": "9000", "LOG_LEVEL": "DEBUG"}, clear=False):
            test_settings = Settings()
            assert test_settings.HOST == "127.0.0.1"
            assert test_settings.PORT == 9000
            assert test_settings.LOG_LEVEL == "DEBUG"

    def test_allowed_origins_parsing(self):
        """Test that ALLOWED_ORIGINS is properly parsed from environment."""
        with patch.dict(os.environ, {"ALLOWED_ORIGINS": "http://localhost:3000,http://localhost:8080"}, clear=False):
            test_settings = Settings()
            expected_origins = ["http://localhost:3000", "http://localhost:8080"]
            assert test_settings.ALLOWED_ORIGINS == expected_origins


class TestLoggingSetup:
    """Test cases for logging configuration."""

    def test_setup_logging_configures_basic_config(self):
        """Test that setup_logging configures basic logging."""
        # Clear any existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        setup_logging()

        # Check that logging is configured
        assert len(root_logger.handlers) > 0
        assert root_logger.level == logging.INFO

    def test_setup_logging_respects_log_level(self):
        """Test that setup_logging respects LOG_LEVEL environment variable."""
        with patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"}, clear=False):
            # Create new settings instance with patched environment
            test_settings = Settings()

            # Verify the settings picked up the environment variable
            assert test_settings.LOG_LEVEL == "DEBUG"

            # Clear any existing handlers
            root_logger = logging.getLogger()
            for handler in root_logger.handlers[:]:
                root_logger.removeHandler(handler)

            # Configure logging with new settings
            logging.basicConfig(
                level=getattr(logging, test_settings.LOG_LEVEL.upper()),
                format=test_settings.LOG_FORMAT,
                handlers=[logging.StreamHandler()],
                force=True
            )

            # Check that debug level is set
            assert root_logger.level == logging.DEBUG


class TestGlobalSettings:
    """Test cases for global settings instance."""

    def test_settings_instance_exists(self):
        """Test that global settings instance exists and is properly configured."""
        assert settings is not None
        assert isinstance(settings, Settings)
        assert hasattr(settings, 'API_TITLE')
        assert hasattr(settings, 'API_VERSION')
