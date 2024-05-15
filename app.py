from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
import inference
from functions import get_file_names
from transformers import AutoTokenizer, AutoModel
import faiss
import numpy as np
import pickle
import os
from transformers import pipeline
# from transformers import MarianTokenizer, MarianMTModel

# mname = "marefa-nlp/marefa-mt-en-ar"
# translation_tokenizer = MarianTokenizer.from_pretrained(mname)
# translation_model = MarianMTModel.from_pretrained(mname)

# def translate(text):
#     translated_text = [""]
#     try:
#         translated_tokens = translation_model.generate(**translation_tokenizer.prepare_seq2seq_batch([input], return_tensors="pt"))
#         translated_text = [translation_tokenizer.decode(t, skip_special_tokens=True) for t in translated_tokens]
#     except:
#         pass
#     return " ".join(translated_text)
 

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ar")



app = Flask(__name__)

events = []

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




@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('Login_Signup'))

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/New_Registration_guest')
def New_Registration_guest():
    return render_template('New_Registration_guest.html')

@app.route('/Login_Signup')
def Login_Signup():
    return render_template('Login-Signup.html')

@app.route('/New_Registration')
def New_Registration():
    return render_template('New_Registration.html')

@app.route('/Main_Webpage')
def Main_Webpage():
    return render_template('Main Webpage.html', resources=get_file_names("resources"), events=events)

@app.route('/contributeresource')
def contributeresource():
    image_url = "https://simpleicon.com/wp-content/uploads/cloud-upload-1.svg"
    response = inference.get(image_url)

    return render_template('contributeresource.html', image_data=response.content)

@app.route('/login.php', methods=['GET', 'POST'])
def login_php():
    return redirect(url_for('Main_Webpage'))

@app.route('/final', methods=['GET', 'POST'])
def final():
    return render_template('final.html')

@app.route('/Tarikhi', methods=['GET', 'POST'])
def tarikhi():
    query = request.args.get('query')


    chunks = get_chunks()


    batch_dict = tokenizer(query, max_length=512, padding=True, truncation=True, return_tensors='pt')

    outputs = model(**batch_dict)

    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()

    d = 1024

    index = faiss.IndexFlatL2(d)

    index.add(np.vstack(get_embeddings_list(chunks)))

    D, I = index.search(embeddings, 20)

    top_k_chunks = [(chunks[i], D[0][j]) for j, i in enumerate(I[0])]
    
    events = []
    for chunk in top_k_chunks:
        for event in chunk[0].list_of_events:
            events.append(event)
    
    return jsonify(events)

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    text = request.args.get('text')
    translated_text = pipe(">>ara<<"+text)[0]['translation_text']
    return jsonify(translated_text)

if __name__ == "__main__":
    app.run(debug=True)














    