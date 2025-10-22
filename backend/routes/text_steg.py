"""
Text Steganography Routes
"""

from flask import Blueprint, request, jsonify, current_app
import sys
import os

# Add shared directory to path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
shared_dir = os.path.join(backend_dir, '..', 'shared')
steganography_dir = os.path.join(shared_dir, 'steganography')
sys.path.insert(0, shared_dir)
sys.path.insert(0, steganography_dir)

# Now we can import from steganography package
from text_steganography import TextSteganography
from ai_analyzer import AIAnalyzer

text_steg_bp = Blueprint('text_steg', __name__)

# Initialize services
text_steg = TextSteganography()
ai_analyzer = AIAnalyzer()

@text_steg_bp.route('/embed', methods=['POST'])
def embed_text():
    """Embed message in text"""
    try:
        data = request.get_json()
        
        if not data or 'cover_text' not in data or 'secret_message' not in data:
            return jsonify({'error': 'Missing required fields: cover_text, secret_message'}), 400
            
        cover_text = data['cover_text']
        secret_message = data['secret_message']
        method = data.get('method', 'auto')
        
        # If method is auto, use AI to determine best method
        if method == 'auto':
            analysis = ai_analyzer.analyze_text_for_steganography(cover_text)
            method = analysis['recommended_method']
        
        # Embed message
        stego_text = text_steg.embed_message(cover_text, secret_message, method)
        
        return jsonify({
            'success': True,
            'stego_text': stego_text,
            'method_used': method,
            'message': 'Text embedded successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@text_steg_bp.route('/extract', methods=['POST'])
def extract_text():
    """Extract message from steganographic text"""
    try:
        data = request.get_json()
        
        if not data or 'stego_text' not in data:
            return jsonify({'error': 'Missing required field: stego_text'}), 400
            
        stego_text = data['stego_text']
        method = data.get('method', 'auto')
        
        # If method is auto, use AI to determine best method or try all methods
        if method == 'auto':
            # First try AI analysis to predict the method
            try:
                analysis = ai_analyzer.analyze_text_for_steganography(stego_text)
                predicted_method = analysis['recommended_method']
                confidence = analysis['confidence']
                
                # Try the predicted method first
                try:
                    extracted = text_steg.extract_message(stego_text, predicted_method)
                    if extracted and len(extracted) > 0:
                        return jsonify({
                            'success': True,
                            'extracted_message': extracted,
                            'method_used': predicted_method,
                            'confidence': confidence,
                            'message': 'Message extracted successfully using AI prediction'
                        })
                except Exception:
                    pass  # Continue to try other methods
                    
                # If predicted method failed, try all methods
                methods = ['whitespace', 'synonym', 'binary']
                for m in methods:
                    try:
                        extracted = text_steg.extract_message(stego_text, m)
                        if extracted and len(extracted) > 0:
                            return jsonify({
                                'success': True,
                                'extracted_message': extracted,
                                'method_used': m,
                                'confidence': 0.7,  # Lower confidence when fallback used
                                'message': 'Message extracted successfully using fallback method'
                            })
                    except Exception:
                        continue
                        
                return jsonify({'error': 'Could not extract message from text using any method'}), 400
            except Exception as ai_error:
                # If AI analysis fails, fall back to trying all methods
                methods = ['whitespace', 'synonym', 'binary']
                for m in methods:
                    try:
                        extracted = text_steg.extract_message(stego_text, m)
                        if extracted and len(extracted) > 0:
                            return jsonify({
                                'success': True,
                                'extracted_message': extracted,
                                'method_used': m,
                                'confidence': 0.6,  # Lower confidence when no AI used
                                'message': 'Message extracted successfully using fallback method'
                            })
                    except Exception:
                        continue
                return jsonify({'error': 'Could not extract message from text using any method'}), 400
        else:
            # Use specific method
            extracted = text_steg.extract_message(stego_text, method)
            if extracted and len(extracted) > 0:
                return jsonify({
                    'success': True,
                    'extracted_message': extracted,
                    'method_used': method,
                    'confidence': 0.9,
                    'message': 'Message extracted successfully'
                })
            else:
                return jsonify({'error': 'Could not extract message from text'}), 400
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500