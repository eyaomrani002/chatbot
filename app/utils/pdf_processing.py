import pdfplumber
import logging
import os
from pdf2image import convert_from_path
import pytesseract

logger = logging.getLogger(__name__)

# Configuration de Tesseract (même chemin que dans image_processing.py)
try:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
except Exception as e:
    logger.error(f"Erreur de configuration de Tesseract: {e}")

def process_pdf(pdf_path):
    """
    Extrait le texte d'un fichier PDF en utilisant pdfplumber et pytesseract (OCR).
    
    Args:
        pdf_path (str): Chemin vers le fichier PDF.
    
    Returns:
        str: Texte extrait ou message d'erreur.
    """
    try:
        if not os.path.exists(pdf_path):
            logger.error(f"Fichier PDF introuvable: {pdf_path}")
            return "Fichier PDF introuvable."

        if not pdf_path.lower().endswith('.pdf'):
            logger.error(f"Type de fichier non supporté: {pdf_path}")
            return "Erreur : type de fichier non supporté."

        # Essayer l'extraction textuelle avec pdfplumber
        extracted_text = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text.append(text.strip())
        except Exception as e:
            logger.warning(f"Échec de l'extraction textuelle avec pdfplumber: {e}")

        full_text = ' '.join(extracted_text)
        full_text = ' '.join(full_text.split())  # Normalise les espaces
        
        if full_text:
            logger.info(f"Texte extrait du PDF {pdf_path}: {full_text[:100]}...")
            return full_text
        
        # Si aucun texte, tenter l'OCR
        logger.info(f"Aucun texte détecté avec pdfplumber, tentative d'OCR pour {pdf_path}")
        try:
            images = convert_from_path(pdf_path)
            ocr_text = []
            for img in images:
                text = pytesseract.image_to_string(img, lang='fra+eng+ara', config='--psm 6').strip()
                if text:
                    ocr_text.append(text)
            
            full_text = ' '.join(ocr_text)
            full_text = ' '.join(full_text.split())
            
            if not full_text:
                logger.warning(f"Aucun texte détecté dans le PDF après OCR: {pdf_path}")
                return "Aucun texte détecté dans le PDF."
            
            logger.info(f"Texte OCR extrait du PDF {pdf_path}: {full_text[:100]}...")
            return full_text
        
        except Exception as e:
            logger.error(f"Erreur lors de l'OCR du PDF {pdf_path}: {e}")
            return "Erreur lors de l'extraction du texte."
    
    except Exception as e:
        logger.error(f"Erreur générale lors de l'extraction du texte du PDF {pdf_path}: {e}")
        return "Erreur lors de l'extraction du texte."