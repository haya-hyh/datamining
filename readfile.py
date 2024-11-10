import json
import os

def read_json_files(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r',encoding='utf-8') as file:
                data = json.load(file)
                documents.append(data['text'])
    return documents
