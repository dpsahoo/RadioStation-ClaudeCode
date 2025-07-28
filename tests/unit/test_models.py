"""Unit tests for database models."""

import pytest
import sqlite3
from unittest.mock import patch, MagicMock

from backend.models.user import User
from backend.models.post import Post
from backend.models.rating import Rating
from backend.models.database import get_db_connection, init_db


class TestUserModel:
    """Test cases for User model."""
    
    def test_create_user_success(self, db_connection):
        """Test successful user creation."""
        with patch('backend.models.user.get_db_connection', return_value=db_connection):
            user = User.create('John Doe', 'john@example.com')
            
            assert user is not None
            assert user.name == 'John Doe'
            assert user.email == 'john@example.com'
            assert user.id is not None
    
    def test_create_user_duplicate_email(self, db_connection):
        """Test user creation with duplicate email fails."""
        with patch('backend.models.user.get_db_connection', return_value=db_connection):
            # Create first user
            user1 = User.create('John Doe', 'john@example.com')
            assert user1 is not None
            
            # Try to create second user with same email
            user2 = User.create('Jane Doe', 'john@example.com')
            assert user2 is None
    
    def test_get_user_by_id(self, db_connection):
        """Test retrieving user by ID."""
        with patch('backend.models.user.get_db_connection', return_value=db_connection):
            # Create user
            created_user = User.create('John Doe', 'john@example.com')
            
            # Retrieve user
            retrieved_user = User.get_by_id(created_user.id)
            
            assert retrieved_user is not None
            assert retrieved_user.id == created_user.id
            assert retrieved_user.name == 'John Doe'
            assert retrieved_user.email == 'john@example.com'
    
    def test_get_user_by_email(self, db_connection):
        """Test retrieving user by email."""
        with patch('backend.models.user.get_db_connection', return_value=db_connection):
            # Create user
            User.create('John Doe', 'john@example.com')
            
            # Retrieve user by email
            user = User.get_by_email('john@example.com')
            
            assert user is not None
            assert user.name == 'John Doe'
            assert user.email == 'john@example.com'
    
    def test_get_all_users(self, db_connection):
        """Test retrieving all users."""
        with patch('backend.models.user.get_db_connection', return_value=db_connection):
            # Create multiple users
            User.create('John Doe', 'john@example.com')
            User.create('Jane Smith', 'jane@example.com')
            
            # Get all users
            users = User.get_all()
            
            assert len(users) == 2
            assert users[0].name in ['John Doe', 'Jane Smith']
            assert users[1].name in ['John Doe', 'Jane Smith']
    
    def test_user_to_dict(self, db_connection):
        """Test user to dictionary conversion."""
        with patch('backend.models.user.get_db_connection', return_value=db_connection):
            user = User.create('John Doe', 'john@example.com')
            user_dict = user.to_dict()
            
            assert isinstance(user_dict, dict)
            assert user_dict['name'] == 'John Doe'
            assert user_dict['email'] == 'john@example.com'
            assert 'id' in user_dict
            assert 'created_at' in user_dict


class TestPostModel:
    """Test cases for Post model."""
    
    def test_create_post_success(self, db_connection):
        """Test successful post creation."""
        with patch('backend.models.post.get_db_connection', return_value=db_connection):
            post = Post.create('Test Title', 'Test content', 1)
            
            assert post is not None
            assert post.title == 'Test Title'
            assert post.content == 'Test content'
            assert post.user_id == 1
            assert post.id is not None
    
    def test_create_post_without_content(self, db_connection):
        """Test post creation without content."""
        with patch('backend.models.post.get_db_connection', return_value=db_connection):
            post = Post.create('Test Title')
            
            assert post is not None
            assert post.title == 'Test Title'
            assert post.content is None
            assert post.user_id is None
    
    def test_get_post_by_id(self, db_connection):
        """Test retrieving post by ID."""
        with patch('backend.models.post.get_db_connection', return_value=db_connection):
            # Create post
            created_post = Post.create('Test Title', 'Test content')
            
            # Retrieve post
            retrieved_post = Post.get_by_id(created_post.id)
            
            assert retrieved_post is not None
            assert retrieved_post.id == created_post.id
            assert retrieved_post.title == 'Test Title'
            assert retrieved_post.content == 'Test content'
    
    def test_get_all_posts(self, db_connection):
        """Test retrieving all posts."""
        with patch('backend.models.post.get_db_connection', return_value=db_connection):
            # Create multiple posts
            Post.create('Post 1', 'Content 1')
            Post.create('Post 2', 'Content 2')
            
            # Get all posts
            posts = Post.get_all()
            
            assert len(posts) == 2
    
    def test_get_posts_by_user(self, db_connection):
        """Test retrieving posts by user."""
        with patch('backend.models.post.get_db_connection', return_value=db_connection):
            # Create posts for different users
            Post.create('User 1 Post', 'Content', 1)
            Post.create('User 2 Post', 'Content', 2)
            Post.create('Another User 1 Post', 'Content', 1)
            
            # Get posts by user 1
            user_posts = Post.get_by_user(1)
            
            assert len(user_posts) == 2
            for post in user_posts:
                assert post.user_id == 1
    
    def test_post_to_dict(self, db_connection):
        """Test post to dictionary conversion."""
        with patch('backend.models.post.get_db_connection', return_value=db_connection):
            post = Post.create('Test Title', 'Test content', 1)
            post_dict = post.to_dict()
            
            assert isinstance(post_dict, dict)
            assert post_dict['title'] == 'Test Title'
            assert post_dict['content'] == 'Test content'
            assert post_dict['user_id'] == 1
            assert 'id' in post_dict
            assert 'created_at' in post_dict


class TestRatingModel:
    """Test cases for Rating model."""
    
    def test_save_rating_new(self, db_connection):
        """Test saving a new rating."""
        with patch('backend.models.rating.get_db_connection', return_value=db_connection):
            success = Rating.save_rating('test-track', 'up', 'user123')
            
            assert success is True
    
    def test_save_rating_update_existing(self, db_connection):
        """Test updating an existing rating."""
        with patch('backend.models.rating.get_db_connection', return_value=db_connection):
            # Create initial rating
            Rating.save_rating('test-track', 'up', 'user123')
            
            # Update rating
            success = Rating.save_rating('test-track', 'down', 'user123')
            
            assert success is True
    
    def test_save_rating_remove(self, db_connection):
        """Test removing a rating."""
        with patch('backend.models.rating.get_db_connection', return_value=db_connection):
            # Create rating
            Rating.save_rating('test-track', 'up', 'user123')
            
            # Remove rating
            success = Rating.save_rating('test-track', None, 'user123')
            
            assert success is True
    
    def test_get_track_ratings(self, db_connection):
        """Test getting track ratings."""
        with patch('backend.models.rating.get_db_connection', return_value=db_connection):
            # Create ratings
            Rating.save_rating('test-track', 'up', 'user1')
            Rating.save_rating('test-track', 'up', 'user2')
            Rating.save_rating('test-track', 'down', 'user3')
            
            # Get ratings
            ratings = Rating.get_track_ratings('test-track', 'user1')
            
            assert ratings['track_id'] == 'test-track'
            assert ratings['ratings']['up'] == 2
            assert ratings['ratings']['down'] == 1
            assert ratings['user_rating'] == 'up'
    
    def test_get_track_ratings_no_user(self, db_connection):
        """Test getting track ratings without user fingerprint."""
        with patch('backend.models.rating.get_db_connection', return_value=db_connection):
            # Create ratings
            Rating.save_rating('test-track', 'up', 'user1')
            
            # Get ratings without user
            ratings = Rating.get_track_ratings('test-track')
            
            assert ratings['track_id'] == 'test-track'
            assert ratings['ratings']['up'] == 1
            assert ratings['user_rating'] is None
    
    def test_get_user_ratings(self, db_connection):
        """Test getting user ratings."""
        with patch('backend.models.rating.get_db_connection', return_value=db_connection):
            # Create ratings for user
            Rating.save_rating('track1', 'up', 'user123')
            Rating.save_rating('track2', 'down', 'user123')
            Rating.save_rating('track3', 'up', 'other_user')
            
            # Get user ratings
            user_ratings = Rating.get_user_ratings('user123')
            
            assert len(user_ratings) == 2
            for rating in user_ratings:
                assert 'track_id' in rating
                assert 'rating' in rating
                assert 'timestamp' in rating


class TestDatabaseModule:
    """Test cases for database module."""
    
    def test_init_db(self, test_config):
        """Test database initialization."""
        with patch('backend.models.database.config', test_config):
            # This should not raise an exception
            init_db()
    
    def test_get_db_connection(self, test_config):
        """Test database connection."""
        with patch('backend.models.database.config', test_config):
            conn = get_db_connection()
            
            assert conn is not None
            assert conn.row_factory == sqlite3.Row
            conn.close()
    
    @patch('backend.models.database.sqlite3.connect')
    def test_db_connection_error(self, mock_connect):
        """Test database connection error handling."""
        mock_connect.side_effect = sqlite3.Error("Connection failed")
        
        with pytest.raises(sqlite3.Error):
            get_db_connection()