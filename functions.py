import os
import pickle
import faiss





def get_file_names(path):
    files =[]
    for file in os.listdir(path):
        files.append(file)
    edited = []
    for file in files:
        edited.append(file.rsplit('.', 1)[0])
    
    return edited


