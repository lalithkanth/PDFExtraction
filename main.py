from flask import Flask, request, jsonify
import requests
from PyPDF2 import PdfReader
from io import BytesIO

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def extract_text():
    data = request.get_json()
    pdf_url = data.get('url')
    
    if not pdf_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        
        # Load PDF from in-memory bytes
        with BytesIO(response.content) as pdf_file:
            reader = PdfReader(pdf_file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
        
        return jsonify({"extracted_text": text})
    
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Failed to process the PDF"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
