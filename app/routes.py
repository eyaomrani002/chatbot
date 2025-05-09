from flask import Blueprint, request, jsonify, send_file, current_app, render_template
from werkzeug.utils import secure_filename
import os
import pandas as pd
import bleach
from .utils.pdf_generator import generate_pdf
from .utils.history import save_conversation
from .models.naive_bayes import NaiveBayesModel
import uuid
import logging

bp = Blueprint('routes', __name__)
logger = logging.getLogger(__name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/chat', methods=['POST'])
def chat():
    try:
        pdf = request.files.get('pdf_file')
        image = request.files.get('image_file')
        question = request.form.get('message', '')
        output_lang = request.form.get('output_lang', 'fr')
        
        if not question and not (pdf or image):
            return jsonify({'error': 'Aucune question ou fichier fourni'}), 400
        
        uploaded_files = []
        if pdf and pdf.filename:
            if not pdf.filename.endswith('.pdf') or pdf.content_type != 'application/pdf':
                return jsonify({'error': 'Fichier PDF invalide'}), 400
            pdf.seek(0, os.SEEK_END)
            if pdf.tell() > current_app.config['MAX_CONTENT_LENGTH']:
                return jsonify({'error': 'Fichier PDF trop volumineux (max 5 Mo)'}), 400
            pdf.seek(0)
            filename = secure_filename(pdf.filename)
            pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            pdf.save(pdf_path)
            uploaded_files.append(pdf_path)
        
        if image and image.filename:
            if image.content_type not in ['image/png', 'image/jpeg']:
                return jsonify({'error': 'Fichier image invalide (PNG/JPEG requis)'}), 400
            image.seek(0, os.SEEK_END)
            if image.tell() > current_app.config['MAX_CONTENT_LENGTH']:
                return jsonify({'error': 'Fichier image trop volumineux (max 5 Mo)'}), 400
            image.seek(0)
            filename = secure_filename(pdf.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            uploaded_files.append(image_path)
        
        # Use Naive Bayes model for response
        model = NaiveBayesModel(current_app.config['DATAFRAME'], current_app.config['VECTORIZER'], current_app.config['TFIDF_MATRIX'])
        response = model.get_response(question or "Fichier uploadé")
        
        # Save conversation
        save_conversation(question, response['answer'], response['link'], response['category'], response['response_id'])
        
        # Clean up files
        for file_path in uploaded_files:
            try:
                os.remove(file_path)
            except Exception as e:
                logger.error(f"Error deleting file {file_path}: {e}")
        
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in /chat: {e}", exc_info=True)
        return jsonify({'error': 'Une erreur interne est survenue'}), 500

@bp.route('/add_response', methods=['POST'])
def add_response():
    try:
        data = request.json
        if not data or 'question' not in data or 'response' not in data:
            return jsonify({'error': 'Données manquantes'}), 400
        
        # Preprocess the new question
        def preprocess_text(text):
            import string
            from nltk.corpus import stopwords
            from nltk.stem.snowball import FrenchStemmer
            text = text.lower()
            text = ''.join(c for c in text if c not in '0123456789' + string.punctuation)
            tokens = nltk.word_tokenize(text, language='french')
            tokens = [FrenchStemmer().stem(word) for word in tokens if word not in stopwords.words('french')]
            return ' '.join(tokens)
        
        new_row = {
            'Question': bleach.clean(data['question']),
            'Réponse': bleach.clean(data['response']),
            'Lien': bleach.clean(data.get('link', '')),
            'Catégorie': bleach.clean(data.get('category', 'Général')),
            'Rating': 0,
            'Processed_Question': preprocess_text(data['question'])
        }
        
        df = pd.concat([current_app.config['DATAFRAME'], pd.DataFrame([new_row])], ignore_index=True)
        current_app.config['DATAFRAME'] = df
        current_app.config['TFIDF_MATRIX'] = current_app.config['VECTORIZER'].fit_transform(df['Processed_Question'])
        df.to_csv('iset_questions_reponses.csv', index=False, encoding='utf-8')
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error in /add_response: {e}", exc_info=True)
        return jsonify({'error': 'Une erreur interne est survenue'}), 500

@bp.route('/rate', methods=['POST'])
def rate():
    try:
        data = request.json
        if not data or 'response_id' not in data or 'rating' not in data:
            return jsonify({'error': 'Données manquantes'}), 400
        
        # Save rating to ratings.csv
        ratings_file = 'ratings.csv'
        rating_data = pd.DataFrame([{
            'response_id': data['response_id'],
            'rating': data['rating'],
            'timestamp': pd.Timestamp.now()
        }])
        if os.path.exists(ratings_file):
            rating_data.to_csv(ratings_file, mode='a', header=False, index=False)
        else:
            rating_data.to_csv(ratings_file, index=False)
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error in /rate: {e}", exc_info=True)
        return jsonify({'error': 'Une erreur interne est survenue'}), 500

@bp.route('/export_conversations', methods=['POST'])
def export_conversations():
    try:
        data = request.json
        if not data or 'conversations' not in data:
            return jsonify({'error': 'Données manquantes'}), 400
        
        pdf_buffer = generate_pdf(data['conversations'])
        return send_file(pdf_buffer, mimetype='application/pdf', download_name='conversation.pdf')
    except Exception as e:
        logger.error(f"Error in /export_conversations: {e}", exc_info=True)
        return jsonify({'error': 'Une erreur interne est survenue'}), 500