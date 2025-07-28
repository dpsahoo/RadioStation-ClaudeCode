"""Ratings API endpoints for Radio Calico."""

from flask import Blueprint, request, jsonify
import logging
from ..models.rating import Rating
from ..utils.validation import validate_json, validate_rating
from ..utils.responses import success_response, error_response

logger = logging.getLogger(__name__)
ratings_bp = Blueprint('ratings', __name__, url_prefix='/api/ratings')


@ratings_bp.route('', methods=['POST'])
def create_rating():
    """Create or update a rating for a track."""
    try:
        # Validate request data
        data = validate_json(request)
        if not data:
            return error_response('Invalid JSON data', 400)
        
        # Check required fields
        required_fields = ['track_id', 'rating', 'user_fingerprint']
        for field in required_fields:
            if field not in data:
                return error_response(f'{field} is required', 400)
        
        track_id = data['track_id']
        rating = data['rating']
        user_fingerprint = data['user_fingerprint']
        
        # Validate rating value
        if not validate_rating(rating):
            return error_response('Rating must be "up", "down", or null', 400)
        
        # Save rating
        success = Rating.save_rating(track_id, rating, user_fingerprint)
        
        if success:
            action = 'removed' if rating is None else 'saved'
            return success_response({
                'track_id': track_id,
                'rating': rating,
                'message': f'Rating {action} successfully'
            })
        else:
            return error_response('Failed to save rating', 500)
            
    except Exception as e:
        logger.error(f"Error in create_rating: {e}")
        return error_response('Internal server error', 500)


@ratings_bp.route('/<track_id>', methods=['GET'])
def get_track_ratings(track_id):
    """Get ratings for a specific track."""
    try:
        user_fingerprint = request.args.get('fingerprint')
        
        # Get ratings data
        ratings_data = Rating.get_track_ratings(track_id, user_fingerprint)
        
        return success_response(ratings_data)
        
    except Exception as e:
        logger.error(f"Error in get_track_ratings: {e}")
        return error_response('Internal server error', 500)


@ratings_bp.route('/user/<user_fingerprint>', methods=['GET'])
def get_user_ratings(user_fingerprint):
    """Get recent ratings by a user."""
    try:
        limit = request.args.get('limit', 50, type=int)
        
        # Validate limit
        if limit > 100:
            limit = 100
        
        ratings = Rating.get_user_ratings(user_fingerprint, limit)
        
        return success_response({
            'user_fingerprint': user_fingerprint,
            'ratings': ratings,
            'count': len(ratings)
        })
        
    except Exception as e:
        logger.error(f"Error in get_user_ratings: {e}")
        return error_response('Internal server error', 500)