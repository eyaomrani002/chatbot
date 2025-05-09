from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
import os
from app.utils import initialize_logging
from app.utils.data_manager import get_best_response, add_response, rate_response, get_df_lock, initialize_data
from app.utils.pdf_generator import export_conversations

logger = initialize_logging()
api = Blueprint('api', __name__)

# Initialize data
try:
    initialize_data()
except Exception as e:
    logger.error(f"Failed to initialize data at startup: {e}", exc_info=True)
    raise

@api.route('/')
def home():
    """Render the chatbot homepage."""
    return render_template('chat.html')

@api.route('/chat', methods=['POST'])
def chat_handler():
    """Handle user messages or uploaded files."""
    try:
        pdf = request.files.get('pdf_file')
        image = request.files.get('image_file')
        uploaded_files = []

        # Validate and save PDF
        if pdf and pdf.filename:
            logger.debug(f"Processing PDF: {pdf.filename}")
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

        # Validate and save image
        if image and image.filename:
            logger.debug(f"Processing image: {image.filename}")
            if image.content_type not in ['image/png', 'image/jpeg']:
                return jsonify({'error': 'Fichier image invalide (PNG/JPEG requis)'}), 400
            image.seek(0, os.SEEK_END)
            if image.tell() > current_app.config['MAX_CONTENT_LENGTH']:
                return jsonify({'error': 'Fichier image trop volumineux (max 5 Mo)'}), 400
            image.seek(0)
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            uploaded_files.append(image_path)

        question = request.form.get('message', '')
        logger.debug(f"Received question: {question}")
        if not question and not (pdf or image):
            return jsonify({'error': 'Aucune question ou fichier fourni'}), 400

        response = get_best_response(question or "Fichier uploadé")
        response['ask_for_response'] = response['confidence'] < 0.3

        # Clean up uploaded files
        for file_path in uploaded_files:
            try:
                os.remove(file_path)
            except Exception as e:
                logger.error(f"Erreur lors de la suppression du fichier {file_path}: {e}")

        logger.debug(f"Sending response: {response}")
        return jsonify(response)
    
    except RuntimeError as e:
        logger.error(f"Erreur dans /chat: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Erreur dans /chat: {e}", exc_info=True)
        return jsonify({'error': 'Une erreur interne est survenue. Veuillez réessayer.'}), 500

@api.route('/add_response', methods=['POST'])
def add_response_route():
    """Add a new question/response to the dataset."""
    result, status = add_response(request.json)
    return jsonify(result), status

@api.route('/rate', methods=['POST'])
def rate_response_route():
    """Record a response rating."""
    result, status = rate_response(request.json)
    return jsonify(result), status

@api.route('/export_conversations', methods=['POST'])
def export_conversations_route():
    """Export conversations to PDF."""
    result = export_conversations(request.json)
    if isinstance(result, tuple):
        buffer, mimetype, filename = result
        return send_file(buffer, mimetype=mimetype, download_name=filename)
    return jsonify(result), result.get('status', 500)