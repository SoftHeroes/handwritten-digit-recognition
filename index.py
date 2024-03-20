import base64
import numpy as np
from PIL import Image
import io
import cv2
import tensorflow as tf
from flask import Flask, render_template ,request, jsonify
from keras.preprocessing import image

import tensorflow as tf
app = Flask(__name__)

# Load the saved model
model = tf.keras.models.load_model('cnn_model.h5')

def preprocess_image(image_path):
    """Preprocesses an image and converts it to black and white."""
    # Open the image
    img = Image.open('processed_image_before.png')
    
    # Convert the image to grayscale
    bw_img = img.convert('L')

    return bw_img

@app.route("/")
def hello_world():
    return render_template('paint.html')

# API endpoint


@app.route("/predict", methods=['POST'])
def get_data():
# Get the image data from the request
    data = request.get_json()
    image_base64 = data.get('image')

# Split the string to extract the base64 data
    data_uri = image_base64.split(',')
    if len(data_uri) == 2:
        image_base64 = data_uri[1]
        
        # Decode the base64 data
        image_data = base64.b64decode(image_base64)

    # Convert the image data to a PIL Image object
    image_data = Image.open(io.BytesIO(image_data))

    image_data = tf.image.resize(image_data,[28,28])
    
    image_data = image.img_to_array(image_data)
    
    # Save the processed image as a file
    pil_image = Image.fromarray(image_data.squeeze().astype('uint8'))
    pil_image.save('processed_image_before.png')
    
    # Preprocess the image
    processed_image = np.expand_dims(preprocess_image(image_data), axis=0)
    
    # Save the processed image as a file
    pil_image = Image.fromarray(processed_image.squeeze().astype('uint8'))
    pil_image.save('processed_image.png')
    
    # Load the image in grayscale mode
    processed_image = Image.open('processed_image.png').convert('L')

    # Resize the image to the required input size of the model
    processed_image = processed_image.resize((28, 28))

    # Convert the image to a numpy array
    processed_image = np.array(processed_image)

    # Expand the dimensions to match the expected input shape of the model
    processed_image = np.expand_dims(processed_image, axis=0)

    # Reshape the image to have a single channel (since it's grayscale)
    processed_image = np.expand_dims(processed_image, axis=-1)


    prediction = model.predict(processed_image)

    # Return the prediction as JSON
    return jsonify({'predicted': int(np.argmax(prediction))})


if __name__ == "__main__":
    app.run(debug=True)
