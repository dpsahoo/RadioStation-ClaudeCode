"""Post model for Radio Calico application."""

import sqlite3
import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from .database import execute_query, get_db_connection

logger = logging.getLogger(__name__)


@dataclass
class Post:
    """Post model."""
    
    title: str
    content: Optional[str] = None
    user_id: Optional[int] = None
    id: Optional[int] = None
    created_at: Optional[str] = None
    author_name: Optional[str] = None
    
    @classmethod
    def create(cls, title: str, content: Optional[str] = None, user_id: Optional[int] = None) -> Optional['Post']:
        """Create a new post."""
        try:
            post_id = execute_query(
                'INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)',
                (title, content, user_id)
            )
            
            if post_id:
                post = cls(title=title, content=content, user_id=user_id, id=post_id)
                logger.info(f"Post created: {title}")
                return post
            
        except sqlite3.Error as e:
            logger.error(f"Error creating post: {e}")
            return None
    
    @classmethod
    def get_by_id(cls, post_id: int) -> Optional['Post']:
        """Get post by ID."""
        try:
            conn = get_db_connection()
            post_data = conn.execute('''
                SELECT posts.*, users.name as author_name 
                FROM posts 
                LEFT JOIN users ON posts.user_id = users.id 
                WHERE posts.id = ?
            ''', (post_id,)).fetchone()
            conn.close()
            
            if post_data:
                return cls(
                    id=post_data['id'],
                    title=post_data['title'],
                    content=post_data['content'],
                    user_id=post_data['user_id'],
                    created_at=post_data['created_at'],
                    author_name=post_data['author_name']
                )
            
        except sqlite3.Error as e:
            logger.error(f"Error getting post by ID: {e}")
            return None
    
    @classmethod
    def get_all(cls, limit: int = 100) -> List['Post']:
        """Get all posts with author information."""
        try:
            conn = get_db_connection()
            posts_data = conn.execute('''
                SELECT posts.*, users.name as author_name 
                FROM posts 
                LEFT JOIN users ON posts.user_id = users.id 
                ORDER BY posts.created_at DESC 
                LIMIT ?
            ''', (limit,)).fetchall()
            conn.close()
            
            return [
                cls(
                    id=post['id'],
                    title=post['title'],
                    content=post['content'],
                    user_id=post['user_id'],
                    created_at=post['created_at'],
                    author_name=post['author_name']
                )
                for post in posts_data
            ]
            
        except sqlite3.Error as e:
            logger.error(f"Error getting all posts: {e}")
            return []
    
    @classmethod
    def get_by_user(cls, user_id: int, limit: int = 50) -> List['Post']:
        """Get posts by user."""
        try:
            conn = get_db_connection()
            posts_data = conn.execute('''
                SELECT posts.*, users.name as author_name 
                FROM posts 
                LEFT JOIN users ON posts.user_id = users.id 
                WHERE posts.user_id = ? 
                ORDER BY posts.created_at DESC 
                LIMIT ?
            ''', (user_id, limit)).fetchall()
            conn.close()
            
            return [
                cls(
                    id=post['id'],
                    title=post['title'],
                    content=post['content'],
                    user_id=post['user_id'],
                    created_at=post['created_at'],
                    author_name=post['author_name']
                )
                for post in posts_data
            ]
            
        except sqlite3.Error as e:
            logger.error(f"Error getting posts by user: {e}")
            return []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert post to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'author_name': self.author_name
        }