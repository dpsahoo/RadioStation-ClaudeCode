"""Users API endpoints for Radio Calico."""

from flask import Blueprint, request
import logging
from ..models.user import User
from ..utils.validation import validate_json, validate_email, validate_required_fields
from ..utils.responses import success_response, error_response

logger = logging.getLogger(__name__)
users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('', methods=['GET'])
def get_users():
    """Get all users."""
    try:
        limit = request.args.get('limit', 100, type=int)
        if limit > 100:
            limit = 100
            
        users = User.get_all(limit)
        
        return success_response({
            'users': [user.to_dict() for user in users],
            'count': len(users)
        })
        
    except Exception as e:
        logger.error(f"Error in get_users: {e}")
        return error_response('Internal server error', 500)


@users_bp.route('', methods=['POST'])
def create_user():
    """Create a new user."""
    try:
        # Validate request data
        data = validate_json(request)
        if not data:
            return error_response('Invalid JSON data', 400)
        
        # Check required fields
        missing_fields = validate_required_fields(data, ['name', 'email'])
        if missing_fields:
            return error_response(missing_fields, 400)
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        
        # Validate email format
        if not validate_email(email):
            return error_response('Invalid email format', 400)
        
        # Create user
        user = User.create(name, email)
        
        if user:
            return success_response(
                user.to_dict(),
                'User created successfully',
                201
            )
        else:
            return error_response('Email already exists', 400)
            
    except Exception as e:
        logger.error(f"Error in create_user: {e}")
        return error_response('Internal server error', 500)


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID."""
    try:
        user = User.get_by_id(user_id)
        
        if user:
            return success_response(user.to_dict())
        else:
            return error_response('User not found', 404)
            
    except Exception as e:
        logger.error(f"Error in get_user: {e}")
        return error_response('Internal server error', 500)