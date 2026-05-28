import os

class Config:
    """Base configuration settings for the Flask application."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-ckc-101'
    PORT = int(os.environ.get('PORT') or 19191)
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
