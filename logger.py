"""
Professional Logging Module

Provides console logging (colored) and file logging (logs/backend.log)
using standard Python logging module.
"""

from app.core.logger import LOG_FILE_PATH, logger, setup_logger

__all__ = ["logger", "setup_logger", "LOG_FILE_PATH"]
