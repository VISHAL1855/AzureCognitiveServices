
from flask import Flask,render_template,request
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os, time, uuid
app=Flask(__name__)
UPLOAD_FOLDER="Images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/scan",methods=['POST',"GET"])
def scan():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        # path_to_sample_documents=file1
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        path_to_sample_documents="Images/"+file1.filename
        

        # Replace with valid values
        ENDPOINT = "https://newcus-prediction.cognitiveservices.azure.com/"

        prediction_key = "5b31f138816a418d9874f07d249701c0"
        prediction_resource_id = "/subscriptions/0f401efe-c05c-46c4-9009-7a4e699648c2/resourceGroups/customvisiongrp/providers/Microsoft.CognitiveServices/accounts/newcus-Prediction"
        publish_iteration_name = "Iteration1"
        project_id="31e15828-2d9d-48a9-bd53-993560f220e4"
        # Now there is a trained endpoint that can be used to make a prediction
        prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
        predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
        data=dict()
        image_contents=open(file1.filename,"rb")
        results = predictor.classify_image(project_id, publish_iteration_name, image_contents.read())
        
        for prediction in results.predictions:
            print("\t" + prediction.tag_name +": {0:.2f}%".format(prediction.probability * 100))
            data[prediction.tag_name]=prediction.probability * 100
        if data["Dog"]>data["Cat"]:
            return "The given image is of Dog"
        else:
            return "The given image is of Cat"

if __name__ == "__main__":
    app.run(debug=True) 
    




