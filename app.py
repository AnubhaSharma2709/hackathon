from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import io
from PIL import Image
import easyocr

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/image_to_text', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'image',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'The image file to be converted to text'
        }
    ],
    'responses': {
        '200': {
            'description': 'Text extracted from the image'
        }
    }
})
def image_to_text():
    """
    Convert image to text using EasyOCR
    ---
    consumes:
      - multipart/form-data
    """
    try:
        # Extract image file from request data
        image_file = request.files['image']

        # Ensure that a file is selected
        if image_file.filename == '':
            return jsonify({'error': 'No selected file'})

        # Read the image from the request data
        img = Image.open(io.BytesIO(image_file.read()))

        # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'])

        # Extract text from the image using EasyOCR
        result = reader.readtext(img)

        # Extract text from EasyOCR result
        text = ' '.join([entry[1] for entry in result])

        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing the image', 'details': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
