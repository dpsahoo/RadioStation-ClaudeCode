"""Database connection and initialization for Radio Calico."""

import sqlite3
import logging
from typing import Optional
from ..config import config

logger = logging.getLogger(__name__)


def get_db_connection() -> sqlite3.Connection:
    """Get database connection with proper configuration."""
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise


def init_db() -> None:
    """Initialize the database with all required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create posts table
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
        
        # Create ratings table
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
        
        # Create index for faster rating queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_ratings_track_id 
            ON ratings(track_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_ratings_fingerprint 
            ON ratings(user_fingerprint)
        ''')
        
        conn.commit()
        logger.info("Database initialized successfully")
        
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


def execute_query(query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = False):
    """Execute a database query with proper error handling."""
    conn = get_db_connection()
    try:
        cursor = conn.execute(query, params)
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = cursor.lastrowid
            
        conn.commit()
        return result
        
    except sqlite3.Error as e:
        logger.error(f"Query execution error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()