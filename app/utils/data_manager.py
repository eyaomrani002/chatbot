import os
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import uuid
from threading import Lock
from . import initialize_logging
from .preprocess import preprocess_text, initialize_vectorizer

logger = initialize_logging()
ratings = pd.DataFrame(columns=['response_id', 'rating', 'timestamp'])

# Thread lock for dataset updates
_df_lock = Lock()

# Internal state
_state = {
    'df': None,
    'vectorizer': None,
    'X': None,
    'initialized': False
}

def initialize_data():
    """Initialize dataset and vectorizer."""
    if _state['initialized']:
        logger.debug("Data already initialized.")
        return
    
    try:
        _state['df'] = load_data()
        _state['vectorizer'], _state['X'] = initialize_vectorizer(_state['df'])
        _state['initialized'] = True
        logger.info("Dataset and vectorizer initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize data: {e}", exc_info=True)
        raise RuntimeError(f"Data initialization failed: {e}")

def load_data():
    """Load the dataset."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../data/iset_questions_reponses.csv')
    
    if not os.path.exists(data_path):
        logger.error(f"Dataset file not found at {data_path}")
        raise FileNotFoundError(f"Dataset file not found at {data_path}. Please ensure 'iset_questions_reponses.csv' exists in 'app/data/'.")
    
    try:
        df = pd.read_csv(data_path, encoding='utf-8')
        logger.debug(f"Loaded dataset from {data_path} with {len(df)} rows.")
        return df
    except Exception as e:
        logger.error(f"Error loading dataset from {data_path}: {e}")
        raise

def get_df_lock():
    """Return a thread lock for dataset updates."""
    return _df_lock

def get_df():
    """Return the dataset."""
    if not _state['initialized']:
        raise RuntimeError("Data not initialized. Please check server logs.")
    return _state['df']

def get_vectorizer():
    """Return the vectorizer."""
    if not _state['initialized']:
        raise RuntimeError("Data not initialized. Please check server logs.")
    return _state['vectorizer']

def get_X():
    """Return the vectorized questions."""
    if not _state['initialized']:
        raise RuntimeError("Data not initialized. Please check server logs.")
    return _state['X']

def get_best_response(user_input):
    """Find the best response based on cosine similarity."""
    if not _state['initialized']:
        logger.error("Cannot process response: Data not initialized.")
        raise RuntimeError("Data not initialized. Please check server logs.")
    
    df = _state['df']
    vectorizer = _state['vectorizer']
    X = _state['X']
    
    logger.debug(f"Processing input: {user_input}")
    processed_input = preprocess_text(user_input)
    input_vec = vectorizer.transform([processed_input])
    similarities = cosine_similarity(input_vec, X)
    max_idx = similarities.argmax()
    response = {
        'answer': df.iloc[max_idx]['Réponse'],
        'link': df.iloc[max_idx]['Lien'],
        'category': df.iloc[max_idx]['Catégorie'],
        'response_id': str(uuid.uuid4()),
        'confidence': float(similarities.max())
    }
    logger.debug(f"Generated response: {response}")
    return response

def add_response(data):
    """Add a new question/response to the dataset."""
    if not _state['initialized']:
        logger.error("Cannot add response: Data not initialized.")
        return {'error': 'Data not initialized. Please check server logs.'}, 500
    
    df = _state['df']
    vectorizer = _state['vectorizer']
    
    try:
        if not data or 'question' not in data or 'response' not in data:
            return {'error': 'Missing question or response data'}, 400

        import bleach
        new_row = pd.DataFrame([{
            'Question': bleach.clean(data['question']),
            'Réponse': bleach.clean(data['response']),
            'Lien': bleach.clean(data.get('link', '')),
            'Catégorie': bleach.clean(data.get('category', 'Général')),
            'Rating': 0
        }])
        
        with _df_lock:
            _state['df'] = pd.concat([df, new_row], ignore_index=True)
            _state['df']['Processed_Question'] = _state['df']['Question'].apply(preprocess_text)
            _state['X'] = vectorizer.fit_transform(_state['df']['Processed_Question'])
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(base_dir, '../data/iset_questions_reponses.csv')
            _state['df'].to_csv(data_path, index=False, encoding='utf-8')
        
        return {'success': True}, 200
    
    except Exception as e:
        logger.error(f"Error in add_response: {e}", exc_info=True)
        return {'error': 'An internal error occurred.'}, 500

def rate_response(data):
    """Record a response rating."""
    global ratings
    try:
        if not data or 'response_id' not in data or 'rating' not in data:
            return {'error': 'Missing response_id or rating data'}, 400

        ratings = pd.concat([ratings, pd.DataFrame([{
            'response_id': data['response_id'],
            'rating': data['rating'],
            'timestamp': pd.Timestamp.now()
        }])], ignore_index=True)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ratings_path = os.path.join(base_dir, '../data/ratings.csv')
        ratings.to_csv(ratings_path, index=False, encoding='utf-8')
        
        return {'success': True}, 200
    
    except Exception as e:
        logger.error(f"Error in rate_response: {e}", exc_info=True)
        return {'error': 'An internal error occurred.'}, 500