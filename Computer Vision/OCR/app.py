
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
from flask import Flask,request
app=Flask(__name__)
@app.route("/home",methods=["GET","POST"])
def home():
    if request.method=="POST":

        url = request.form.get('url')


        '''
        Authenticate
        Authenticates your credentials and creates a client.
        '''
        subscription_key = "2bb6d9c22a00413db2b203c33514113e"
        endpoint = "https://compvsinst.cognitiveservices.azure.com/"

        computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
        '''
        END - Authenticate
        '''

        '''
        OCR: Read File using the Read API, extract text - remote
        This example will extract text in an image, then print results, line by line.
        This API call can also extract handwriting style text (not shown).
        '''
        print("===== Read File - remote =====")
        # Get an image with text
        # read_image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"

        # Call API with URL and raw response (allows you to get the operation location)
        read_response = computervision_client.read(url,  raw=True)

        # Get the operation location (URL with an ID at the end) from the response
        read_operation_location = read_response.headers["Operation-Location"]
        # Grab the ID from the URL
        operation_id = read_operation_location.split("/")[-1]

        # Call the "GET" API and wait for it to retrieve the results 
        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)
        output=" "
        # Print the detected text, line by line
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    output+=line.text
        '''
        END - Read File - remote
        '''

        # print("End of Computer Vision quickstart.")
    return output
if __name__ == "__main__":
    app.run(debug=True,port=8000)



