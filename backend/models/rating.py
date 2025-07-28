"""Rating model for track ratings."""

import sqlite3
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from .database import execute_query, get_db_connection

logger = logging.getLogger(__name__)


@dataclass
class Rating:
    """Rating model for track ratings."""
    
    track_id: str
    rating: Optional[str]  # 'up', 'down', or None
    user_fingerprint: str
    id: Optional[int] = None
    timestamp: Optional[str] = None
    
    @classmethod
    def save_rating(cls, track_id: str, rating: Optional[str], user_fingerprint: str) -> bool:
        """Save or update a rating for a track."""
        try:
            if rating is None:
                # Remove existing rating
                execute_query(
                    'DELETE FROM ratings WHERE track_id = ? AND user_fingerprint = ?',
                    (track_id, user_fingerprint)
                )
                logger.info(f"Rating removed for track {track_id}")
                return True
            
            # Check if rating already exists
            conn = get_db_connection()
            existing = conn.execute(
                'SELECT id FROM ratings WHERE track_id = ? AND user_fingerprint = ?',
                (track_id, user_fingerprint)
            ).fetchone()
            
            if existing:
                # Update existing rating
                execute_query(
                    '''UPDATE ratings SET rating = ?, timestamp = CURRENT_TIMESTAMP 
                       WHERE track_id = ? AND user_fingerprint = ?''',
                    (rating, track_id, user_fingerprint)
                )
                logger.info(f"Rating updated for track {track_id}: {rating}")
            else:
                # Create new rating
                execute_query(
                    'INSERT INTO ratings (track_id, rating, user_fingerprint) VALUES (?, ?, ?)',
                    (track_id, rating, user_fingerprint)
                )
                logger.info(f"New rating created for track {track_id}: {rating}")
            
            conn.close()
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Error saving rating: {e}")
            return False
    
    @classmethod
    def get_track_ratings(cls, track_id: str, user_fingerprint: Optional[str] = None) -> Dict[str, Any]:
        """Get rating counts and user's current rating for a track."""
        try:
            conn = get_db_connection()
            
            # Get rating counts
            ratings = conn.execute('''
                SELECT rating, COUNT(*) as count 
                FROM ratings 
                WHERE track_id = ? 
                GROUP BY rating
            ''', (track_id,)).fetchall()
            
            # Get user's current rating if fingerprint provided
            user_rating = None
            if user_fingerprint:
                user_rating_row = conn.execute(
                    'SELECT rating FROM ratings WHERE track_id = ? AND user_fingerprint = ?',
                    (track_id, user_fingerprint)
                ).fetchone()
                user_rating = user_rating_row['rating'] if user_rating_row else None
            
            conn.close()
            
            # Format response
            result = {
                'track_id': track_id,
                'ratings': {
                    'up': 0,
                    'down': 0
                },
                'user_rating': user_rating
            }
            
            for rating in ratings:
                result['ratings'][rating['rating']] = rating['count']
            
            return result
            
        except sqlite3.Error as e:
            logger.error(f"Error getting track ratings: {e}")
            return {
                'track_id': track_id,
                'ratings': {'up': 0, 'down': 0},
                'user_rating': None,
                'error': str(e)
            }
    
    @classmethod
    def get_user_ratings(cls, user_fingerprint: str, limit: int = 50) -> list:
        """Get recent ratings by a user."""
        try:
            conn = get_db_connection()
            ratings = conn.execute('''
                SELECT track_id, rating, timestamp 
                FROM ratings 
                WHERE user_fingerprint = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (user_fingerprint, limit)).fetchall()
            conn.close()
            
            return [dict(rating) for rating in ratings]
            
        except sqlite3.Error as e:
            logger.error(f"Error getting user ratings: {e}")
            return []