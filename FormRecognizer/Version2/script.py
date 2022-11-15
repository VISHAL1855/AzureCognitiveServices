import json
from sqlite3 import Date
data=open('inv2.json')
json_data=json.load(data)
company=json_data['analyzeResult']["documentResults"][0]["fields"]["Company"]["text"]
date=json_data['analyzeResult']["documentResults"][0]["fields"]["Date"]["text"]
invoice=json_data['analyzeResult']["documentResults"][0]["fields"]["Invoice number"]["text"]
total=json_data['analyzeResult']["documentResults"][0]["fields"]["Total"]["text"]
print("Company Name:",company)
print("Date:",date)
print("Invoice Number:",invoice)
print("Total:",total)