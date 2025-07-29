"""Plugin system for egile-mcp-starter templates."""

from .base import TemplatePlugin
from .registry import TemplateRegistry

__all__ = ["TemplatePlugin", "TemplateRegistry"]
