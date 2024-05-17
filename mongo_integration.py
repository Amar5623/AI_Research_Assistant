import pandas as pd
from pymongo import MongoClient

# Load the CSV file into a DataFrame
df = pd.read_csv('arxiv_papers.csv')

# Connect to MongoDB
client = MongoClient('mongodb+srv://amar05:Amar5623@cluster0.arfln2l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.research_assistant
collection = db.papers

# Insert data into MongoDB
for index, row in df.iterrows():
    document = {
        'id': row['id'],
        'title': row['title'],
        'abstract': row['abstract']
        # Add 'full_text' if it's in your CSV
        # 'full_text': row['full_text']
    }
    collection.insert_one(document)

print("Data inserted successfully")
