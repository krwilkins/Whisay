from flask import Flask, request, jsonify, send_file, send_from_directory
import pytesseract
from gtts import gTTS
from PIL import Image
from googletrans import Translator
import io
import os
from langdetect import detect
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Set up Tesseract paths
os.environ['TESSDATA_PREFIX'] = r'/app/.apt/usr/share/tesseract-ocr/5/tessdata'
pytesseract.pytesseract.tesseract_cmd = r'/app/.apt/usr/bin/tesseract'

# Initialize Flask app
app = Flask(__name__)
CORS(app)

def speak(text, filename="output.mp3"):
    """
    Converts text to speech using gTTS and saves it as an MP3 file.
    
    Args:
        text (str): The text to be converted to speech.
        filename (str): The name of the output MP3 file.

    Returns:
        str: The filename of the saved MP3 file.
    """
    tts = gTTS(text=str(text), lang='en')
    tts.save(filename)
    return filename

def clean_text(text):
    """
    Cleans and formats the text for better readability.
    
    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned and formatted text.
    """
    text = ' '.join(str(text).split())
    sentences = text.split('.')
    formatted_text = '. '.join(sentence.strip().capitalize() for sentence in sentences if sentence)
    return formatted_text

@app.route('/translate', methods=['POST'])
def translate_text():
    """
    Extracts text from an uploaded image, translates it to English, 
    converts the translated text to speech, and sends the audio file as a response.
    
    Returns:
        Response: An audio file or a JSON error message.
    """
    if 'image' not in request.files:
        logging.error('No image part in the request.')
        return jsonify({"error": "No image part"}), 400
    file = request.files['image']
    if file.filename == '':
        logging.error('No selected file.')
        return jsonify({"error": "No selected file"}), 400
    try:
        # Open and preprocess the image
        image = Image.open(io.BytesIO(file.read())).convert('L')
        text = pytesseract.image_to_string(image)
        logging.debug(f"Extracted text: {text}")

        if not text.strip():
            logging.error('Extracted text is empty or invalid.')
            return jsonify({"error": "Extracted text is empty or invalid"}), 400

        # Detect language and translate text
        src_lang = detect(text)
        translator = Translator()
        translated = translator.translate(text, src=src_lang, dest='en').text
        logging.debug(f"Translated text: {translated}")

        cleaned_text = clean_text(translated)
        logging.debug(f"Cleaned text: {cleaned_text}")

        # Convert translated text to speech
        audio_filename = speak(cleaned_text)
        if os.path.exists(audio_filename):
            return send_file(audio_filename, mimetype='audio/mpeg')
        else:
            logging.error('Audio file not found.')
            return jsonify({"error": "Audio file not found."}), 404
    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_home():
    """
    Serves the homepage.
    
    Returns:
        Response: The index.html file.
    """
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """
    Serves static files.
    
    Args:
        path (str): The path of the static file.

    Returns:
        Response: The requested static file.
    """
    return send_from_directory('frontend', path)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
