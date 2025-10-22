# Steganography Web Application

A web-based steganography application with AI integration for text-based steganography techniques.

## Project Structure

- `backend/` - Flask backend application
  - `app.py` - Main application file
  - `run.py` - Script to run the application
  - `requirements.txt` - Python dependencies
  - `static/` - Built frontend files
  - `routes/` - API endpoints
  - `config/` - Configuration files
- `shared/` - Core steganography implementation
  - `steganography/` - Text steganography algorithms and AI analyzer

## How to Run

1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Run the application:
   ```bash
   python backend/run.py
   ```

3. Access the application at http://localhost:5007

## Features

- Text Steganography: Hide messages in plain text using various techniques
- AI Analysis: Intelligent recommendation system for optimal steganography techniques
- Secure: End-to-end encryption for maximum security

## Key Techniques

- Whitespace variation
- Synonym substitution
- Binary word length encoding

The application is now ready for deployment with only the essential files needed for it to function properly.
