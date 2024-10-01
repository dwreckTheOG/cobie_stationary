import os

class Config:
    """Base configuration class."""

    # Flask settings
    SECRET_KEY = os.urandom(24)  # Change 'your_secret_key' to a secure value
    WTF_CSRF_ENABLED = True
    DEBUG = os.environ.get('DEBUG', True)

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')  # Default to SQLite if not set
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking to save resources
