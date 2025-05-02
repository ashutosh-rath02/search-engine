import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.search.semantic_search import SemanticSearch
from src.indexing.inverted_index import InvertedIndex
from src.indexing.tokenizer import Tokenizer

def main():
    # Create a tokenizer and index
    tokenizer = Tokenizer(remove_stopwords=True)
    index = InvertedIndex(tokenizer=tokenizer)
    
    # Create a semantic search engine
    search = SemanticSearch(index=index)
    
    # Add some sample documents
    documents = [
        "The quick brown fox jumps over the lazy dog.",
        "Deep learning is a subset of machine learning with neural networks.",
        "Paris is the capital of France and known for the Eiffel Tower.",
        "Machine learning algorithms learn patterns from data to make predictions.",
        "Climate change is causing rising sea levels and extreme weather events.",
        "Renewable energy sources include solar, wind, and hydroelectric power.",
        "Natural language processing helps computers understand human language.",
        "The Louvre Museum in Paris houses the Mona Lisa painting."
    ]
    
    # Add documents to the index and generate embeddings
    for i, doc in enumerate(documents):
        search.add_document(i, doc)
    
    # Perform semantic searches
    print("Semantic search for 'artificial intelligence':")
    results = search.search("artificial intelligence")
    display_results(results)
    
    print("\nSemantic search for 'global warming':")
    results = search.search("global warming")
    display_results(results)
    
    print("\nSemantic search for 'tourism in Europe':")
    results = search.search("tourism in Europe")
    display_results(results)
    
    print("\nSemantic search for 'animals in nature':")
    results = search.search("animals in nature")
    display_results(results)

def display_results(results):
    if not results:
        print("  No results found.")
    else:
        for i, (doc_id, content, score) in enumerate(results, 1):
            print(f"  {i}. [Doc #{doc_id}, Score: {score:.4f}] {content}")

if __name__ == "__main__":
    main()