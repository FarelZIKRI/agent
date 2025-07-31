#!/usr/bin/env python3
"""
Gemini AI Agent - Main Application Runner

This script starts the Gemini AI Agent web application.
Make sure to set your GEMINI_API_KEY environment variable before running.
"""

import os
import sys
import logging
from config import get_config, Config

def setup_logging(config):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main application entry point"""
    try:
        # Get configuration
        config = get_config()()
        
        # Validate configuration
        config.validate_config()
        
        # Setup logging
        setup_logging(config)
        logger = logging.getLogger(__name__)
        
        # Import and create Flask app
        from web_app import app
        
        logger.info(f"🚀 Starting Gemini AI Agent")
        logger.info(f"📍 Environment: {config.FLASK_ENV}")
        logger.info(f"🔗 URL: http://{config.HOST}:{config.PORT}")
        logger.info(f"🤖 Model: {config.GEMINI_MODEL}")
        
        # Run the application
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.FLASK_DEBUG
        )
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("💡 Please check your .env file and ensure all required variables are set.")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()