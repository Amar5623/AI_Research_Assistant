from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
import torch

# Load pre-trained models
tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large')
model = TFAutoModelForSeq2SeqLM.from_pretrained('facebook/bart-large')

# Connect to MongoDB
client = MongoClient('mongodb+srv://amar05:Amar5623@cluster0.arfln2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['research_assistant']
collection = db['papers']

def get_embeddings(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

def retrieve_documents(query):
    query_embedding = get_embeddings(query)
    documents = list(collection.find())
    embeddings = np.array([doc['embeddings'] for doc in documents])
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    top_indices = np.argsort(similarities)[-5:][::-1]
    return [documents[i] for i in top_indices]

def generate_summary(papers):
    texts = " ".join([paper['abstract'] for paper in papers])
    inputs = tokenizer.encode("summarize: " + texts, return_tensors="tf", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def get_summary(query):
    papers = retrieve_documents(query)
    summary = generate_summary(papers)
    return summary
