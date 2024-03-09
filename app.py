from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import re
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'tesseract.exe'

@app.route('/detect_text', methods=['POST'])
def detect_text():
    """
    Detect text from an uploaded image and extract total payable amount.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The image file to process
    responses:
      200:
        description: Total payable amount extracted successfully
        schema:
          properties:
            total_payable:
              type: string
              description: The total payable amount extracted from the image
      400:
        description: Error if no file provided or no selected file
    """
    # Check if an image file is present in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    image = Image.open(file)
    extracted_text = pytesseract.image_to_string(image)
    total_payable = extract_total_payable(extracted_text)
    return jsonify({'total_payable': total_payable}), 200

def extract_total_payable(text):
    keywords = ["TOTAL DUE", "TOTAL PAYABLE", "TOTAL ELECTRICITY"]
    total_payable = None
    for keyword in keywords:
        match = re.search(rf'{keyword}[\s:]*([$€£¥]?[\d,.]+)', text, re.IGNORECASE)
        if match:
            total_payable = match.group(1)
            break

    return total_payable

if __name__ == '__main__':
    app.run(debug=True)
