import logging

def initialize_logging():
    """Configure logging."""
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(__name__)