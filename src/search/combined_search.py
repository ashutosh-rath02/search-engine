from ..indexing.inverted_index import InvertedIndex
from ..search.basic_search import BasicSearch
from ..search.fuzzy_search import FuzzySearch
from ..search.phonetic_search import PhoneticSearch
from ..search.semantic_search import SemanticSearch

class CombinedSearch:

    def __init__(self, index=None):
        self.index = index or InvertedIndex()
        
        self.basic_search = BasicSearch(index=self.index)
        self.fuzzy_search = FuzzySearch(index=self.index)
        self.phonetic_search = PhoneticSearch(index=self.index)
        self.semantic_search = SemanticSearch(index=self.index)
    
    def add_document(self, doc_id, content):
        self.semantic_search.add_document(doc_id, content)
        
        self.phonetic_search._build_phonetic_indices()
    
    def search(self, query, mode="combined", limit=10):
        results = []
        
        if mode == "basic" or mode == "combined":
            basic_results = self.basic_search.search(query, rank=True)
            for doc_id, content, score in basic_results:
                results.append((doc_id, content, score, "basic"))
        
        if mode == "fuzzy" or mode == "combined":
            fuzzy_results = self.fuzzy_search.search(query, limit=limit)
            for doc_id, content, score in fuzzy_results:
                results.append((doc_id, content, score * 0.8, "fuzzy")) 
        
        if mode == "phonetic" or mode == "combined":
            phonetic_results = self.phonetic_search.search(query, limit=limit)
            for doc_id, content, score in phonetic_results:
                results.append((doc_id, content, score * 0.8, "phonetic")) 
        
        if mode == "semantic" or mode == "combined":
            semantic_results = self.semantic_search.search(query, top_k=limit)
            for doc_id, content, score in semantic_results:
                results.append((doc_id, content, score * 0.9, "semantic")) 
        unique_results = {}
        for doc_id, content, score, technique in results:
            if doc_id not in unique_results or score > unique_results[doc_id][1]:
                unique_results[doc_id] = (content, score, technique)
        
        final_results = [(doc_id, content, score, technique) 
                         for doc_id, (content, score, technique) in unique_results.items()]
        final_results.sort(key=lambda x: x[2], reverse=True)
        
        return final_results[:limit]