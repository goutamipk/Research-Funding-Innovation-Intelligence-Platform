"""
Backend Configuration Module

Clean architecture configuration management using Pydantic Settings.
Reads environment variables from `.env` file.
"""

from app.core.config import Settings, settings

__all__ = ["Settings", "settings"]
