import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///accommodation.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Email Configuration
    # Set these as environment variables for security:
    # MAIL_USERNAME=your-email@gmail.com
    # MAIL_PASSWORD=your-app-password
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'rahulrgadgimata@gmail.com'
    # IMPORTANT: Use Gmail App Password, not regular password!
    # Get App Password from: https://myaccount.google.com/apppasswords
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''  # Set via environment variable for security
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME') or 'rahulrgadgimata@gmail.com'

