class SVMModel:
    def __init__(self, df, vectorizer, tfidf_matrix):
        self.df = df
        self.vectorizer = vectorizer
        self.tfidf_matrix = tfidf_matrix
    
    def get_response(self, question):
        # Placeholder: Use same logic as Naive Bayes
        from .naive_bayes import NaiveBayesModel
        model = NaiveBayesModel(self.df, self.vectorizer, self.tfidf_matrix)
        return model.get_response(question)