import json
import os
import re

def read_json_files(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r',encoding='utf-8') as file:
                data = json.load(file)
                content = data['text'].lower()
                content = re.sub(r'[^a-zA-Z0-9\s]', ' ', content)
                documents.append(content)
    return documents
