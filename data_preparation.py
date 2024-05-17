import pandas as pd
from transformers import BertTokenizer, BertModel
import torch

# Load the dataset
data = pd.read_csv('arxiv_papers.csv')

# Initialize BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

# Process and save embeddings
data['embeddings'] = data['abstract'].apply(get_embeddings)
data.to_pickle('processed_arxiv_papers.pkl')
