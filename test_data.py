import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import logging
import json

# Configurer le logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_test_image(text, filename="test.png"):
    """Crée une image avec du texte pour tester l'OCR."""
    img = Image.new('RGB', (300, 150), color='white')  # Augmenter la taille
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 20)  # Taille de police plus grande
    except:
        logger.warning("Police Arial non trouvée, utilisation de la police par défaut")
        font = ImageFont.load_default()
    draw.text((20, 60), text, fill='black', font=font)
    img.save(filename, format="PNG")
    logger.info(f"Image créée : {filename}")
    return filename

def test_ocr_extraction():
    """Teste l'extraction de texte via l'endpoint /chat."""
    url = "http://192.168.100.201:5000/chat"
    test_text = "Quels sont les horaires des cours d’informatique ?"
    image_path = create_test_image(test_text)

    try:
        with open(image_path, 'rb') as img_file:
            files = {
                "image_file": (image_path, img_file, "image/png"),
                "output_lang": (None, "fr"),
                "csrf_token": (None, "dummy_csrf_token")
            }
            headers = {"X-CSRFToken": "dummy_csrf_token"}
            response = requests.post(url, files=files, headers=headers, timeout=10)

        response.raise_for_status()
        data = response.json()

        logger.debug(f"Réponse JSON complète : {json.dumps(data, indent=2)}")

        if "error" in data:
            logger.error(f"Erreur serveur : {data['error']}")
            return False

        extracted_text = data.get("extracted_text", "")
        answer = data.get("answer", "")

        logger.info(f"Texte extrait : '{extracted_text}'")
        logger.info(f"Réponse du chatbot : '{answer}'")

        # Validation stricte : extracted_text doit être non vide et correspondre
        if not extracted_text:
            logger.error("Échec : Aucun texte extrait")
            return False
        if test_text.lower() not in extracted_text.lower() and extracted_text.lower() not in test_text.lower():
            logger.error(f"Échec : Texte attendu '{test_text}', obtenu '{extracted_text}'")
            return False

        logger.info("Succès : Le texte a été extrait correctement")
        return True

    except requests.RequestException as e:
        logger.error(f"Erreur réseau : {e}")
        return False
    except Exception as e:
        logger.error(f"Erreur inattendue : {e}")
        return False

if __name__ == "__main__":
    result = test_ocr_extraction()
    print("Test OCR :", "Succès" if result else "Échec")