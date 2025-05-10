from flask import Blueprint, request, jsonify, send_file, current_app, render_template
from werkzeug.utils import secure_filename
import os
import logging
from .utils.pdf_generator import export_conversations
from .utils.history import save_conversation
from .utils.rating import migrate_ratings, rate_response
from .models.naive_bayes import NaiveBayesModel
import uuid
from .image_processing import process_image
from .pdf_processing import process_pdf

bp = Blueprint('routes', __name__)
logger = logging.getLogger(__name__)

@bp.route('/')
def home():
    return render_template('chat.html')

@bp.route('/chat', methods=['POST'])
def chat():
    try:
        pdf = request.files.get('pdf_file')
        image = request.files.get('image_file')
        question = request.form.get('message', '').strip()
        output_lang = request.form.get('output_lang', 'fr')
        extracted_text = ''
        questions = []

        supported_langs = ['fr', 'en', 'ar']
        if output_lang not in supported_langs:
            return jsonify({'error': f"Langue non supportée: {output_lang}. Langues supportées: {supported_langs}", 'extracted_text': extracted_text, 'questions': questions}), 400

        if not question and not (pdf or image):
            return jsonify({'error': 'Aucune question ou fichier fourni', 'extracted_text': extracted_text, 'questions': questions}), 400
        
        uploaded_files = []
        if pdf and pdf.filename:
            if not pdf.filename.endswith('.pdf') or pdf.content_type != 'application/pdf':
                logger.error(f"Fichier PDF invalide: {pdf.filename}")
                return jsonify({'error': 'Fichier PDF invalide', 'extracted_text': extracted_text, 'questions': questions}), 400
            pdf.seek(0, os.SEEK_END)
            if pdf.tell() > current_app.config['MAX_CONTENT_LENGTH']:
                logger.error(f"Fichier PDF trop volumineux: {pdf.filename} ({pdf.tell()} bytes)")
                return jsonify({'error': 'Fichier PDF trop volumineux (max 5 Mo)', 'extracted_text': extracted_text, 'questions': questions}), 400
            pdf.seek(0)
            filename = secure_filename(pdf.filename)
            pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            pdf.save(pdf_path)
            uploaded_files.append(pdf_path)
    
            extracted_text, questions = process_pdf(pdf_path)
            logger.debug(f"Texte extrait du PDF: '{extracted_text[:100]}...'")
            logger.debug(f"Questions détectées dans le PDF: {questions}")
            if extracted_text in [
                "Aucun texte détecté dans le PDF.",
                "Erreur lors du traitement du PDF.",
                "Fichier PDF introuvable.",
                "Erreur : type de fichier non supporté."
            ]:
                return jsonify({'error': extracted_text, 'extracted_text': extracted_text, 'questions': questions}), 400
        
        if image and image.filename:
            if image.content_type not in ['image/png', 'image/jpeg']:
                return jsonify({'error': 'Fichier image invalide (PNG/JPEG requis)', 'extracted_text': extracted_text, 'questions': questions}), 400
            image.seek(0, os.SEEK_END)
            if image.tell() > current_app.config['MAX_CONTENT_LENGTH']:
                return jsonify({'error': 'Fichier image trop volumineux (max 5 Mo)', 'extracted_text': extracted_text, 'questions': questions}), 400
            image.seek(0)
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            uploaded_files.append(image_path)
            
            extracted_text = process_image(image_path)
            logger.debug(f"Texte extrait de l'image: '{extracted_text[:100]}...'")
            if extracted_text in [
                "Aucun texte détecté dans l'image.",
                "Erreur lors de l'extraction du texte.",
                "Fichier image introuvable.",
                "Image trop petite pour l'extraction de texte.",
                "Image non valide pour l'extraction de texte (faible contraste ou contenu)."
            ]:
                return jsonify({'error': extracted_text, 'extracted_text': extracted_text, 'questions': questions}), 400

        if not question and extracted_text:
            question = extracted_text[:1000]
        elif not question:
            return jsonify({'error': 'Aucun texte extrait ou question fournie', 'extracted_text': extracted_text, 'questions': questions}), 400

        logger.debug(f"Question envoyée au modèle: '{question[:100]}...'")
        model = NaiveBayesModel(current_app.config['DATAFRAME'], current_app.config['VECTORIZER'], current_app.config['TFIDF_MATRIX'])
        response = model.get_response(question)
        
        response['extracted_text'] = extracted_text
        response['questions'] = questions
        logger.debug(f"Réponse JSON envoyée: {response}")
        
        save_conversation(question, response['answer'], response['link'], response['category'], response['response_id'])
        
        for file_path in uploaded_files:
            try:
                os.remove(file_path)
            except Exception as e:
                logger.error(f"Erreur lors de la suppression du fichier {file_path}: {e}")
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Erreur dans /chat: {e}", exc_info=True)
        return jsonify({'error': 'Une erreur interne est survenue', 'extracted_text': extracted_text, 'questions': questions}), 500

@bp.route('/add_response', methods=['POST'])
def add_response():
    try:
        data = request.json
        if not data or 'question' not in data or 'response' not in data:
            return jsonify({'error': 'Données manquantes'}), 400
        
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
            'Processed_Question': preprocess_text(data['question']),
            'response_id': str(uuid.uuid4())
        }
        
        df = pd.concat([current_app.config['DATAFRAME'], pd.DataFrame([new_row])], ignore_index=True)
        current_app.config['DATAFRAME'] = df
        current_app.config['TFIDF_MATRIX'] = current_app.config['VECTORIZER'].fit_transform(df['Processed_Question'])
        df.to_csv(os.path.join(current_app.config['DATA_FOLDER'], 'iset_questions_reponses.csv'), index=False, encoding='utf-8')        
        return jsonify({'success': True})
    
    except Exception as e:
        logger.error(f"Erreur dans /add_response: {e}", exc_info=True)
        return jsonify({'error': 'Une erreur interne est survenue'}), 500

@bp.route('/rate', methods=['POST'])
def rate():
    # Migrate ratings.csv if needed
    migrate_ratings()
    # Process the rating
    return rate_response(request.json)

@bp.route('/export_conversations', methods=['POST'])
def export_conversations():
    try:
        data = request.json
        if not data or 'conversations' not in data:
            return jsonify({'error': 'Données manquantes'}), 400
        
        result = export_conversations(data)
        if isinstance(result, tuple):
            buffer, mimetype, download_name = result
            return send_file(
                buffer,
                mimetype=mimetype,
                download_name=download_name,
                as_attachment=True
            )
        else:
            return jsonify(result), result[1]
    
    except Exception as e:
        logger.error(f"Erreur dans /export_conversations: {e}", exc_info=True)
        return jsonify({'error': 'Une erreur interne est survenue'}), 500