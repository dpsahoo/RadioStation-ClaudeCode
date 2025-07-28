"""Test utility functions and helpers for Radio Sahoo tests."""

import json
import sqlite3
from typing import Dict, Any, Optional
from unittest.mock import MagicMock, patch


class DatabaseTestHelper:
    """Helper class for database testing operations."""
    
    @staticmethod
    def create_test_database(connection: sqlite3.Connection) -> None:
        """Create test database schema."""
        cursor = connection.cursor()
        
        # Create all tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                track_id TEXT NOT NULL,
                rating TEXT CHECK(rating IN ('up', 'down')) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_fingerprint TEXT NOT NULL,
                UNIQUE(track_id, user_fingerprint)
            )
        ''')
        
        connection.commit()
    
    @staticmethod
    def insert_test_data(connection: sqlite3.Connection) -> Dict[str, Any]:
        """Insert test data and return inserted IDs."""
        cursor = connection.cursor()
        
        # Insert test users
        cursor.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            ('Test User 1', 'user1@example.com')
        )
        user1_id = cursor.lastrowid
        
        cursor.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            ('Test User 2', 'user2@example.com')
        )
        user2_id = cursor.lastrowid
        
        # Insert test posts
        cursor.execute(
            'INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)',
            ('Test Post 1', 'Content 1', user1_id)
        )
        post1_id = cursor.lastrowid
        
        cursor.execute(
            'INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)',
            ('Test Post 2', 'Content 2', user2_id)
        )
        post2_id = cursor.lastrowid
        
        # Insert test ratings
        cursor.execute(
            'INSERT INTO ratings (track_id, rating, user_fingerprint) VALUES (?, ?, ?)',
            ('test-track-1', 'up', 'fingerprint1')
        )
        rating1_id = cursor.lastrowid
        
        cursor.execute(
            'INSERT INTO ratings (track_id, rating, user_fingerprint) VALUES (?, ?, ?)',
            ('test-track-1', 'down', 'fingerprint2')
        )
        rating2_id = cursor.lastrowid
        
        connection.commit()
        
        return {
            'user_ids': [user1_id, user2_id],
            'post_ids': [post1_id, post2_id],
            'rating_ids': [rating1_id, rating2_id]
        }


class APITestHelper:
    """Helper class for API testing operations."""
    
    @staticmethod
    def create_user_payload(name: str = "Test User", email: str = "test@example.com") -> Dict[str, str]:
        """Create user payload for API requests."""
        return {
            'name': name,
            'email': email
        }
    
    @staticmethod 
    def create_post_payload(title: str = "Test Post", 
                           content: str = "Test content", 
                           user_id: Optional[int] = None) -> Dict[str, Any]:
        """Create post payload for API requests."""
        payload = {
            'title': title,
            'content': content
        }
        if user_id:
            payload['user_id'] = user_id
        return payload
    
    @staticmethod
    def create_rating_payload(track_id: str = "test-track", 
                             rating: str = "up", 
                             user_fingerprint: str = "test-fingerprint") -> Dict[str, str]:
        """Create rating payload for API requests."""
        return {
            'track_id': track_id,
            'rating': rating,
            'user_fingerprint': user_fingerprint
        }
    
    @staticmethod
    def assert_success_response(response_data: Dict[str, Any], 
                               expected_status: int = 200) -> None:
        """Assert that response is a success response."""
        assert response_data['success'] is True
        assert 'message' in response_data
    
    @staticmethod
    def assert_error_response(response_data: Dict[str, Any], 
                             expected_status: int = 400) -> None:
        """Assert that response is an error response."""
        assert response_data['success'] is False
        assert 'error' in response_data
        assert response_data['status_code'] == expected_status


class MockHelper:
    """Helper class for creating mocks and patches."""
    
    @staticmethod
    def mock_requests_success(json_data: Dict[str, Any] = None) -> MagicMock:
        """Create a mock successful requests response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = json_data or {}
        mock_response.headers = {
            'content-type': 'application/json',
            'date': 'Mon, 01 Jan 2024 00:00:00 GMT'
        }
        return mock_response
    
    @staticmethod
    def mock_requests_error(status_code: int = 404, 
                           error_message: str = "Not Found") -> MagicMock:
        """Create a mock error requests response."""
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.ok = False
        mock_response.statusText = error_message
        mock_response.raise_for_status.side_effect = Exception(error_message)
        return mock_response
    
    @staticmethod
    def patch_database_connection(connection: sqlite3.Connection):
        """Create a context manager for patching database connections."""
        return patch('backend.models.database.get_db_connection', return_value=connection)
    
    @staticmethod
    def create_mock_metadata() -> Dict[str, Any]:
        """Create mock metadata for testing."""
        return {
            'artist': 'Mock Artist',
            'title': 'Mock Song',
            'album': 'Mock Album',
            'date': '2024',
            'bit_depth': 16,
            'sample_rate': 44100,
            'is_new': True,
            'is_summer': False,
            'is_vidgames': False,
            'prev_artist_1': 'Previous Artist 1',
            'prev_title_1': 'Previous Song 1',
            'prev_artist_2': 'Previous Artist 2',
            'prev_title_2': 'Previous Song 2',
            'prev_artist_3': 'Previous Artist 3',
            'prev_title_3': 'Previous Song 3'
        }


class ValidationTestHelper:
    """Helper class for validation testing."""
    
    @staticmethod
    def get_valid_emails() -> list:
        """Get list of valid email addresses for testing."""
        return [
            'test@example.com',
            'user.name@domain.co.uk',
            'test123@test-domain.org',
            'valid.email+tag@example.com',
            'user@sub.domain.com'
        ]
    
    @staticmethod
    def get_invalid_emails() -> list:
        """Get list of invalid email addresses for testing."""
        return [
            'invalid-email',
            '@domain.com',
            'test@',
            'test.domain.com',
            '',
            'test@domain',
            'test space@domain.com',
            'test..double.dot@domain.com'
        ]
    
    @staticmethod
    def get_valid_ratings() -> list:
        """Get list of valid rating values for testing."""
        return ['up', 'down', None]
    
    @staticmethod
    def get_invalid_ratings() -> list:
        """Get list of invalid rating values for testing."""
        return ['invalid', 'UP', 'DOWN', '', 'like', 'dislike', 123, []]


class TestDataGenerator:
    """Helper class for generating test data."""
    
    @staticmethod
    def generate_users(count: int = 3) -> list:
        """Generate list of user data for testing."""
        users = []
        for i in range(count):
            users.append({
                'name': f'Test User {i+1}',
                'email': f'user{i+1}@example.com'
            })
        return users
    
    @staticmethod
    def generate_posts(count: int = 3, user_id: int = 1) -> list:
        """Generate list of post data for testing."""
        posts = []
        for i in range(count):
            posts.append({
                'title': f'Test Post {i+1}',
                'content': f'This is test post content {i+1}',
                'user_id': user_id
            })
        return posts
    
    @staticmethod
    def generate_ratings(track_id: str = "test-track", count: int = 3) -> list:
        """Generate list of rating data for testing."""
        ratings = []
        rating_values = ['up', 'down', 'up']  # Cycle through values
        
        for i in range(count):
            ratings.append({
                'track_id': track_id,
                'rating': rating_values[i % len(rating_values)],
                'user_fingerprint': f'fingerprint-{i+1}'
            })
        return ratings
    
    @staticmethod
    def generate_large_string(length: int = 1000) -> str:
        """Generate a large string for testing string length limits."""
        return 'A' * length


class AssertionHelper:
    """Helper class for common test assertions."""
    
    @staticmethod
    def assert_valid_user_response(data: Dict[str, Any]) -> None:
        """Assert that data contains valid user response fields."""
        required_fields = ['id', 'name', 'email', 'created_at']
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        assert isinstance(data['id'], int)
        assert isinstance(data['name'], str)
        assert isinstance(data['email'], str)
        assert data['name'].strip() != ''
        assert '@' in data['email']
    
    @staticmethod
    def assert_valid_post_response(data: Dict[str, Any]) -> None:
        """Assert that data contains valid post response fields."""
        required_fields = ['id', 'title', 'content', 'created_at']
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        assert isinstance(data['id'], int)
        assert isinstance(data['title'], str)
        assert data['title'].strip() != ''
    
    @staticmethod
    def assert_valid_rating_response(data: Dict[str, Any]) -> None:
        """Assert that data contains valid rating response fields."""
        required_fields = ['track_id', 'ratings', 'user_rating']
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        assert isinstance(data['track_id'], str)
        assert isinstance(data['ratings'], dict)
        assert 'up' in data['ratings']
        assert 'down' in data['ratings']
        assert isinstance(data['ratings']['up'], int)
        assert isinstance(data['ratings']['down'], int)