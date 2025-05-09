from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import string
import re
import bleach
from . import french_stopwords, stemmer

def preprocess_text(text):
    """Preprocess text for search: clean, tokenize, stem."""
    if not isinstance(text, str):
        text = str(text)
    text = bleach.clean(text)
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text, language='french')
    tokens = [stemmer.stem(word) for word in tokens if word not in french_stopwords]
    return ' '.join(tokens)

def initialize_vectorizer(df):
    """Initialize vectorizer and transform questions."""
    df['Processed_Question'] = df['Question'].apply(preprocess_text)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['Processed_Question'])
    return vectorizer, X