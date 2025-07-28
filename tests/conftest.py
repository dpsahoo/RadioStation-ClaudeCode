"""Test configuration and fixtures for Radio Sahoo tests."""

import os
import pytest
import tempfile
import sqlite3
from unittest.mock import patch, MagicMock
import sys

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.app import create_app
from backend.models.database import init_db
from backend.config import Config


@pytest.fixture(scope='session')
def test_config():
    """Test configuration fixture."""
    config = Config()
    config.DEBUG = True
    config.SECRET_KEY = 'test-secret-key'
    config.DATABASE_PATH = ':memory:'  # Use in-memory database for tests
    config.STREAM_URL = 'http://test-stream.example.com/test.m3u8'
    config.METADATA_URL = 'http://test-stream.example.com/metadata.json'
    config.COVER_ART_URL = 'http://test-stream.example.com/cover.jpg'
    config.ALLOWED_ORIGINS = ['http://localhost', 'http://127.0.0.1']
    return config


@pytest.fixture(scope='session')
def app(test_config):
    """Create and configure a test Flask application."""
    with patch('backend.config.config', test_config):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        with app.app_context():
            init_db()
            yield app


@pytest.fixture
def client(app):
    """Test client fixture."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Test CLI runner fixture."""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def db_connection():
    """Create a test database connection."""
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        # Initialize test database schema
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                track_id TEXT NOT NULL,
                rating TEXT CHECK(rating IN ('up', 'down')) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_fingerprint TEXT NOT NULL,
                UNIQUE(track_id, user_fingerprint)
            )
        ''')
        
        conn.commit()
        yield conn
        
    finally:
        conn.close()
        os.close(db_fd)
        os.unlink(db_path)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        'name': 'John Doe',
        'email': 'john@example.com'
    }


@pytest.fixture
def sample_post_data():
    """Sample post data for testing."""
    return {
        'title': 'Test Post',
        'content': 'This is a test post content',
        'user_id': 1
    }


@pytest.fixture
def sample_rating_data():
    """Sample rating data for testing."""
    return {
        'track_id': 'test-artist-test-song',
        'rating': 'up',
        'user_fingerprint': 'test-fingerprint-123'
    }


@pytest.fixture
def sample_metadata():
    """Sample metadata for testing."""
    return {
        'artist': 'Test Artist',
        'title': 'Test Song',
        'album': 'Test Album',
        'date': '2023',
        'bit_depth': 16,
        'sample_rate': 44100,
        'is_new': True,
        'is_summer': False,
        'is_vidgames': False,
        'prev_artist_1': 'Previous Artist 1',
        'prev_title_1': 'Previous Song 1',
        'prev_artist_2': 'Previous Artist 2',
        'prev_title_2': 'Previous Song 2'
    }


@pytest.fixture
def mock_requests():
    """Mock requests module for external API calls."""
    with patch('requests.get') as mock_get, \
         patch('requests.head') as mock_head, \
         patch('requests.post') as mock_post:
        
        # Mock successful metadata response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {
            'artist': 'Test Artist',
            'title': 'Test Song',
            'album': 'Test Album'
        }
        mock_response.headers = {
            'content-type': 'application/json',
            'date': 'Mon, 01 Jan 2024 00:00:00 GMT'
        }
        
        mock_get.return_value = mock_response
        mock_head.return_value = mock_response
        mock_post.return_value = mock_response
        
        yield {
            'get': mock_get,
            'head': mock_head,
            'post': mock_post,
            'response': mock_response
        }


@pytest.fixture
def auth_headers():
    """Authentication headers for API requests."""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


@pytest.fixture(autouse=True)
def clean_database():
    """Clean database before each test."""
    # This fixture runs automatically before each test
    # Add any cleanup logic here if needed
    yield
    # Cleanup after test if needed


class TestHelpers:
    """Helper methods for testing."""
    
    @staticmethod
    def create_test_user(client, user_data=None):
        """Helper to create a test user."""
        if user_data is None:
            user_data = {
                'name': 'Test User',
                'email': 'test@example.com'
            }
        
        response = client.post('/api/users', 
                             json=user_data,
                             headers={'Content-Type': 'application/json'})
        return response
    
    @staticmethod
    def create_test_post(client, post_data=None):
        """Helper to create a test post."""
        if post_data is None:
            post_data = {
                'title': 'Test Post',
                'content': 'Test content',
                'user_id': 1
            }
        
        response = client.post('/api/posts',
                             json=post_data,
                             headers={'Content-Type': 'application/json'})
        return response
    
    @staticmethod
    def create_test_rating(client, rating_data=None):
        """Helper to create a test rating."""
        if rating_data is None:
            rating_data = {
                'track_id': 'test-track',
                'rating': 'up',
                'user_fingerprint': 'test-fingerprint'
            }
        
        response = client.post('/api/ratings',
                             json=rating_data,
                             headers={'Content-Type': 'application/json'})
        return response


@pytest.fixture
def helpers():
    """Test helpers fixture."""
    return TestHelpers