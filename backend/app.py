from flask import Flask, request, jsonify, send_from_directory
import pytesseract
from gtts import gTTS
from PIL import Image
from googletrans import Translator
import io
import os
from langdetect import detect
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)
os.environ['TESSDATA_PREFIX'] = r'/usr/share/tesseract-ocr/4.00/tessdata'
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

app = Flask(__name__)
CORS(app)

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")

def clean_text(text):
    text = ' '.join(text.split())
    sentences = text.split('.')
    formatted_text = '. '.join(sentence.strip().capitalize() for sentence in sentences if sentence)
    return formatted_text

@app.route('/translate', methods=['POST'])
def translate_text():
    if 'image' not in request.files:
        logging.error('No image part in the request.')
        return jsonify({"error": "No image part"}), 400
    file = request.files['image']
    if file.filename == '':
        logging.error('No selected file.')
        return jsonify({"error": "No selected file"}), 400
    try:
        image = Image.open(io.BytesIO(file.read()))
        text = pytesseract.image_to_string(image)
        logging.debug(f"Extracted text: {text}")
        src_lang = detect(text)
        translator = Translator()
        translated = translator.translate(text, src=src_lang, dest='en').text
        logging.debug(f"Translated text: {translated}")
        cleaned_text = clean_text(translated)
        logging.debug(f"Cleaned text: {cleaned_text}")
        speak(cleaned_text)
        return jsonify({"translated_text": cleaned_text})
    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_home():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
