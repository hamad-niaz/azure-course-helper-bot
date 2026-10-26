# Step 1: create the search index and fill it with the FAQ (run once)

import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("SEARCH_ENDPOINT", "").rstrip("/")
admin_key = os.getenv("SEARCH_KEY")
if not admin_key:
    raise ValueError("SEARCH_KEY is missing. Check your .env file.")

api = "?api-version=2024-07-01"

headers = {
    "api-key": admin_key,
    "Content-Type": "application/json"
}

base = endpoint.rstrip("/")

index = {
    "name": "faq",
    "fields": [
        {"name": "id", "type": "Edm.String", "key": True},
        {"name": "question", "type": "Edm.String", "searchable": True},
        {"name": "answer", "type": "Edm.String", "searchable": True},
        {
            "name": "category",
            "type": "Edm.String",
            "filterable": True,
            "facetable": True
        }
    ]
}

# Create or update the index
r = requests.put(
    f"{base}/indexes/faq{api}",
    headers=headers,
    json=index,
    timeout=30
)

print("Create index:", r.status_code)
r.raise_for_status()

# Load FAQ file from the same folder as this script
faq_path = os.path.join(os.path.dirname(__file__), "faq.json")

with open(faq_path, encoding="utf-8") as file:
    docs = json.load(file)

# Upload FAQ documents
batch = {
    "value": [
        {**doc, "@search.action": "upload"}
        for doc in docs
    ]
}

r = requests.post(
    f"{base}/indexes/faq/docs/index{api}",
    headers=headers,
    json=batch,
    timeout=30
)

print("Upload FAQ:", r.status_code)
r.raise_for_status()

print("Done:", len(docs), "questions are now in the index")






















# import json, requests

# endpoint  = "https://hama-search.search.windows.net"     # e.g. https://rajasearch.search.windows.net
# admin_key = "6jqQLhrdDEnXZUpQhKxPq4egV8eWHJeMoX08nHa45mAzSeAVtxZE"           # Settings > Keys > Primary admin key
# api = "?api-version=2024-07-01"
# headers = {"api-key": admin_key, "Content-Type": "application/json"}
# base = endpoint.rstrip("/")

# index = {
#     "name": "faq",
#     "fields": [
#         {"name": "id",       "type": "Edm.String", "key": True},
#         {"name": "question", "type": "Edm.String", "searchable": True},
#         {"name": "answer",   "type": "Edm.String", "searchable": True},
#         {"name": "category", "type": "Edm.String", "filterable": True, "facetable": True},
#     ],
# }
# r = requests.put(f"{base}/indexes/faq{api}", headers=headers, json=index, timeout=30)
# print("Create index:", r.status_code)
# r.raise_for_status()

# docs = json.load(open(r"C:\Users\shubi\Desktop\AI & ML\week8-boot\week08-class2-bot file>\faq.json", encoding="utf-8"))
# batch = {"value": [dict(d, **{"@search.action": "upload"}) for d in docs]}
# r = requests.post(f"{base}/indexes/faq/docs/index{api}", headers=headers, json=batch, timeout=30)
# print("Upload FAQ:", r.status_code)
# r.raise_for_status()
# print("Done:", len(docs), "questions are now in the index")
