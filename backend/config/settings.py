"""
Application Configuration Settings
"""

import os

class Config:
    """Base configuration class"""
    
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'steganography-app-secret-key-for-development'
    DEBUG = os.environ.get('FLASK_DEBUG') or True
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
    
    # Allowed file extensions
    ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'flac', 'aac'}
    ALLOWED_TEXT_EXTENSIONS = {'txt', 'md', 'doc', 'docx'}
    
    # Steganography settings
    DEFAULT_TEXT_METHOD = 'whitespace'
    DEFAULT_AUDIO_METHOD = 'lsb'
    
    # AI settings
    AI_CONFIDENCE_THRESHOLD = 0.7
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = 'production'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}