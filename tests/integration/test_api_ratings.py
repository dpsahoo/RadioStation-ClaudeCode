"""Integration tests for ratings API endpoints."""

import pytest
import json


class TestRatingsAPI:
    """Test cases for ratings API endpoints."""
    
    def test_create_rating_success(self, client, sample_rating_data, auth_headers):
        """Test successful rating creation."""
        response = client.post('/api/ratings', 
                             json=sample_rating_data,
                             headers=auth_headers)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['track_id'] == sample_rating_data['track_id']
        assert data['rating'] == sample_rating_data['rating']
    
    def test_create_rating_missing_fields(self, client, auth_headers):
        """Test rating creation with missing required fields."""
        incomplete_data = {'track_id': 'test-track'}
        
        response = client.post('/api/ratings',
                             json=incomplete_data,
                             headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_create_rating_invalid_rating(self, client, sample_rating_data, auth_headers):
        """Test rating creation with invalid rating value."""
        sample_rating_data['rating'] = 'invalid'
        
        response = client.post('/api/ratings',
                             json=sample_rating_data,
                             headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'must be' in data['error']
    
    def test_update_existing_rating(self, client, sample_rating_data, auth_headers):
        """Test updating an existing rating."""
        # Create initial rating
        client.post('/api/ratings',
                   json=sample_rating_data,
                   headers=auth_headers)
        
        # Update rating
        sample_rating_data['rating'] = 'down'
        response = client.post('/api/ratings',
                             json=sample_rating_data,
                             headers=auth_headers)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['rating'] == 'down'
    
    def test_remove_rating(self, client, sample_rating_data, auth_headers):
        """Test removing a rating."""
        # Create initial rating
        client.post('/api/ratings',
                   json=sample_rating_data,
                   headers=auth_headers)
        
        # Remove rating
        sample_rating_data['rating'] = None
        response = client.post('/api/ratings',
                             json=sample_rating_data,
                             headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'removed' in data['message']
    
    def test_get_track_ratings(self, client, sample_rating_data):
        """Test getting ratings for a track."""
        # Create some ratings
        client.post('/api/ratings', json=sample_rating_data)
        
        # Create another rating with different user
        other_rating = sample_rating_data.copy()
        other_rating['user_fingerprint'] = 'different-user'
        other_rating['rating'] = 'down'
        client.post('/api/ratings', json=other_rating)
        
        # Get track ratings
        track_id = sample_rating_data['track_id']
        fingerprint = sample_rating_data['user_fingerprint']
        response = client.get(f'/api/ratings/{track_id}?fingerprint={fingerprint}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['track_id'] == track_id
        assert data['ratings']['up'] == 1
        assert data['ratings']['down'] == 1
        assert data['user_rating'] == 'up'
    
    def test_get_track_ratings_no_fingerprint(self, client, sample_rating_data):
        """Test getting track ratings without user fingerprint."""
        # Create rating
        client.post('/api/ratings', json=sample_rating_data)
        
        # Get track ratings without fingerprint
        track_id = sample_rating_data['track_id']
        response = client.get(f'/api/ratings/{track_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['user_rating'] is None
        assert data['ratings']['up'] == 1
    
    def test_get_user_ratings(self, client, sample_rating_data):
        """Test getting ratings by user."""
        # Create multiple ratings for the same user
        fingerprint = sample_rating_data['user_fingerprint']
        
        # First rating
        client.post('/api/ratings', json=sample_rating_data)
        
        # Second rating
        sample_rating_data['track_id'] = 'another-track'
        sample_rating_data['rating'] = 'down'
        client.post('/api/ratings', json=sample_rating_data)
        
        # Get user ratings
        response = client.get(f'/api/ratings/user/{fingerprint}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['user_fingerprint'] == fingerprint
        assert len(data['ratings']) == 2
        assert data['count'] == 2
    
    def test_get_user_ratings_with_limit(self, client, sample_rating_data):
        """Test getting user ratings with limit."""
        fingerprint = sample_rating_data['user_fingerprint']
        
        # Create multiple ratings
        for i in range(5):
            rating_data = sample_rating_data.copy()
            rating_data['track_id'] = f'track-{i}'
            client.post('/api/ratings', json=rating_data)
        
        # Get user ratings with limit
        response = client.get(f'/api/ratings/user/{fingerprint}?limit=3')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['ratings']) == 3
    
    def test_get_user_ratings_limit_max(self, client, sample_rating_data):
        """Test user ratings limit enforcement."""
        fingerprint = sample_rating_data['user_fingerprint']
        
        # Request with limit over 100
        response = client.get(f'/api/ratings/user/{fingerprint}?limit=150')
        
        assert response.status_code == 200
        # Should still work but limit should be capped at 100
    
    def test_create_rating_invalid_json(self, client, auth_headers):
        """Test rating creation with invalid JSON."""
        response = client.post('/api/ratings',
                             data='invalid json',
                             headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_get_track_ratings_nonexistent(self, client):
        """Test getting ratings for non-existent track."""
        response = client.get('/api/ratings/nonexistent-track')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['ratings']['up'] == 0
        assert data['ratings']['down'] == 0
    
    def test_get_user_ratings_nonexistent(self, client):
        """Test getting ratings for non-existent user."""
        response = client.get('/api/ratings/user/nonexistent-user')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['ratings']) == 0