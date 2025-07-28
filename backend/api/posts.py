"""Posts API endpoints for Radio Calico."""

from flask import Blueprint, request
import logging
from ..models.post import Post
from ..utils.validation import validate_json, validate_required_fields
from ..utils.responses import success_response, error_response

logger = logging.getLogger(__name__)
posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')


@posts_bp.route('', methods=['GET'])
def get_posts():
    """Get all posts."""
    try:
        limit = request.args.get('limit', 100, type=int)
        if limit > 100:
            limit = 100
            
        posts = Post.get_all(limit)
        
        return success_response({
            'posts': [post.to_dict() for post in posts],
            'count': len(posts)
        })
        
    except Exception as e:
        logger.error(f"Error in get_posts: {e}")
        return error_response('Internal server error', 500)


@posts_bp.route('', methods=['POST'])
def create_post():
    """Create a new post."""
    try:
        # Validate request data
        data = validate_json(request)
        if not data:
            return error_response('Invalid JSON data', 400)
        
        # Check required fields
        missing_fields = validate_required_fields(data, ['title'])
        if missing_fields:
            return error_response(missing_fields, 400)
        
        title = data['title'].strip()
        content = data.get('content', '').strip()
        user_id = data.get('user_id')
        
        # Create post
        post = Post.create(title, content, user_id)
        
        if post:
            return success_response(
                post.to_dict(),
                'Post created successfully',
                201
            )
        else:
            return error_response('Failed to create post', 500)
            
    except Exception as e:
        logger.error(f"Error in create_post: {e}")
        return error_response('Internal server error', 500)


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get post by ID."""
    try:
        post = Post.get_by_id(post_id)
        
        if post:
            return success_response(post.to_dict())
        else:
            return error_response('Post not found', 404)
            
    except Exception as e:
        logger.error(f"Error in get_post: {e}")
        return error_response('Internal server error', 500)


@posts_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_posts(user_id):
    """Get posts by user."""
    try:
        limit = request.args.get('limit', 50, type=int)
        if limit > 100:
            limit = 100
            
        posts = Post.get_by_user(user_id, limit)
        
        return success_response({
            'posts': [post.to_dict() for post in posts],
            'count': len(posts),
            'user_id': user_id
        })
        
    except Exception as e:
        logger.error(f"Error in get_user_posts: {e}")
        return error_response('Internal server error', 500)