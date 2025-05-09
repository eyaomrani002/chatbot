from sklearn.metrics.pairwise import cosine_similarity
import uuid
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer

class NaiveBayesModel:
    def __init__(self, df, vectorizer, tfidf_matrix):
        self.df = df
        self.vectorizer = vectorizer
        self.tfidf_matrix = tfidf_matrix
        self.stemmer = FrenchStemmer()
        self.stopwords = stopwords.words('french')
    
    def preprocess_text(self, text):
        text = text.lower()
        text = ''.join(c for c in text if c not in '0123456789' + string.punctuation)
        tokens = nltk.word_tokenize(text, language='french')
        tokens = [self.stemmer.stem(word) for word in tokens if word not in self.stopwords]
        return ' '.join(tokens)
    
    def get_response(self, question):
        processed_question = self.preprocess_text(question)
        input_vec = self.vectorizer.transform([processed_question])
        similarities = cosine_similarity(input_vec, self.tfidf_matrix)
        max_idx = similarities.argmax()
        return {
            'answer': self.df.iloc[max_idx]['Réponse'],
            'link': self.df.iloc[max_idx]['Lien'],
            'category': self.df.iloc[max_idx]['Catégorie'],
            'response_id': str(uuid.uuid4()),
            'confidence': float(similarities.max()),
            'ask_for_response': similarities.max() < 0.3
        }