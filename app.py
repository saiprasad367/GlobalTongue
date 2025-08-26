from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from PyPDF2 import PdfReader
import os
import speech_recognition as sr

app = Flask(__name__)
translator = Translator()

def translate_text(input_text, target_lang):
    try:
        translation = translator.translate(input_text, dest=target_lang)
        return translation.text
    except Exception as e:
        return f"Translation error: {str(e)}"

def translate_pdf(pdf_file, target_lang):
    try:
        pdf_reader = PdfReader(pdf_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                pdf_text += text + "\n"
        return pdf_text, translate_text(pdf_text, target_lang)
    except Exception as e:
        return "", f"Could not read PDF. Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    input_type = request.form.get('inputType')
    target_lang = request.form.get('targetLang')

    if input_type == 'text':
        input_text = request.form.get('inputText')
        translation = translate_text(input_text, target_lang)
        return jsonify({'extractedText': input_text, 'translation': translation})

    elif input_type == 'pdf':
        pdf_file = request.files['pdfFile']
        if pdf_file:
            extracted_text, translation = translate_pdf(pdf_file, target_lang)
            return jsonify({'extractedText': extracted_text, 'translation': translation})
        else:
            return jsonify({'error': 'No PDF file uploaded.'}), 400

    elif input_type == 'audio':
        audio_text = request.form.get('audioText')
        translation = translate_text(audio_text, target_lang)
        return jsonify({'extractedText': audio_text, 'translation': translation})

    return jsonify({'error': 'Invalid input type.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
