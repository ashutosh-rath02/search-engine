import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.search.basic_search import BasicSearch

def main():
    search = BasicSearch()
    
    documents = [
        "The quick brown fox jumps over the lazy dog.",
        "Python is a popular programming language for data science and machine learning.",
        "Search engines use inverted indices and TF-IDF for efficient and relevant lookups.",
        "Machine learning algorithms learn patterns from data to make predictions.",
        "Information retrieval systems help find relevant documents using various techniques.",
        "Python can be used to build powerful search engines, machine learning models, and indexing systems."
    ]
    
    for i, doc in enumerate(documents):
        search.index.add_document(i, doc)
    
    print("Search for 'python' (ranked):")
    results = search.search("python", rank=True)
    display_results(results)
    
    print("\nSearch for 'machine learning' (ranked):")
    results = search.search("machine learning", rank=True)
    display_results(results)
    
    print("\nSearch for 'search engine' (ranked):")
    results = search.search("search engine", rank=True)
    display_results(results)

def display_results(results):
    if not results:
        print("  No results found.")
    else:
        for i, (doc_id, content, score) in enumerate(results, 1):
            print(f"  {i}. [Doc #{doc_id}, Score: {score:.4f}] {content}")

if __name__ == "__main__":
    main()