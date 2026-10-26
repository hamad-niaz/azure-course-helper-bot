# # Step 3: the chatbot website.  Run:  streamlit run chatbot.py

import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT", "").rstrip("/")
SEARCH_KEY = os.getenv("SEARCH_KEY", "")

TRANSLATOR_KEY = os.getenv("TRANSLATOR_KEY", "")
TRANSLATOR_REGION = os.getenv("TRANSLATOR_REGION", "eastus")

MIN_SCORE = 1.0

st.set_page_config(
    page_title="Course Helper Bot",
    page_icon="🤖"
)

st.title("🤖 Course Helper Bot")
st.caption("Ask questions about Azure and this course.")

if not SEARCH_ENDPOINT or not SEARCH_KEY:
    st.error("SEARCH_ENDPOINT or SEARCH_KEY is missing in .env")
    st.stop()

urdu = st.toggle(
    "Answer in Urdu",
    value=False,
    disabled=not TRANSLATOR_KEY
)


def search(question):
    url = (
        f"{SEARCH_ENDPOINT}/indexes/faq/docs/search"
        "?api-version=2024-07-01"
    )

    headers = {
        "api-key": SEARCH_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "search": question,
        "top": 1,
        "select": "question,answer"
    }

    response = requests.post(
        url,
        headers=headers,
        json=body,
        timeout=30
    )

    response.raise_for_status()

    hits = response.json().get("value", [])

    if hits and hits[0].get("@search.score", 0) >= MIN_SCORE:
        return hits[0]

    return None


def to_urdu(text):
    url = (
        "https://api.cognitive.microsofttranslator.com/"
        "translate?api-version=3.0&to=ur"
    )

    headers = {
        "Ocp-Apim-Subscription-Key": TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": TRANSLATOR_REGION,
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        headers=headers,
        json=[{"Text": text}],
        timeout=30
    )

    response.raise_for_status()

    return response.json()[0]["translations"][0]["text"]


if "chat" not in st.session_state:
    st.session_state.chat = []

for role, message in st.session_state.chat:
    with st.chat_message(role):
        st.write(message)

question = st.chat_input("Ask a question about Azure...")

if question:
    st.session_state.chat.append(("user", question))

    with st.chat_message("user"):
        st.write(question)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Searching for an answer..."):
                hit = search(question)

                if hit:
                    answer = hit["answer"]

                    if urdu:
                        answer = to_urdu(answer)

                    answer += f"\n\nMatched FAQ: {hit['question']}"
                else:
                    answer = (
                        "Sorry, I don't know that yet. "
                        "Please ask your teacher."
                    )

                st.write(answer)

        st.session_state.chat.append(("assistant", answer))

    except requests.RequestException as error:
        st.error(f"Azure request failed: {error}")






























########################
# import os
# import requests
# import streamlit as st
# from dotenv import load_dotenv

# load_dotenv()
# SEARCH_ENDPOINT = os.getenv("https://hama-search.search.windows.net", "").rstrip("/")
# SEARCH_KEY      = os.getenv("W6fkkyrzotuc2zB53w4LEYI0aKolewmyuvEOWA3VlzAzSeC3duCt")
# TRANSLATOR_KEY    = os.getenv("W6fkkyrzotuc2zB53w4LEYI0aKolewmyuvEOWA3VlzAzSeC3duCt")             # optional, for Urdu answers
# TRANSLATOR_REGION = os.getenv("TRANSLATOR_REGION", "eastus")
# MIN_SCORE = 1.0   # answers with a lower match score are treated as "I don't know"

# st.set_page_config(page_title="Course Helper Bot", page_icon="🤖")
# st.title("🤖 Course Helper Bot")
# st.caption("I answer questions about Azure and this course. I am a bot, not a person.")

# if not SEARCH_ENDPOINT or not SEARCH_KEY:
#     st.error("Missing SEARCH_ENDPOINT or SEARCH_KEY in .env")
#     st.stop()

# urdu = st.toggle("Answer in Urdu", value=False, disabled=not TRANSLATOR_KEY)

# def search(question):
#     url = SEARCH_ENDPOINT + "/indexes/faq/docs/search?api-version=2024-07-01"
#     body = {"search": question, "top": 1, "select": "question,answer"}
#     r = requests.post(url, headers={"api-key": SEARCH_KEY}, json=body, timeout=30)
#     r.raise_for_status()
#     hits = r.json()["value"]
#     return hits[0] if hits and hits[0]["@search.score"] >= MIN_SCORE else None

# def to_urdu(text):
#     url = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=ur"
#     h = {"Ocp-Apim-Subscription-Key": TRANSLATOR_KEY, "Ocp-Apim-Subscription-Region": TRANSLATOR_REGION}
#     r = requests.post(url, headers=h, json=[{"Text": text}], timeout=30)
#     r.raise_for_status()
#     return r.json()[0]["translations"][0]["text"]

# if "chat" not in st.session_state:
#     st.session_state.chat = []

# for role, text in st.session_state.chat:
#     st.chat_message(role).write(text)

# question = st.chat_input("Ask me something, e.g. What does error 401 mean?")
# if question:
#     st.chat_message("user").write(question)
#     hit = search(question)
#     if hit:
#         answer = hit["answer"]
#         if urdu:
#             answer = to_urdu(answer)
#         answer += f"\n\n_(matched FAQ: {hit['question']})_"
#     else:
#         answer = "Sorry, I don't know that yet. Please ask your teacher."
#     st.chat_message("assistant").write(answer)
#     st.session_state.chat += [("user", question), ("assistant", answer)]
