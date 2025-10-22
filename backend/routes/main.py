"""
Main routes for the application
"""

from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main application endpoint"""
    return jsonify({
        'message': 'Steganography App with AI Integration',
        'version': '1.0.0',
        'status': 'running'
    })

@main_bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'steganography-api'
    })