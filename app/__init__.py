from flask import Flask
import os
from app.utils import initialize_nltk, initialize_logging
from app.routes.api import api

def create_app():
    """Create and configure the Flask app."""
    # Use absolute path for template and static folders
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_folder = os.path.join(base_dir, 'templates')
    static_folder = os.path.join(base_dir, 'static-ot')
    
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    
    # Configuration
    app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB limit
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize NLTK and logging
    initialize_nltk()
    initialize_logging()
    
    # Register routes
    app.register_blueprint(api)
    
    return app