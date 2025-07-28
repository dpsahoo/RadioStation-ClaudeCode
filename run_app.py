#!/usr/bin/env python3
"""
Simple startup script for Radio Sahoo application
Handles import paths and runs the Flask app
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Set up environment
os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('FLASK_DEBUG', '1')

def main():
    """Main entry point"""
    try:
        # Import Flask and create a simple app
        from flask import Flask, render_template, send_from_directory, jsonify
        from flask_cors import CORS
        import sqlite3
        import logging
        from datetime import datetime
        
        # Create Flask app
        app = Flask(__name__, 
                   template_folder='frontend/templates',
                   static_folder='frontend/static')
        
        # Configure app
        app.config['SECRET_KEY'] = 'dev-secret-key-for-local-testing'
        app.config['DEBUG'] = True
        
        # Setup CORS
        CORS(app, origins=['http://localhost:5000', 'http://127.0.0.1:5000'])
        
        # Setup basic logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Initialize database
        def init_db():
            """Initialize SQLite database"""
            try:
                conn = sqlite3.connect('radio_sahoo.db')
                cursor = conn.cursor()
                
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
                
                conn.commit()
                conn.close()
                logger.info("Database initialized successfully")
            except Exception as e:
                logger.error(f"Database initialization failed: {e}")
        
        # Routes
        @app.route('/')
        def home():
            """Home page"""
            return '''
            <h1>🎵 Radio Sahoo - Lossless Audio Streaming</h1>
            <p>Server is running successfully!</p>
            <p>Database: SQLite connected</p>
            <h2>Available Routes:</h2>
            <ul>
                <li><a href="/radio">Radio Player</a> - Online HLS Radio Stream</li>
                <li><a href="/health">Health Check</a> - System status</li>
            </ul>
            <p><strong>Stream URL:</strong> https://d3d4yli4hf5bmh.cloudfront.net/hls/live.m3u8</p>
            <p><strong>Version:</strong> 2.0 (Dockerized)</p>
            '''
        
        @app.route('/radio')
        def radio():
            """Radio player page"""
            return render_template('radio.html')
        
        @app.route('/health')
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'version': '2.0',
                'database': 'connected',
                'timestamp': datetime.now().isoformat(),
                'stream_url': 'https://d3d4yli4hf5bmh.cloudfront.net/hls/live.m3u8'
            })
        
        @app.route('/api/ratings', methods=['POST'])
        def add_rating():
            """Add a rating"""
            from flask import request
            try:
                data = request.get_json()
                track_id = data.get('track_id')
                rating = data.get('rating')
                user_fingerprint = data.get('user_fingerprint')
                
                if not all([track_id, rating, user_fingerprint]):
                    return jsonify({'success': False, 'error': 'Missing required fields'}), 400
                
                if rating not in ['up', 'down', None]:
                    return jsonify({'success': False, 'error': 'Invalid rating'}), 400
                
                conn = sqlite3.connect('radio_sahoo.db')
                cursor = conn.cursor()
                
                if rating is None:
                    # Remove rating
                    cursor.execute('DELETE FROM ratings WHERE track_id = ? AND user_fingerprint = ?',
                                 (track_id, user_fingerprint))
                else:
                    # Add or update rating
                    cursor.execute('''
                        INSERT OR REPLACE INTO ratings (track_id, rating, user_fingerprint, timestamp)
                        VALUES (?, ?, ?, ?)
                    ''', (track_id, rating, user_fingerprint, datetime.now()))
                
                conn.commit()
                conn.close()
                
                return jsonify({'success': True, 'message': 'Rating saved'})
                
            except Exception as e:
                logger.error(f"Rating error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @app.route('/api/ratings/<track_id>')
        def get_ratings(track_id):
            """Get ratings for a track"""
            from flask import request
            try:
                user_fingerprint = request.args.get('fingerprint')
                
                conn = sqlite3.connect('radio_sahoo.db')
                cursor = conn.cursor()
                
                # Get rating counts
                cursor.execute('SELECT rating, COUNT(*) FROM ratings WHERE track_id = ? GROUP BY rating', (track_id,))
                counts = dict(cursor.fetchall())
                
                # Get user's rating
                user_rating = None
                if user_fingerprint:
                    cursor.execute('SELECT rating FROM ratings WHERE track_id = ? AND user_fingerprint = ?',
                                 (track_id, user_fingerprint))
                    result = cursor.fetchone()
                    if result:
                        user_rating = result[0]
                
                conn.close()
                
                return jsonify({
                    'success': True,
                    'track_id': track_id,
                    'ratings': {
                        'up': counts.get('up', 0),
                        'down': counts.get('down', 0)
                    },
                    'user_rating': user_rating
                })
                
            except Exception as e:
                logger.error(f"Get ratings error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        # Static file routes for frontend assets
        @app.route('/css/<path:filename>')
        def css_files(filename):
            """Serve CSS files from frontend/css directory"""
            return send_from_directory('frontend/css', filename, mimetype='text/css')
        
        @app.route('/js/<path:filename>')
        def js_files(filename):
            """Serve JavaScript files from frontend/js directory"""
            return send_from_directory('frontend/js', filename, mimetype='application/javascript')
        
        @app.route('/css/components/<path:filename>')
        def css_components(filename):
            """Serve CSS component files"""
            return send_from_directory('frontend/css/components', filename, mimetype='text/css')
        
        @app.route('/js/modules/<path:filename>')
        def js_modules(filename):
            """Serve JavaScript module files"""
            return send_from_directory('frontend/js/modules', filename, mimetype='application/javascript')
        
        # Error handlers
        @app.errorhandler(404)
        def not_found(error):
            return jsonify({'success': False, 'error': 'Resource not found'}), 404
        
        @app.errorhandler(500)
        def internal_error(error):
            logger.error(f"Internal server error: {error}")
            return jsonify({'success': False, 'error': 'Internal server error'}), 500
        
        # Initialize database
        init_db()
        
        # Start the application
        logger.info("🎵 Starting Radio Sahoo server...")
        logger.info("🌐 Access the app at: http://127.0.0.1:5000/radio")
        
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000
        )
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()