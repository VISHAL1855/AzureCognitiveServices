import os, io, base64, operator, random
from flask import Flask, render_template, request, jsonify
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

PREDICTION_KEY = os.environ['0d8ca3c522d7452d8e68fc2ae0376365']
ENDPOINT = os.environ['https://centralindia.api.cognitive.microsoft.com/']
PROJECT_ID = os.environ['5a4bb1d3-ea5b-4b5d-9d5a-37318eb05294']
PUBLISH_ITERATION_NAME = os.environ['Dog vs Cat']
LABELS = ['Cat','Dog']

# Initialize the web application

app = Flask(__name__)

# The root route, returns the rendered 'home.html' template page
@app.route('/')
def home():
    page_data = {}
    return render_template('home.html', page_data = page_data)

# Our custom API endpoint where we will receive images
@app.route('/process_image', methods=['POST'])
def check_results():
    # Get the JSON passed to the request and extract the image
    body = request.get_json()
    image_bytes = base64.b64decode(body['image_base64'].split(',')[1])
    # image = io.BytesIO(image_bytes)

    predictor = CustomVisionPredictionClient(PREDICTION_KEY, endpoint=ENDPOINT)

    results = predictor.classify_image(
        PROJECT_ID, PUBLISH_ITERATION_NAME, image_bytes)
    
    predictions = {prediction.tag_name: prediction.probability for prediction in results.predictions}

    predicted = max(predictions.keys(), key=(lambda k: predictions[k]))

    return jsonify({'predicted': predicted,
                    'probability': predictions[predicted],
                    'opponent': LABELS[random.randint(0,4)]})