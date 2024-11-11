import json
import os
import re

def read_json_files(directory):
    documents = []
    files = sorted(os.listdir(directory), key=lambda x: int(x.split('_')[1].split('.')[0]))

    for filename in files:
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r',encoding='utf-8') as file:
                data = json.load(file)
                content = data['text'].lower()
                content = re.sub(r'[^a-zA-Z0-9\s]', ' ', content)
                documents.append(content)
    return documents
