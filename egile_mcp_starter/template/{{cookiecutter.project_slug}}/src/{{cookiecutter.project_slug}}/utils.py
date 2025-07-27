"""Utility functions for {{ cookiecutter.project_name }}.

This module contains common utility functions used throughout the MCP server.
"""

import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional, Union
from pathlib import Path

logger = logging.getLogger(__name__)


def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """Format a timestamp for display.

    Args:
        timestamp: Datetime object to format, defaults to current time

    Returns:
        Formatted timestamp string
    """
    if timestamp is None:
        timestamp = datetime.now()

    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely load JSON string with error handling.

    Args:
        json_str: JSON string to parse
        default: Default value to return on error

    Returns:
        Parsed JSON data or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f"Failed to parse JSON: {e}")
        return default


def safe_json_dumps(data: Any, default: str = "{}") -> str:
    """Safely serialize data to JSON string with error handling.

    Args:
        data: Data to serialize
        default: Default JSON string to return on error

    Returns:
        JSON string or default value
    """
    try:
        return json.dumps(data, indent=2, default=str)
    except (TypeError, ValueError) as e:
        logger.warning(f"Failed to serialize to JSON: {e}")
        return default


def validate_config(config: Dict[str, Any], required_keys: list) -> bool:
    """Validate that a configuration dictionary contains required keys.

    Args:
        config: Configuration dictionary to validate
        required_keys: List of required key names

    Returns:
        True if all required keys are present, False otherwise
    """
    missing_keys = [key for key in required_keys if key not in config]

    if missing_keys:
        logger.error(f"Missing required configuration keys: {missing_keys}")
        return False

    return True


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing or replacing invalid characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename safe for filesystem use
    """
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    sanitized = filename

    for char in invalid_chars:
        sanitized = sanitized.replace(char, "_")

    # Remove leading/trailing whitespace and dots
    sanitized = sanitized.strip(" .")

    # Ensure the filename is not empty
    if not sanitized:
        sanitized = "unnamed_file"

    return sanitized


def ensure_directory(directory_path: Union[str, Path]) -> Path:
    """Ensure a directory exists, creating it if necessary.

    Args:
        directory_path: Path to the directory

    Returns:
        Path object for the directory

    Raises:
        OSError: If directory creation fails
    """
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_size(file_path: Union[str, Path]) -> int:
    """Get the size of a file in bytes.

    Args:
        file_path: Path to the file

    Returns:
        File size in bytes, or 0 if file doesn't exist
    """
    try:
        return Path(file_path).stat().st_size
    except (OSError, FileNotFoundError):
        return 0


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to a maximum length with optional suffix.

    Args:
        text: Text to truncate
        max_length: Maximum length of the result
        suffix: Suffix to add when truncating

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two dictionaries recursively.

    Args:
        dict1: First dictionary
        dict2: Second dictionary (takes precedence)

    Returns:
        Merged dictionary
    """
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value

    return result


def get_environment_info() -> Dict[str, Any]:
    """Get information about the current environment.

    Returns:
        Dictionary containing environment information
    """
    import platform
    import sys

    return {
        "python_version": sys.version,
        "python_executable": sys.executable,
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "server_info": {
            "name": "{{ cookiecutter.project_name }}",
            "version": "{{ cookiecutter.version }}",
            "framework": "FASTMCP",
        },
    }


class LogFilter:
    """Custom log filter for controlling log output."""

    def __init__(self, level: int = logging.INFO):
        """Initialize the log filter.

        Args:
            level: Minimum log level to allow
        """
        self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter log records based on level.

        Args:
            record: Log record to filter

        Returns:
            True if the record should be logged, False otherwise
        """
        return record.levelno >= self.level


def setup_enhanced_logging(
    log_level: str = "INFO",
    log_file: Optional[Union[str, Path]] = None,
    include_timestamp: bool = True,
    include_module: bool = True,
) -> None:
    """Setup enhanced logging configuration.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file to write logs to
        include_timestamp: Whether to include timestamps in log messages
        include_module: Whether to include module names in log messages
    """
    # Build format string
    format_parts = []

    if include_timestamp:
        format_parts.append("%(asctime)s")

    if include_module:
        format_parts.append("%(name)s")

    format_parts.extend(["%(levelname)s", "%(message)s"])
    log_format = " - ".join(format_parts)

    # Configure logging
    handlers = [logging.StreamHandler()]

    if log_file:
        file_handler = logging.FileHandler(log_file)
        handlers.append(file_handler)

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=handlers,
        force=True,
    )
