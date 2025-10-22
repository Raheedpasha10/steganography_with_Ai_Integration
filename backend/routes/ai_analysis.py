"""
AI Analysis Routes
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Add shared directory to path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
shared_dir = os.path.join(backend_dir, '..', 'shared')
sys.path.insert(0, shared_dir)

# Import steganography modules
from steganography import AIAnalyzer

ai_analysis_bp = Blueprint('ai_analysis', __name__)

# Initialize services
ai_analyzer = AIAnalyzer()

@ai_analysis_bp.route('/analyze_text', methods=['POST'])
def analyze_text():
    """Analyze text for steganography"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing required field: text'}), 400
            
        text = data['text']
        
        # Analyze text
        analysis = ai_analyzer.analyze_text_for_steganography(text)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'message': 'Text analysis completed'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500