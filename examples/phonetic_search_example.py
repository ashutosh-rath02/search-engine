# examples/phonetic_search_example.py

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.search.phonetic_search import PhoneticSearch
from src.indexing.inverted_index import InvertedIndex
from src.indexing.tokenizer import Tokenizer

def main():
    # Create a tokenizer and index
    tokenizer = Tokenizer(remove_stopwords=True)
    index = InvertedIndex(tokenizer=tokenizer, use_lemmatization=True)
    
    # Create a phonetic search engine with Metaphone algorithm
    search = PhoneticSearch(index=index, algorithm="metaphone")
    
    # Add some sample documents
    documents = [
        "The phone number is in the directory.",
        "Please fone me when you get home.",
        "Python is a powerful programming language.",
        "The facks machine is broken.",
        "Send a fax to the office.",
        "The knight rode through the night.",
        "The site has a beautiful view.",
        "I can see the sight from here.",
        "The weather effects were amazing.",
        "The special effects in the movie were impressive."
    ]
    
    # Add documents to the index
    for i, doc in enumerate(documents):
        search.index.add_document(i, doc)
    
    # Rebuild phonetic indices after adding documents
    search._build_phonetic_indices()
    
    # Perform phonetic searches
    print("Phonetic search for 'fone' (should match 'phone'):")
    results = search.search("fone")
    display_results(results)
    
    print("\nPhonetic search for 'nite' (should match 'night'):")
    results = search.search("nite")
    display_results(results)
    
    print("\nPhonetic search for 'fax' (should match 'facks'):")
    results = search.search("fax")
    display_results(results)
    
    print("\nPhonetic search for 'site' (should match 'sight'):")
    results = search.search("site")
    display_results(results)
    
    print("\nPhonetic search for 'effects' (should match 'effects'):")
    results = search.search("effects")
    display_results(results)
    
    # Display phonetic matches for some terms
    print("\nPhonetically similar terms for 'phone':")
    matches = search.get_phonetic_matches("phone")
    print(f"  {', '.join(matches)}")
    
    print("\nPhonetically similar terms for 'night':")
    matches = search.get_phonetic_matches("night")
    print(f"  {', '.join(matches)}")

def display_results(results):
    if not results:
        print("  No results found.")
    else:
        for i, (doc_id, content, score) in enumerate(results, 1):
            print(f"  {i}. [Doc #{doc_id}, Score: {score:.4f}] {content}")

if __name__ == "__main__":
    main()