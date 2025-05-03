from flask import Flask, render_template, request, jsonify
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.search.combined_search import CombinedSearch
from src.indexing.inverted_index import InvertedIndex
from src.indexing.tokenizer import Tokenizer

app = Flask(__name__)

sample_documents = [
    "The quick brown fox jumps over the lazy dog.",
    "Deep learning is a subset of machine learning with neural networks.",
    "Paris is the capital of France and known for the Eiffel Tower.",
    "Machine learning algorithms learn patterns from data to make predictions.",
    "Climate change is causing rising sea levels and extreme weather events.",
    "Python is a popular programming language for data science and ML.",
    "Natural language processing helps computers understand human language.",
    "The Louvre Museum in Paris houses the Mona Lisa painting.",
    "Phone numbers can be stored in the phonebook or directory.",
    "Please send me an email or fone me when you arrive.",
    "Artificial intelligence aims to create systems that can think like humans.",
    "The Internet of Things connects everyday devices to the internet.",
    "Cloud computing provides computing services over the internet.",
    "Big data involves analyzing extremely large data sets.",
    "Virtual reality creates an immersive simulated environment.",
    "Croissant is made from a flaky pastry dough.",
    "The Eiffel Tower is a famous landmark in Paris.",
    "Prashant has been working pretty hard."
]

def initialize_search_engine():
    print("Initializing search engine...")
    tokenizer = Tokenizer(remove_stopwords=True)
    index = InvertedIndex(tokenizer=tokenizer)
    search = CombinedSearch(index=index)
    
    for i, doc in enumerate(sample_documents):
        search.add_document(i, doc)
    
    print("Search engine initialized with sample documents.")
    return search

search_engine = initialize_search_engine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '')
    mode = data.get('mode', 'combined')
    
    if not query:
        return jsonify({'results': []})
    
    start_time = time.time()
    
    results = search_engine.search(query, mode=mode, limit=10)
    
    search_time = time.time() - start_time
    
    formatted_results = []
    for doc_id, content, score, technique in results:
        formatted_results.append({
            'doc_id': doc_id,
            'content': content,
            'score': round(score, 4),
            'technique': technique
        })
    
    return jsonify({
        'results': formatted_results,
        'query': query,
        'mode': mode,
        'search_time': round(search_time * 1000, 2)  # Convert to milliseconds
    })
    
@app.route('/process', methods=['POST'])
def process():
    """Return detailed information about how each search technique processes a query"""
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'processes': []})
    
    processes = []
    
    if search_engine.index.use_lemmatization:
        basic_tokens = search_engine.index.tokenizer.lemmatize(query)
    else:
        basic_tokens = search_engine.index.tokenizer.tokenize(query)
    
    basic_process = {
        'technique': 'basic',
        'steps': [
            {'name': 'Tokenization', 'description': f"Query '{query}' tokenized to {basic_tokens}"},
            {'name': 'Lookup', 'description': f"Looking up documents containing these terms"}
        ]
    }
    
    matching_docs = []
    for token in basic_tokens:
        docs = search_engine.index.lookup(token)
        matching_docs.extend(list(docs))
    
    if matching_docs:
        basic_process['steps'].append({
            'name': 'Matching', 
            'description': f"Found {len(set(matching_docs))} documents containing query terms"
        })
    
    processes.append(basic_process)
    
    fuzzy_process = {
        'technique': 'fuzzy',
        'steps': [
            {'name': 'Tokenization', 'description': f"Query '{query}' tokenized to {basic_tokens}"},
            {'name': 'Edit Distance', 'description': f"Computing edit distances for each token"}
        ]
    }
    
    fuzzy_matches = []
    all_terms = set(search_engine.index.index.keys())
    for token in basic_tokens:
        for term in all_terms:
            distance = search_engine.fuzzy_search._levenshtein_distance(token, term)
            if 0 < distance <= 2: 
                fuzzy_matches.append((term, distance))
                if len(fuzzy_matches) >= 3:  
                    break
    
    if fuzzy_matches:
        examples = ", ".join([f"'{term}' (distance {dist})" for term, dist in fuzzy_matches])
        fuzzy_process['steps'].append({
            'name': 'Fuzzy Matches', 
            'description': f"Found similar terms: {examples}"
        })
    
    processes.append(fuzzy_process)
    
    phonetic_process = {
        'technique': 'phonetic',
        'steps': [
            {'name': 'Tokenization', 'description': f"Query '{query}' tokenized to {basic_tokens}"},
            {'name': 'Phonetic Encoding', 'description': f"Converting tokens to phonetic codes"}
        ]
    }
    
    phonetic_codes = []
    for token in basic_tokens:
        code = search_engine.phonetic_search._get_phonetic_code(token)
        if code:
            phonetic_codes.append((token, code))
    
    if phonetic_codes:
        examples = ", ".join([f"'{token}' → '{code}'" for token, code in phonetic_codes])
        phonetic_process['steps'].append({
            'name': 'Phonetic Codes', 
            'description': f"Generated phonetic codes: {examples}"
        })
        
        phonetic_matches = []
        for token, code in phonetic_codes:
            similar_terms = search_engine.phonetic_search.get_phonetic_matches(token)
            phonetic_matches.extend(list(similar_terms)[:2])  
        
        if phonetic_matches:
            phonetic_process['steps'].append({
                'name': 'Phonetic Matches', 
                'description': f"Found phonetically similar terms: {phonetic_matches}"
            })
    
    processes.append(phonetic_process)
    
    semantic_process = {
        'technique': 'semantic',
        'steps': [
            {'name': 'Query Embedding', 'description': f"Converting query '{query}' to a vector embedding"},
            {'name': 'Similarity Calculation', 'description': f"Computing cosine similarity with document embeddings"}
        ]
    }
    
    semantic_process['steps'].append({
        'name': 'Vector Space', 
        'description': f"Comparing in a high-dimensional vector space"
    })
    
    processes.append(semantic_process)
    
    return jsonify({'processes': processes})

if __name__ == '__main__':
    app.run(debug=True)