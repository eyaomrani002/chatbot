from flask import Flask
import os

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder='static-ot')
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from app.utils import initialize_nltk, initialize_logging
    initialize_nltk()
    logger = initialize_logging()
    logger.debug("Flask app initialized with upload folder: %s", app.config['UPLOAD_FOLDER'])

    from app.routes.api import api
    app.register_blueprint(api)
    
    return app