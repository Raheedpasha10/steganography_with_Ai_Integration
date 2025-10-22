# Local Development Setup

This document explains how to run the Steganography Web Application locally.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository (if not already done):
   ```bash
   git clone <repository-url>
   cd steganography_with_ai_temp
   ```

2. Install the required dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

## Running the Application

1. Start the Flask backend server:
   ```bash
   python backend/run.py
   ```

2. Access the application in your browser at:
   ```
   http://localhost:5007
   ```

## Application Structure

- The backend Flask application serves both the API endpoints and the static frontend files
- All frontend files are located in `backend/static/`
- API endpoints are available under `/api/` prefix:
  - Text steganography: `/api/text/embed` and `/api/text/extract`
  - AI analysis: `/api/ai/analyze_text`

## Features

The application includes:

1. **Text Steganography**:
   - Hide messages in plain text using whitespace variation
   - Hide messages using synonym substitution
   - Hide messages using binary word length encoding

2. **AI Analysis**:
   - Intelligent recommendation for optimal steganography techniques
   - Analysis of text for steganography suitability
   - Security insights and optimization tips

3. **User Interface**:
   - Clean, modern web interface
   - Responsive design that works on desktop and mobile
   - Intuitive workflow for embedding and extracting messages

## Troubleshooting

If you encounter any issues:

1. **Port already in use**: The application runs on port 5007 by default. If this port is in use, you can modify `backend/run.py` to use a different port.

2. **Missing dependencies**: Make sure all dependencies from `backend/requirements.txt` are installed.

3. **Static files not loading**: Ensure the `backend/static/` directory contains all the built frontend files.

4. **API errors**: Check that all required Python packages are installed and the shared steganography modules are accessible.

## Development Notes

- The application uses Flask's development server for local development
- For production deployment, consider using a production WSGI server like Gunicorn
- The frontend is a built Vue.js application, so frontend source files are not included in this repository