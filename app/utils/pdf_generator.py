from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os
import bleach
from .logging import initialize_logging
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

logger = initialize_logging()

def generate_summary(conversations):
    """Generate a summary of conversation topics using keyword extraction."""
    if not conversations:
        return "No conversations to summarize."
    
    # Extract keywords using TF-IDF
    texts = [conv['question'] + ' ' + conv['answer'] for conv in conversations if isinstance(conv, dict)]
    vectorizer = TfidfVectorizer(max_features=5)
    X = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    
    # Get top keywords
    keywords = feature_names.tolist()
    return f"Summary of topics discussed: {', '.join(keywords)}"

def export_conversations(data):
    """Export conversations to PDF with a summary."""
    try:
        if not data or 'conversations' not in data or not isinstance(data['conversations'], list):
            return {'error': 'Invalid or missing conversation data'}, 400

        valid_conversations = [conv for conv in data['conversations'] if isinstance(conv, dict) and 'question' in conv and 'answer' in conv]
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Load Amiri font
        try:
            font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../fonts', 'Amiri-Regular.ttf')
            pdfmetrics.registerFont(TTFont('Amiri', font_path))
            p.setFont('Amiri', 12)
        except Exception as e:
            logger.warning(f"Failed to load Amiri font, using Helvetica: {e}")
            p.setFont('Helvetica', 12)

        y = 750
        # Add summary
        summary = generate_summary(valid_conversations)
        p.drawString(50, y, "Conversation Summary:")
        p.drawString(50, y-20, summary[:100])
        y -= 40
        
        # Add conversations
        for conv in valid_conversations:
            question = bleach.clean(str(conv['question']))[:100]
            answer = bleach.clean(str(conv['answer']))[:100]
            p.drawString(50, y, f"Q: {question}")
            p.drawString(50, y-20, f"R: {answer}")
            y -= 40
            if y < 50:
                p.showPage()
                p.setFont('Amiri' if 'Amiri' in pdfmetrics.getRegisteredFontNames() else 'Helvetica', 12)
                y = 750
        
        if not valid_conversations:
            p.setFont('Helvetica', 12)
            p.drawString(50, 750, "No valid conversations found.")
        
        p.save()
        buffer.seek(0)
        return buffer, 'application/pdf', 'conversation.pdf'
    
    except Exception as e:
        logger.error(f"Error in export_conversations: {e}", exc_info=True)
        return {'error': 'An internal error occurred.'}, 500