# Step 2: ask one question (no website yet)
import requests

endpoint = "https://hama-search.search.windows.net"
key      = "XqybtXLcyZ4gWFPYN5Ped1dXINbSLc9oMyQ9gcNqqoAzSeAk1FVG"
question = "my key leaked, what do I do?"

url = endpoint.rstrip("/") + "/indexes/faq/docs/search?api-version=2024-07-01"
body = {"search": question, "top": 3, "select": "question,answer,category"}
r = requests.post(url, headers={"api-key": key}, json=body, timeout=30)
r.raise_for_status()
for hit in r.json()["value"]:
    print(round(hit["@search.score"], 2), "|", hit["question"])
    print("   ->", hit["answer"])
