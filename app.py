from flask import Flask, request, jsonify
from PIL import Image
import io
import easyocr
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Initialize EasyOCR reader with CPU and lowest PyTorch version
reader = easyocr.Reader(['en'], gpu=False)

@app.route('/detect_text', methods=['POST'])
def detect_text():
    """
    Detect text from an uploaded image.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The image file to process
    responses:
      200:
        description: Text extracted successfully
        schema:
          properties:
            extracted_text:
              type: string
              description: The text extracted from the image
      400:
        description: Error if no file provided or no selected file
    """
    # Check if an image file is present in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    extracted_text = process_image(file)
    if extracted_text:
        return jsonify({'extracted_text': extracted_text}), 200
    else:
        return jsonify({'error': 'Failed to extract text from the image'}), 400

def process_image(file):
    try:
        # Read image from memory
        image = Image.open(io.BytesIO(file.read()))

        # Use EasyOCR to extract text from the image
        result = reader.readtext(image)

        # Concatenate all recognized text
        extracted_text = ' '.join([text[1] for text in result])

        return extracted_text
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
