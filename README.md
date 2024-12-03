Image Translator App

Overview
The Image Translator App allows users to take or upload a photo containing text, extract the text from the image, translate it to English, and then speak the translated text aloud. This app is built using Flask for the backend and HTML/CSS/JavaScript for the frontend. The app is hosted on Heroku.

Features
Image Upload: Users can upload a photo or take a new one using their device's camera.

Text Extraction: The app uses Tesseract OCR to extract text from the uploaded image.

Translation: The extracted text is translated to English using Google Translate.

Text-to-Speech: The translated text is then spoken aloud using gTTS (Google Text-to-Speech).

Limitations
The application currently struggles with text extraction on images taken with mobile device cameras. I will be investigating this further to find a solution.

The application also currently struggles with extracting text from languages that do not have a Latin-based script. I will be investigating this further to find a solution.

Requirements
Python 3.7+
Flask
pytesseract
Pillow
googletrans==4.0.0-rc1
gTTS
Flask-CORS
langdetect

Installation
Clone the repository:
git clone <repository_url>
cd <repository_directory>

Set up a virtual environment:
python -m venv venv
source venv/bin/activate

Install the required packages:
pip install -r requirements.txt

Make sure to set the Tesseract paths correctly in app.py:
os.environ['TESSDATA_PREFIX'] = r'/app/.apt/usr/share/tesseract-ocr/5/tessdata'
pytesseract.pytesseract.tesseract_cmd = r'/app/.apt/usr/bin/tesseract'

Usage
Run the Flask app:
python app.py
Open your web browser and navigate to http://localhost:5000.

Upload a photo containing text and click "Translate". The app will extract the text, translate it to English, and speak the translated text.

Deployment
To deploy the app on Heroku:

Create a Heroku app:
heroku create

Add the required buildpacks:
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-apt
heroku buildpacks:add heroku/python

Push the code to Heroku:
git push heroku master

Set the environment variables:
heroku config:set TESSDATA_PREFIX=/app/.apt/usr/share/tesseract-ocr/5/tessdata
heroku config:set TESSERACT_CMD=/app/.apt/usr/bin/tesseract

I have included a set of example images that I used for testing the app.
The app is currently live at the following URL:
https://whisay-cb5ee47d5934.herokuapp.com/
Please let me know once you have finished testing so I can take it down.