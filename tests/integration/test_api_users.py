"""Integration tests for users API endpoints."""

import pytest
import json


class TestUsersAPI:
    """Test cases for users API endpoints."""
    
    def test_create_user_success(self, client, sample_user_data, auth_headers):
        """Test successful user creation."""
        response = client.post('/api/users',
                             json=sample_user_data,
                             headers=auth_headers)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['name'] == sample_user_data['name']
        assert data['email'] == sample_user_data['email']
        assert 'id' in data
    
    def test_create_user_missing_fields(self, client, auth_headers):
        """Test user creation with missing required fields."""
        incomplete_data = {'name': 'John Doe'}
        
        response = client.post('/api/users',
                             json=incomplete_data,
                             headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'email' in data['error']
    
    def test_create_user_invalid_email(self, client, auth_headers):
        """Test user creation with invalid email."""
        invalid_data = {
            'name': 'John Doe',
            'email': 'invalid-email'
        }
        
        response = client.post('/api/users',
                             json=invalid_data,
                             headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'Invalid email' in data['error']
    
    def test_create_user_duplicate_email(self, client, sample_user_data, auth_headers):
        """Test user creation with duplicate email."""
        # Create first user
        client.post('/api/users',
                   json=sample_user_data,
                   headers=auth_headers)
        
        # Try to create second user with same email
        duplicate_data = {
            'name': 'Jane Doe',
            'email': sample_user_data['email']
        }
        
        response = client.post('/api/users',
                             json=duplicate_data,
                             headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'already exists' in data['error']
    
    def test_get_users_empty(self, client):
        """Test getting users when none exist."""
        response = client.get('/api/users')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['users'] == []
        assert data['count'] == 0
    
    def test_get_users_with_data(self, client, auth_headers):
        """Test getting users with existing data."""
        # Create multiple users
        users_data = [
            {'name': 'John Doe', 'email': 'john@example.com'},
            {'name': 'Jane Smith', 'email': 'jane@example.com'}
        ]
        
        for user_data in users_data:
            client.post('/api/users', json=user_data, headers=auth_headers)
        
        # Get all users
        response = client.get('/api/users')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['users']) == 2
        assert data['count'] == 2
    
    def test_get_users_with_limit(self, client, auth_headers):
        """Test getting users with limit parameter."""
        # Create multiple users
        for i in range(5):
            user_data = {
                'name': f'User {i}',
                'email': f'user{i}@example.com'
            }
            client.post('/api/users', json=user_data, headers=auth_headers)
        
        # Get users with limit
        response = client.get('/api/users?limit=3')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['users']) == 3
    
    def test_get_users_limit_enforcement(self, client):
        """Test users limit enforcement."""
        # Request with limit over 100
        response = client.get('/api/users?limit=150')
        
        assert response.status_code == 200
        # Should still work but limit should be capped
    
    def test_get_user_by_id_success(self, client, sample_user_data, auth_headers):
        """Test getting user by ID successfully."""
        # Create user
        create_response = client.post('/api/users',
                                    json=sample_user_data,
                                    headers=auth_headers)
        user_id = create_response.get_json()['id']
        
        # Get user by ID
        response = client.get(f'/api/users/{user_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['id'] == user_id
        assert data['name'] == sample_user_data['name']
        assert data['email'] == sample_user_data['email']
    
    def test_get_user_by_id_not_found(self, client):
        """Test getting non-existent user by ID."""
        response = client.get('/api/users/99999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False
        assert 'not found' in data['error']
    
    def test_create_user_invalid_json(self, client, auth_headers):
        """Test user creation with invalid JSON."""
        response = client.post('/api/users',
                             data='invalid json',
                             headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_create_user_email_normalization(self, client, auth_headers):
        """Test email normalization (lowercase, trimmed)."""
        user_data = {
            'name': '  John Doe  ',
            'email': '  JOHN@EXAMPLE.COM  '
        }
        
        response = client.post('/api/users',
                             json=user_data,
                             headers=auth_headers)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['name'] == 'John Doe'
        assert data['email'] == 'john@example.com'