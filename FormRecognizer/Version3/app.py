from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask import Flask,request,render_template
app=Flask(__name__)

@app.route('/')
def upload():
    return render_template("upload.html")

@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        from azure.core.credentials import AzureKeyCredential
        from azure.ai.formrecognizer import DocumentAnalysisClient
        endpoint = "https://invoice1855.cognitiveservices.azure.com/"
        key = "1a89052829d84d43aa3358b74179acd6"

        model_id = "Invoicerecogniser"
        #formUrl = "https://taxguru.in/wp-content/uploads/2018/10/amzinv1-e1539229186364.jpg"

        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

        # Make sure your document's type is included in the list of document types the custom model can analyze
        f1=open(f.filename,"rb")
        poller = document_analysis_client.begin_analyze_document(model_id, document=f1, locale="en-US")
        result = poller.result()
        new=dict()
        for idx, document in enumerate(result.documents):
            for name, field in document.fields.items():
                field_value = field.value if field.value else field.content
                new[name]=field_value
    return new
if __name__ == '__main__':
   app.run(debug = True)

        
