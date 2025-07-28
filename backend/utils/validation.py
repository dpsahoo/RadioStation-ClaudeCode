"""Validation utilities for Radio Calico application."""

import re
import logging
from typing import Optional, Dict, Any
from flask import Request

logger = logging.getLogger(__name__)


def validate_json(request: Request) -> Optional[Dict[str, Any]]:
    """Validate and return JSON data from request."""
    try:
        data = request.get_json()
        if not data:
            logger.warning("No JSON data provided in request")
            return None
        return data
    except Exception as e:
        logger.error(f"Invalid JSON in request: {e}")
        return None


def validate_email(email: str) -> bool:
    """Validate email format."""
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_rating(rating: Any) -> bool:
    """Validate rating value."""
    return rating in ['up', 'down', None]


def validate_required_fields(data: Dict[str, Any], required_fields: list) -> Optional[str]:
    """Validate that all required fields are present."""
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}"
    
    return None


def validate_string_length(value: str, min_length: int = 1, max_length: int = 255) -> bool:
    """Validate string length."""
    if not isinstance(value, str):
        return False
    
    return min_length <= len(value.strip()) <= max_length


def sanitize_string(value: str) -> str:
    """Sanitize string input."""
    if not isinstance(value, str):
        return ""
    
    # Strip whitespace and limit length
    return value.strip()[:500]