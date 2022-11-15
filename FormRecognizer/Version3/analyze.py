
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

endpoint = "INSERT CREADENTIALS "
key = "INSERT CREADENTIALS "

model_id = "Invoicerecogniser"
formUrl = "https://taxguru.in/wp-content/uploads/2018/10/amzinv1-e1539229186364.jpg"

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Make sure your document's type is included in the list of document types the custom model can analyze
poller = document_analysis_client.begin_analyze_document_from_url(model_id, formUrl)
result = poller.result()
new=dict()
for idx, document in enumerate(result.documents):
    for name, field in document.fields.items():
        field_value = field.value if field.value else field.content
        # print(name,':',field_value)
        new[name]=field_value
    print(new)
        


