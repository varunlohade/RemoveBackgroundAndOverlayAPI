import rembg
import numpy as np
import cv2
from flask import Flask, request, jsonify, send_file
from PIL import Image
from io import BytesIO


app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route("/removeBackground", methods = ['POST'])
def removeBg():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    image_file = request.files['image']
    image = Image.open(image_file)

    # Convert the image to RGBA format
    image = image.convert('RGBA')

    # Create a transparent background
    alpha_mask = Image.new('RGBA', image.size, (0, 0, 0, 0))

    # Combine the image with the transparent background
    image = Image.alpha_composite(image, alpha_mask)

    # Convert the image to numpy array
    image_np = np.array(image)

    # Remove the background using rembg library
    output = rembg.remove(image_np)

    # Create a new PIL Image from the output
    output_image = Image.fromarray(output)

    # Save the output image as a BytesIO object
    output_bytes = BytesIO()
    output_image.save(output_bytes, format='PNG')
    output_bytes.seek(0)

    return send_file(output_bytes, mimetype='image/png')
    # return processed_image_jpeg.tobytes(), {'Content-Type':'image/jpeg'}
    
    



if __name__ == "__main__":
    app.run(debug = True, port = 8000)