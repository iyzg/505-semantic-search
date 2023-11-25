from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI

import gzip
import jsonlines
import os
import numpy as np

EMBEDDING_MODEL = "text-embedding-ada-002"
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
EMBED_FILE = os.path.join(SERVER_DIR, "msg-embeddings.jsonl.gz")

class MessageSearchApp:
    def __init__(self):
        self._messages = None
        self._embeddings = None
        self._client = OpenAI()

    @property
    def messages(self):
        if self._messages is None:
            self._load_msg_embeddings()
        return self._messages

    @property
    def embeddings(self):
        if self._embeddings is None:
            self._load_msg_embeddings()
        return self._embeddings

    def _load_msg_embeddings(self):
        if self._messages is not None and self._embeddings is not None:
            return

        with gzip.GzipFile(fileobj=open(EMBED_FILE, "rb"), mode="rb") as fin:
            message_info = list(jsonlines.Reader(fin))

        print("Lazy loading embedding info...")
        self._messages = [x["message"] for x in message_info]
        self._embeddings = [x["embed"] for x in message_info]
        assert self._messages is not None and self._embeddings is not None

    def get_openai_embedding(self, text: str) -> list[float]:
        result = self._client.embeddings.create(input=text, model=EMBEDDING_MODEL)
        return result.data[0].embedding
    
    # TODO: Understand why this works exactly
    def get_top_relevant_messages(self, query: str, k: int = 20) -> list[dict]:
        query_embed = self.get_openai_embedding(query)
        dotprod = np.matmul(self.embeddings, np.array(query_embed).T)
        m_dotprod = np.median(dotprod)
        ind = np.argpartition(dotprod, -k)[-k:]
        ind = ind[np.argsort(dotprod[ind])][::-1]
        result = [
            {
                "message": self.messages[i].capitalize(),
                "score": (dotprod[i] - m_dotprod) * 100,
            }
            for i in ind
        ]
        return result
    

app = Flask(__name__)
msg_search_app = MessageSearchApp()
CORS(app, support_credentials=True)

@app.route("/search", methods=["POST"])
def search():
    error = None
    result = []

    query = request.get_json().get("query")
    try:
        result = msg_search_app.get_top_relevant_messages(query=query, k=20)
    except Exception as err:
        error = str(err)
    return jsonify(error=error, result=result)

@app.route("/")
def index():
    return 'Hello World!'

app.run()
