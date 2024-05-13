import pickle
import json 

class Chunk:

    def __init__(self, id, text):
        self.id = id
        self.embeddings = None
        self.list_of_events = []
        self.text = text 
    
    
   
def load_chunks(file):
    with open("resources/" + file, "rb") as f:
        chunks = pickle.load(f)
        return chunks
    
load_chunks("الجزيرة.pkl")
            