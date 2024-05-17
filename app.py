from flask import Flask, request, jsonify
from rag_model import get_summary

app = Flask(__name__)

@app.route('/summary', methods=['POST'])
def summary():
    query = request.json.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    summary = get_summary(query)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)