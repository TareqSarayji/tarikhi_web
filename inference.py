from fastapi import FastAPI, Query
from typing import List
import torch
import pickle
import os
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel

app = FastAPI()
os.environ['KMP_DUPLICATE_LIB_OK']='True'

class Chunk:

    def __init__(self, id, text):
        self.id = id
        self.embeddings = None
        self.list_of_events = []
        self.text = text 


tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-large')
model = AutoModel.from_pretrained('intfloat/multilingual-e5-large')

def get_embeddings_list(chunk_l):
    emb_l = []
    for i in chunk_l:
        emb_l.append(i.embeddings)
    
    return emb_l

def load_chunks(file):
    with open("resources/" + file, "rb") as f:
        chunks = pickle.load(f)
        return chunks
    
def get_chunks():
    files = {}
    for file in os.listdir("resources"):
        chunks = load_chunks(file)
        files[file] = chunks

    return chunks

@app.get('/Tarikhi')
async def tarikhi(query: str = Query(..., description="Your query string")):
    chunks = get_chunks()
    print(len(chunks))

    batch_dict = tokenizer(query, max_length=512, padding=True, truncation=True, return_tensors='pt')

    outputs = model(**batch_dict)

    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    print(embeddings)

    d = 1024

    index = faiss.IndexFlatL2(d)
    print("test-1")

    index.add(np.vstack(get_embeddings_list(chunks)))
    print("test-2")
    D, I = index.search(embeddings, 20)
    print("test-3")
    
    top_k_chunks = [(chunks[i], D[0][j]) for j, i in enumerate(I[0])]
    
    events = []
    for chunk in top_k_chunks:
        for event in chunk[0].list_of_events:
            events.append(event['event'])
    
    return {"events": events}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
