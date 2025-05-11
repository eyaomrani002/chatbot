# Mini-Projet Machine Learning: Chatbot pour le site ISET
# Description: Implémentation d'un chatbot utilisant NLP et Machine Learning pour guider les utilisateurs du site ISET.
# Ce code utilise Scikit-learn pour TF-IDF et KNN, et Flask pour l'interface web.

# Importation des bibliothèques nécessaires
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import string
import pandas as pd
from flask import Flask, request, jsonify, render_template

# Téléchargement des ressources NLTK (à exécuter une seule fois)
nltk.download('punkt')
nltk.download('stopwords')

# Initialisation des outils NLP
stemmer = SnowballStemmer('french')
stop_words = set(stopwords.words('french'))

# Fonction de prétraitement du texte
def preprocess_text(text):
    # Tokenisation
    tokens = word_tokenize(text.lower())
    # Suppression de la ponctuation et des stopwords
    tokens = [token for token in tokens if token not in string.punctuation and token not in stop_words]
    # Stemming
    tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(tokens)

# Création d'un dataset fictif (à remplacer par un dataset réel)
data = {
    'question': [
        'Quels sont les cours disponibles pour le département informatique ?',
        'Comment s’inscrire à un cours ?',
        'Où trouver le calendrier universitaire ?',
        'Quelles sont les démarches pour une inscription administrative ?',
        'Qui contacter pour des questions sur les bourses ?'
    ],
    'reponse': [
        'Les cours disponibles sont listés sur la page du département informatique : [Lien].',
        'Pour s’inscrire, visitez la section Inscription : [Lien].',
        'Le calendrier universitaire est disponible ici : [Lien].',
        'Consultez la page des démarches administratives : [Lien].',
        'Contactez le service des bourses via : [Lien].'
    ]
}
df = pd.DataFrame(data)

# Prétraitement des questions
df['question_processed'] = df['question'].apply(preprocess_text)

# Vectorisation avec TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['question_processed'])

# Entraînement du modèle KNN
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X, df['reponse'])

# Fonction pour obtenir une réponse
def get_response(user_question):
    # Prétraitement de la question utilisateur
    processed_question = preprocess_text(user_question)
    # Vectorisation
    question_vector = vectorizer.transform([processed_question])
    # Prédiction avec KNN
    response = knn.predict(question_vector)[0]
    # Calcul de la similarité cosinus pour validation
    similarity = cosine_similarity(question_vector, X).max()
    if similarity < 0.3:  # Seuil de similarité
        return "Désolé, je n’ai pas compris votre question. Pouvez-vous reformuler ?"
    return response

# Configuration de l'application Flask
app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour l'API du chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = get_response(user_input)
    return jsonify({'response': response})

# Template HTML pour l'interface
index_html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Chatbot ISET</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }
        #chat-container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; }
        #chat-box { height: 300px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
        #user-input { width: 80%; padding: 10px; }
        button { padding: 10px; background-color: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div id="chat-container">
        <h2>Chatbot ISET</h2>
        <div id="chat-box"></div>
        <input type="text" id="user-input" placeholder="Posez votre question...">
        <button onclick="sendMessage()">Envoyer</button>
    </div>
    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const chatBox = document.getElementById('chat-box');
            const message = input.value;
            if (message.trim() === '') return;
            
            // Afficher la question de l'utilisateur
            chatBox.innerHTML += `<p><strong>Vous :</strong> ${message}</p>`;
            input.value = '';
            
            // Envoyer la requête au serveur
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            
            // Afficher la réponse du chatbot
            chatBox.innerHTML += `<p><strong>Chatbot :</strong> ${data.response}</p>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        // Permettre l'envoi avec la touche Entrée
        document.getElementById('user-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

# Sauvegarde du template HTML
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)