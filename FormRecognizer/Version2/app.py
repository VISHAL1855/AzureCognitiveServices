from operator import inv
from flask import Flask,send_file,request,render_template
import json
import time
import sys
import os
from requests import get, post
UPLOAD_FOLDER = 'data'



app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def upload():
    return render_template("upload.html")


@app.route("/scan",methods = ['GET', 'POST'])
def scan():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        # path_to_sample_documents=file1
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
    # res=inv_scanner(file1.filename)
    # return res
    input_file ='data/'+file1.filename
    file_type = 'image/png'
    output_file = 'output.json'
    data=dict()
    def runAnalysis(input_file, output_file, file_type):
        # Endpoint URL
        endpoint = r"INSERT CREADENTIALS "
        # Subscription Key
        apim_key = "INSERT CREADENTIALS "
        # Model ID
        model_id = "0d74c885-e9df-4a06-bb34-25a507da229b"
        post_url = endpoint + "/formrecognizer/v2.0/custom/models/%s/analyze" % model_id
        params = {
            "includeTextDetails": True
        }

        headers = {
            # Request headers
            'Content-Type': file_type,
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
            try:
                resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
                resp_json = resp.json()
                if resp.status_code != 200:
                    print("GET analyze results failed:\n%s" % json.dumps(resp_json))
                    quit()
                status = resp_json["status"]
                if status == "succeeded":
                    if output_file:
                        with open(output_file, 'w') as outfile:
                            json.dump(resp_json, outfile, indent=2, sort_keys=True)
                            json_data=resp_json
                            merchant_name=json_data['analyzeResult']['documentResults'][0]['fields']['MerchantName']['text']
                            total=json_data['analyzeResult']['documentResults'][0]['fields']['Total']['text']
                            date=json_data['analyzeResult']['documentResults'][0]['fields']['TransactionDate']['text']
                            data["MerchantName"]=merchant_name
                            data["Total"]=total
                            data["Date"]=date
                    # print(data)
                    # return(data)
                    # print("Analysis succeeded:\n%s" % json.dumps(resp_json, indent=2, sort_keys=True))
                    # quit()
                    break
                if status == "failed":
                    print("Analysis failed:\n%s" % json.dumps(resp_json))
                    quit()
                # Analysis still running. Wait and retry.
                time.sleep(wait_sec)
                n_try += 1
                wait_sec = min(2*wait_sec, max_wait_sec)     
            except Exception as e:
                msg = "GET analyze results failed:\n%s" % str(e)
                print(msg)
                quit()
        print("Analyze operation did not complete within the allocated time.")
    runAnalysis(input_file, output_file, file_type)
    return data

  

if __name__ == "__main__":
    app.run(debug=True)
