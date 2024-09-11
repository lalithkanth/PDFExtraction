from flask import Flask, request, jsonify
import requests
from PyPDF2 import PdfReader
from io import BytesIO

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def extract_text():
    data = request.get_json()
    urls = data.get('urls')
    
    if not urls or not isinstance(urls, list):
        return jsonify({"error": "No URLs provided or URLs are not in a list"}), 400

    extracted_texts = []
    errors = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.
            
            # Load PDF from in-memory bytes
            with BytesIO(response.content) as pdf_file:
                reader = PdfReader(pdf_file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() + '\n'
            extracted_texts.append({"url": url, "text": text})
        
        except requests.RequestException as e:
            errors.append({"url": url, "error": str(e)})
        except Exception as e:
            errors.append({"url": url, "error": "Failed to process the PDF"})

    return jsonify({"extracted_texts": extracted_texts, "errors": errors})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
