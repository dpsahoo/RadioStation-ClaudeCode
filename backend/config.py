"""
Configuration management for Radio Calico application.
Handles environment variables and application settings.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Application configuration class."""
    
    # API Keys
    CLAUDE_API_KEY: Optional[str] = None
    
    # Database
    DATABASE_URL: str = "sqlite:///radio.db"
    DATABASE_PATH: str = "radio.db"
    
    # Stream Configuration
    STREAM_URL: str = "https://d3d4yli4hf5bmh.cloudfront.net/hls/live.m3u8"
    METADATA_URL: str = "https://d3d4yli4hf5bmh.cloudfront.net/metadatav2.json"
    COVER_ART_URL: str = "https://d3d4yli4hf5bmh.cloudfront.net/cover.jpg"
    
    # Flask Configuration
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 5000
    
    # Security
    ALLOWED_ORIGINS: list = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/radio.log"
    
    def __post_init__(self):
        """Load configuration from environment variables."""
        self.CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
        self.DATABASE_URL = os.getenv('DATABASE_URL', self.DATABASE_URL)
        self.DATABASE_PATH = os.getenv('DATABASE_PATH', self.DATABASE_PATH)
        self.STREAM_URL = os.getenv('STREAM_URL', self.STREAM_URL)
        self.METADATA_URL = os.getenv('METADATA_URL', self.METADATA_URL)
        self.COVER_ART_URL = os.getenv('COVER_ART_URL', self.COVER_ART_URL)
        self.SECRET_KEY = os.getenv('FLASK_SECRET_KEY', self.SECRET_KEY)
        self.DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        self.HOST = os.getenv('FLASK_HOST', self.HOST)
        self.PORT = int(os.getenv('FLASK_PORT', self.PORT))
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', self.LOG_LEVEL)
        self.LOG_FILE = os.getenv('LOG_FILE', self.LOG_FILE)
        
        # Parse allowed origins
        origins_str = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000')
        self.ALLOWED_ORIGINS = [origin.strip() for origin in origins_str.split(',')]


def load_config() -> Config:
    """Load and return application configuration."""
    return Config()


# Global config instance
config = load_config()