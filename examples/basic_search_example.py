import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.search.basic_search import BasicSearch
from src.indexing.inverted_index import InvertedIndex

def main():
    index = InvertedIndex()
    
    search = BasicSearch(index)
    
    documents = [
        "The quick brown fox jumps over the lazy dog.",
        "Python is a popular programming language for data science.",
        "Search engines use inverted indices for efficient lookups.",
        "Machine learning algorithms learn patterns from data.",
        "Information retrieval systems help find relevant documents.",
        "Python can be used to build powerful search engines and indexing systems."
    ]
    
    for i, doc in enumerate(documents):
        search.index.add_document(i, doc)
    
    print("AND Search for 'python language':")
    results = search.search("python language", mode="AND")
    display_results(results)
    
    print("\nOR Search for 'python language':")
    results = search.search("python language", mode="OR")
    display_results(results)
    
    print("\nSearch for 'search engines':")
    results = search.search("search engines")
    display_results(results)
    
    print("\nSearch for 'machine learning':")
    results = search.search("machine learning")
    display_results(results)

def display_results(results):
    if not results:
        print("No results found.")
    else:
        for i, (doc_id, content) in enumerate(results, 1):
            print(f"  {i}. [Doc #{doc_id}] {content}")

if __name__ == "__main__":
    main()