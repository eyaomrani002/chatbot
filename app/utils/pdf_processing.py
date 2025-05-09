import pdfplumber
import logging
import os

logger = logging.getLogger(__name__)

def extract_pdf_text(file_path):
    """
    Extrait le texte d'un fichier PDF.
    
    Args:
        file_path (str): Chemin vers le fichier PDF.
    
    Returns:
        str: Texte extrait ou message d'erreur.
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"Le fichier {file_path} n'existe pas.")
            return "Erreur : fichier introuvable."
        
        if not file_path.lower().endswith('.pdf'):
            logger.error(f"Type de fichier non supporté: {file_path}")
            return "Erreur : type de fichier non supporté."
        
        with pdfplumber.open(file_path) as pdf:
            extracted_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
            extracted_text = extracted_text.strip()
            if not extracted_text:
                extracted_text = "Aucun texte détecté dans le PDF."
            logger.info(f"Texte extrait du PDF: {extracted_text}")
            return extracted_text
    
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction du texte du PDF: {e}")
        return "Erreur lors de l'extraction du texte."