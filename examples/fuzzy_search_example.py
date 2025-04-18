import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.search.fuzzy_search import FuzzySearch
from src.indexing.inverted_index import InvertedIndex
from src.indexing.tokenizer import Tokenizer

def main():
    tokenizer = Tokenizer(remove_stopwords=True)
    index = InvertedIndex(tokenizer=tokenizer, use_lemmatization=True)
    
    search = FuzzySearch(index=index, max_distance=2)
    
    # Add some sample documents
    documents = [
        "The quick brown fox jumps over the lazy dog.",
        "Python is a popular programming language for data science.",
        "Search engines use inverted indices for efficient lookups.",
        "Machine learning algorithms learn patterns from data.",
        "Information retrieval systems help find relevant documents.",
        "Python can be used to build powerful search engines and indexing systems."
    ]
    
    for i in range(1000):
        documents.append(f"Document {i} with some random text for testing performance")
    
    print("Indexing documents...")
    for i, doc in enumerate(documents):
        search.index.add_document(i, doc)
    
    queries = [
        "pithon",
        "serch engien",
        "machin lerning",
        "informaton retreival"
    ]
    
    print("\nPerforming searches and comparing performance...")
    for query in queries:
        print(f"\nFuzzy search for '{query}':")
        results = search.search(query)
        display_results(results)
        
        # Get timing statistics
        stats = search.get_average_times()
        print("\nPerformance comparison:")
        print(f"  Linear Search Time: {stats['linear_search_avg']:.6f} seconds")
        print(f"  BK-tree Search Time: {stats['bktree_search_avg']:.6f} seconds")
        print(f"  Speedup factor: {stats['speedup']:.2f}x")

def display_results(results):
    if not results:
        print("  No results found.")
    else:
        for i, (doc_id, content, score) in enumerate(results[:3], 1):  # Show top 3 results
            print(f"  {i}. [Score: {score:.4f}] {content[:100]}...")

if __name__ == "__main__":
    main()