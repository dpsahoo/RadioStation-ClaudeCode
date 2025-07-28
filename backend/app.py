"""
Radio Sahoo - Main Flask Application
Refactored for better organization, security, and maintainability.
"""

import os
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import application modules
try:
    from .config import config
    from .models import init_db
    from .api import users_bp, posts_bp, ratings_bp, stream_bp
    from .utils.logging_config import setup_logging
    from .utils.responses import error_response
except ImportError:
    # Handle direct execution
    from config import config
    from models import init_db
    from api import users_bp, posts_bp, ratings_bp, stream_bp
    from utils.logging_config import setup_logging
    from utils.responses import error_response

# Setup logging
setup_logging()

import logging
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Application factory pattern for creating Flask app."""
    
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    # Configure Flask app
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['DEBUG'] = config.DEBUG
    
    # Setup CORS
    CORS(app, origins=config.ALLOWED_ORIGINS)
    
    # Register API blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(ratings_bp)
    app.register_blueprint(stream_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register main routes
    register_routes(app)
    
    return app


def register_routes(app: Flask) -> None:
    """Register main application routes."""
    
    @app.route('/')
    def home():
        """Home page with server status and available routes."""
        return '''
        <h1>Radio Sahoo - Lossless Audio Streaming</h1>
        <p>Server is running successfully!</p>
        <p>Database: SQLite connected</p>
        <h2>Available Routes:</h2>
        <ul>
            <li><a href="/radio">Radio Player</a> - Online HLS Radio Stream</li>
            <li><a href="/dashboard">Dashboard</a> - Interactive web interface</li>
            <li><strong>API Endpoints:</strong></li>
            <li>GET/POST /api/users - User management</li>
            <li>GET/POST /api/posts - Post management</li>
            <li>GET/POST /api/ratings - Track rating system</li>
        </ul>
        <p><strong>Stream URL:</strong> {}</p>
        <p><strong>Version:</strong> 2.0 (Refactored)</p>
        '''.format(config.STREAM_URL)
    
    @app.route('/radio')
    def radio():
        """Radio player page."""
        return render_template('radio.html')
    
    @app.route('/dashboard')
    def dashboard():
        """Dashboard page."""
        return render_template('dashboard.html')
    
    @app.route('/static/<path:filename>')
    def static_files(filename):
        """Serve static files."""
        return send_from_directory('../frontend/static', filename)
    
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring."""
        return {
            'status': 'healthy',
            'version': '2.0',
            'database': 'connected',
            'stream_url': config.STREAM_URL
        }


def register_error_handlers(app: Flask) -> None:
    """Register global error handlers."""
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return error_response('Resource not found', 404)
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {error}")
        return error_response('Internal server error', 500)
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors."""
        return error_response('Bad request', 400)


def main():
    """Main entry point for the application."""
    try:
        # Initialize database
        init_db()
        logger.info("Database initialized successfully")
        
        # Create Flask app
        app = create_app()
        
        logger.info(f"Starting Radio Sahoo server...")
        logger.info(f"Debug mode: {config.DEBUG}")
        logger.info(f"Host: {config.HOST}:{config.PORT}")
        
        # Run the application
        app.run(
            debug=config.DEBUG,
            host=config.HOST,
            port=config.PORT
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise


if __name__ == '__main__':
    main()