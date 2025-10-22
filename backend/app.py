"""
Main Application Factory
"""

from flask import Flask, send_from_directory, request
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Use direct imports
from config.settings import config

# Initialize extensions
cors = CORS()
socketio = SocketIO()

def create_app(config_name='default'):
    """Application factory pattern"""
    
    # Get the absolute path to the static folder
    static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
    
    app = Flask(__name__, 
                static_folder=static_folder,
                static_url_path='/static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    cors.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Create upload directory if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Serve the main index.html
    @app.route('/')
    def index():
        if app.static_folder and os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return send_from_directory(app.static_folder, 'index.html')
        return {'error': 'Static folder not configured or index.html not found'}, 500
    
    # Serve other static files and handle SPA routing
    @app.route('/<path:path>')
    def static_files(path):
        if app.static_folder:
            full_path = os.path.join(app.static_folder, path)
            # If it's a static file (CSS, JS, images, etc.) and exists, serve it directly
            if path.startswith('assets/') and os.path.exists(full_path):
                return send_from_directory(app.static_folder, path)
            # For all other paths (including Vue Router routes), serve index.html
            # This is needed for SPA routing to work properly
            if os.path.exists(os.path.join(app.static_folder, 'index.html')):
                return send_from_directory(app.static_folder, 'index.html')
        return {'error': 'Static folder not configured'}, 500
    
    # Register blueprints with direct imports
    from routes.main import main_bp
    from routes.text_steg import text_steg_bp
    from routes.ai_analysis import ai_analysis_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(text_steg_bp, url_prefix='/api/text')
    app.register_blueprint(ai_analysis_bp, url_prefix='/api/ai')
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        # Try to serve static files first
        if app.static_folder and request.path.startswith('/static/'):
            static_path = request.path[8:]  # Remove '/static/' prefix
            full_path = os.path.join(app.static_folder, static_path)
            if os.path.exists(full_path):
                return send_from_directory(app.static_folder, static_path)
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app

# Create app instance for gunicorn
app = create_app()