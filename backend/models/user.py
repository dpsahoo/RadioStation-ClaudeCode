"""User model for Radio Calico application."""

import sqlite3
import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from .database import execute_query, get_db_connection

logger = logging.getLogger(__name__)


@dataclass
class User:
    """User model."""
    
    name: str
    email: str
    id: Optional[int] = None
    created_at: Optional[str] = None
    
    @classmethod
    def create(cls, name: str, email: str) -> Optional['User']:
        """Create a new user."""
        try:
            user_id = execute_query(
                'INSERT INTO users (name, email) VALUES (?, ?)',
                (name, email)
            )
            
            if user_id:
                user = cls(name=name, email=email, id=user_id)
                logger.info(f"User created: {email}")
                return user
            
        except sqlite3.IntegrityError:
            logger.warning(f"User creation failed - email already exists: {email}")
            return None
        except sqlite3.Error as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        """Get user by ID."""
        try:
            user_data = execute_query(
                'SELECT * FROM users WHERE id = ?',
                (user_id,),
                fetch_one=True
            )
            
            if user_data:
                return cls(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    created_at=user_data['created_at']
                )
            
        except sqlite3.Error as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        """Get user by email."""
        try:
            user_data = execute_query(
                'SELECT * FROM users WHERE email = ?',
                (email,),
                fetch_one=True
            )
            
            if user_data:
                return cls(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    created_at=user_data['created_at']
                )
            
        except sqlite3.Error as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    @classmethod
    def get_all(cls, limit: int = 100) -> List['User']:
        """Get all users."""
        try:
            users_data = execute_query(
                'SELECT * FROM users ORDER BY created_at DESC LIMIT ?',
                (limit,),
                fetch_all=True
            )
            
            return [
                cls(
                    id=user['id'],
                    name=user['name'],
                    email=user['email'],
                    created_at=user['created_at']
                )
                for user in users_data
            ]
            
        except sqlite3.Error as e:
            logger.error(f"Error getting all users: {e}")
            return []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at
        }