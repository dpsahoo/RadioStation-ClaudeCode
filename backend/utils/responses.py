"""Response utilities for Radio Calico application."""

from flask import jsonify
from typing import Any, Dict, Optional


def success_response(data: Any = None, message: str = "Success", status_code: int = 200):
    """Create a standardized success response."""
    response_data = {
        'success': True,
        'message': message
    }
    
    if data is not None:
        if isinstance(data, dict):
            response_data.update(data)
        else:
            response_data['data'] = data
    
    return jsonify(response_data), status_code


def error_response(message: str, status_code: int = 400, error_code: Optional[str] = None):
    """Create a standardized error response."""
    response_data = {
        'success': False,
        'error': message,
        'status_code': status_code
    }
    
    if error_code:
        response_data['error_code'] = error_code
    
    return jsonify(response_data), status_code


def validation_error_response(errors: Dict[str, str]):
    """Create a validation error response."""
    return error_response(
        message="Validation failed",
        status_code=422,
        error_code="VALIDATION_ERROR"
    )[0].get_json() | {'validation_errors': errors}, 422