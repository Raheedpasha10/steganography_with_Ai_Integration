"""
Simple run script for the backend
"""

import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5007, debug=True)