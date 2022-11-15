########### Python Form Recognizer Async Analyze #############
import json
import time
import getopt
import sys
import os
from requests import get, post

def runAnalysis(input_file):
    # Endpoint URL
    endpoint = " INSERT ENDPOINT"
    # Subscription Key
    apim_key = "INSERT CREADENTIALS "
    # Model ID
    model_id = "b5625d35-8396-4923-8a75-42d66b3b117d"
    # API version
    API_version = "v2.1"

    post_url = endpoint + "/formrecognizer/%s/custom/models/%s/analyze" % (API_version, model_id)
    params = {
        "includeTextDetails": True
    }

    post_url = endpoint + "/formrecognizer/%s/custom/models/%s/analyze" % (API_version, model_id)
    params = {
        "includeTextDetails": True
    }

    headers = {
        # Request headers
        'Content-Type': "image/jpeg",
        'Ocp-Apim-Subscription-Key': apim_key,
    }
    try:
        with open(input_file, "rb") as f:
            data_bytes = f.read()
    except IOError:
        print("Inputfile not accessible.")
        sys.exit(2)

    try:
        print('Initiating analysis...')
        resp = post(url = post_url, data = data_bytes, headers = headers, params = params)
        if resp.status_code != 202:
            print("POST analyze failed:\n%s" % json.dumps(resp.json()))
            quit()
        # print("POST analyze succeeded:\n%s" % resp.headers)
        print
        get_url = resp.headers["operation-location"]
    except Exception as e:
        print("POST analyze failed:\n%s" % str(e))
        quit()

    n_tries = 15
    n_try = 0
    wait_sec = 5
    max_wait_sec = 60
    print()
    print('Getting analysis results...')
    while n_try < n_tries:
        resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
        resp_json = resp.json()
        if resp.status_code != 200:
            print("GET analyze results failed:\n%s" % json.dumps(resp_json))
            quit()
        status = resp_json["status"]
        if status == "succeeded":
            new=dict()
            json_data=resp_json
            new["company"]=json_data['analyzeResult']["documentResults"][0]["fields"]["Company"]["text"]
            new["date"]=json_data['analyzeResult']["documentResults"][0]["fields"]["Date"]["text"]
            new["invoice"]=json_data['analyzeResult']["documentResults"][0]["fields"]["Invoice number"]["text"]
            new["total"]=json_data['analyzeResult']["documentResults"][0]["fields"]["Total"]["text"]
            """new["Company Name"]=company
            new["Date:"]=date
            new["Invoice Number:"]=invoice
            new["Total"]=total"""
    return new  

result=runAnalysis(input_file="inv3.jpg")
print(result)
