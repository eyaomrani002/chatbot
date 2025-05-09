import nltk
import logging
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer

# Initialize shared resources
french_stopwords = stopwords.words('french')
stemmer = FrenchStemmer()

def initialize_nltk():
    """Download NLTK data if not present."""
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

def initialize_logging():
    """Configure logging."""
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(__name__)