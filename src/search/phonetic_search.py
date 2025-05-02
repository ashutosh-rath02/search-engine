import phonetics
from collections import defaultdict
from ..indexing.inverted_index import InvertedIndex

class PhoneticSearch:
   
    
    def __init__(self, index=None, algorithm="metaphone"):
        self.index = index or InvertedIndex()
        self.algorithm = algorithm
        
        self.phonetic_index = defaultdict(set)
        
        self.doc_phonetic_index = defaultdict(set)
        
        self._build_phonetic_indices()
    
    def _build_phonetic_indices(self):
        for term, doc_ids in self.index.index.items():
            phonetic_code = self._get_phonetic_code(term)
            if phonetic_code:
                self.phonetic_index[phonetic_code].add(term)
                
                self.doc_phonetic_index[phonetic_code].update(doc_ids)
    
    def _get_phonetic_code(self, word):
        try:
            if self.algorithm == "metaphone":
                return phonetics.metaphone(word)
            elif self.algorithm == "soundex":
                return phonetics.soundex(word)
            elif self.algorithm == "double_metaphone":
                return phonetics.dmetaphone(word)[0]
            else:
                # Default to Metaphone
                return phonetics.metaphone(word)
        except:
            return None
    
    def search(self, query, limit=10):
        if self.index.use_lemmatization:
            query_terms = self.index.tokenizer.lemmatize(query)
        else:
            query_terms = self.index.tokenizer.tokenize(query)
        
        if not query_terms:
            return []
        
        matches = {}  # doc_id -> score
        
        for term in query_terms:
            phonetic_code = self._get_phonetic_code(term)
            if not phonetic_code:
                continue
            
            doc_ids = self.doc_phonetic_index.get(phonetic_code, set())
            
            for doc_id in doc_ids:
                if doc_id in matches:
                    matches[doc_id] += 1.0
                else:
                    matches[doc_id] = 1.0
        
        results = []
        for doc_id, score in matches.items():
            document = self.index.get_document(doc_id)
            results.append((doc_id, document, score))
        
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:limit]
    
    def get_phonetic_matches(self, term):
        phonetic_code = self._get_phonetic_code(term)
        if not phonetic_code:
            return set()
        
        return self.phonetic_index.get(phonetic_code, set())