"""Unit tests for utility functions."""

import pytest
from unittest.mock import MagicMock

from backend.utils.validation import (
    validate_json, validate_email, validate_rating,
    validate_required_fields, validate_string_length, sanitize_string
)
from backend.utils.responses import success_response, error_response


class TestValidation:
    """Test cases for validation utilities."""
    
    def test_validate_json_valid(self):
        """Test validation with valid JSON."""
        mock_request = MagicMock()
        mock_request.get_json.return_value = {'key': 'value'}
        
        result = validate_json(mock_request)
        
        assert result == {'key': 'value'}
    
    def test_validate_json_empty(self):
        """Test validation with empty JSON."""
        mock_request = MagicMock()
        mock_request.get_json.return_value = None
        
        result = validate_json(mock_request)
        
        assert result is None
    
    def test_validate_json_invalid(self):
        """Test validation with invalid JSON."""
        mock_request = MagicMock()
        mock_request.get_json.side_effect = Exception("Invalid JSON")
        
        result = validate_json(mock_request)
        
        assert result is None
    
    def test_validate_email_valid(self):
        """Test email validation with valid emails."""
        valid_emails = [
            'test@example.com',
            'user.name@domain.co.uk',
            'test123@test-domain.org'
        ]
        
        for email in valid_emails:
            assert validate_email(email) is True
    
    def test_validate_email_invalid(self):
        """Test email validation with invalid emails."""
        invalid_emails = [
            'invalid-email',
            '@domain.com',
            'test@',
            'test.domain.com',
            '',
            None,
            123
        ]
        
        for email in invalid_emails:
            assert validate_email(email) is False
    
    def test_validate_rating_valid(self):
        """Test rating validation with valid values."""
        valid_ratings = ['up', 'down', None]
        
        for rating in valid_ratings:
            assert validate_rating(rating) is True
    
    def test_validate_rating_invalid(self):
        """Test rating validation with invalid values."""
        invalid_ratings = ['invalid', 'UP', 'DOWN', '', 'like', 'dislike', 123]
        
        for rating in invalid_ratings:
            assert validate_rating(rating) is False
    
    def test_validate_required_fields_success(self):
        """Test required fields validation with all fields present."""
        data = {'name': 'John', 'email': 'john@example.com', 'age': 25}
        required = ['name', 'email']
        
        result = validate_required_fields(data, required)
        
        assert result is None
    
    def test_validate_required_fields_missing(self):
        """Test required fields validation with missing fields."""
        data = {'name': 'John'}
        required = ['name', 'email', 'age']
        
        result = validate_required_fields(data, required)
        
        assert result is not None
        assert 'email' in result
        assert 'age' in result
    
    def test_validate_required_fields_none_values(self):
        """Test required fields validation with None values."""
        data = {'name': 'John', 'email': None}
        required = ['name', 'email']
        
        result = validate_required_fields(data, required)
        
        assert result is not None
        assert 'email' in result
    
    def test_validate_string_length_valid(self):
        """Test string length validation with valid strings."""
        assert validate_string_length('Hello') is True
        assert validate_string_length('A', 1, 10) is True
        assert validate_string_length('Test string', 5, 20) is True
    
    def test_validate_string_length_invalid(self):
        """Test string length validation with invalid strings."""
        assert validate_string_length('') is False
        assert validate_string_length('A', 2, 10) is False
        assert validate_string_length('Very long string', 1, 5) is False
        assert validate_string_length(123) is False
        assert validate_string_length(None) is False
    
    def test_sanitize_string_valid(self):
        """Test string sanitization with valid input."""
        assert sanitize_string('  Hello World  ') == 'Hello World'
        assert sanitize_string('Test') == 'Test'
    
    def test_sanitize_string_invalid(self):
        """Test string sanitization with invalid input."""
        assert sanitize_string(123) == ''
        assert sanitize_string(None) == ''
    
    def test_sanitize_string_long(self):
        """Test string sanitization with long input."""
        long_string = 'A' * 600
        result = sanitize_string(long_string)
        
        assert len(result) == 500


class TestResponses:
    """Test cases for response utilities."""
    
    def test_success_response_simple(self):
        """Test simple success response."""
        response, status_code = success_response()
        
        assert status_code == 200
        response_data = response.get_json()
        assert response_data['success'] is True
        assert response_data['message'] == 'Success'
    
    def test_success_response_with_data(self):
        """Test success response with data."""
        data = {'user_id': 123, 'name': 'John'}
        response, status_code = success_response(data, 'User created', 201)
        
        assert status_code == 201
        response_data = response.get_json()
        assert response_data['success'] is True
        assert response_data['message'] == 'User created'
        assert response_data['user_id'] == 123
        assert response_data['name'] == 'John'
    
    def test_success_response_with_data_object(self):
        """Test success response with non-dict data."""
        data = ['item1', 'item2', 'item3']
        response, status_code = success_response(data)
        
        assert status_code == 200
        response_data = response.get_json()
        assert response_data['success'] is True
        assert response_data['data'] == ['item1', 'item2', 'item3']
    
    def test_error_response_simple(self):
        """Test simple error response."""
        response, status_code = error_response('Something went wrong')
        
        assert status_code == 400
        response_data = response.get_json()
        assert response_data['success'] is False
        assert response_data['error'] == 'Something went wrong'
        assert response_data['status_code'] == 400
    
    def test_error_response_with_code(self):
        """Test error response with error code."""
        response, status_code = error_response(
            'Validation failed', 
            422, 
            'VALIDATION_ERROR'
        )
        
        assert status_code == 422
        response_data = response.get_json()
        assert response_data['success'] is False
        assert response_data['error'] == 'Validation failed'
        assert response_data['status_code'] == 422
        assert response_data['error_code'] == 'VALIDATION_ERROR'