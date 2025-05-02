# examples/combined_search_example.py

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.search.combined_search import CombinedSearch
from src.indexing.inverted_index import InvertedIndex
from src.indexing.tokenizer import Tokenizer

def main():
    # Create a tokenizer and index
    tokenizer = Tokenizer(remove_stopwords=True)
    index = InvertedIndex(tokenizer=tokenizer)
    
    # Create a combined search engine
    search = CombinedSearch(index=index)
    
    # Add some sample documents
    documents = [
        "The quick brown fox jumps over the lazy dog.",
        "Deep learning is a subset of machine learning with neural networks.",
        "Paris is the capital of France and known for the Eiffel Tower.",
        "Machine learning algorithms learn patterns from data to make predictions.",
        "Climate change is causing rising sea levels and extreme weather events.",
        "Python is a popular programming language for data science and ML.",
        "Natural language processing helps computers understand human language.",
        "The Louvre Museum in Paris houses the Mona Lisa painting.",
        "Phone numbers can be stored in the phonebook or directory.",
        "Please send me an email or fone me when you arrive."
    ]
    
    # Add documents to all search engines
    for i, doc in enumerate(documents):
        search.add_document(i, doc)
    
    # Perform searches with different modes
    queries = [
        "machine learning",   # Basic search
        "machin lerning",    # Fuzzy match
        "fone directory",    # Phonetic match
        "artificial intelligence"  # Semantic match
    ]
    
    modes = ["basic", "fuzzy", "phonetic", "semantic", "combined"]
    
    for query in queries:
        print(f"\n=== Search for '{query}' ===\n")
        
        for mode in modes:
            print(f"-- {mode.capitalize()} Search Results:")
            results = search.search(query, mode=mode)
            display_results(results)
            print()

def display_results(results):
    if not results:
        print("  No results found.")
    else:
        for i, (doc_id, content, score, technique) in enumerate(results, 1):
            print(f"  {i}. [Doc #{doc_id}, Score: {score:.4f}, Technique: {technique}] {content}")

if __name__ == "__main__":
    main()