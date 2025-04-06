from ..indexing.inverted_index import InvertedIndex
from ..ranking.tf_idf import TFIDFRanker

class BasicSearch:
    """
    Provides basic keyword search functionality using an inverted index.
    """
    
    def __init__(self, index=None):
        """
        Initialize the search engine.
        
        Args:
            index: An existing inverted index, or None to create a new one
        """
        self.index = index or InvertedIndex()
        self.ranker = None
    
    def search(self, query, mode="AND", rank=True):
        """
        Search for documents matching the query.
        
        Args:
            query (str): The search query
            mode (str): The search mode - "AND" requires all terms to match,
                        "OR" requires any term to match
            rank (bool): Whether to rank results by relevance
        
        Returns:
            list: A list of (doc_id, document, score) tuples for matching documents
        """
        if self.index.use_lemmatization:
            tokens = self.index.tokenizer.lemmatize(query)
        else:
            tokens = self.index.tokenizer.tokenize(query)
        
        if not tokens:
            return []
        
        result_docs = self.index.lookup(tokens[0])
        
        for token in tokens[1:]:
            docs = self.index.lookup(token)
            if mode == "AND":
                result_docs = result_docs.intersection(docs)
            else:  # "OR" mode
                result_docs = result_docs.union(docs)
            
            if mode == "AND" and not result_docs:
                break
        
        results = []
        for doc_id in result_docs:
            document = self.index.get_document(doc_id)
            
            if rank:
                if self.ranker is None:
                    self.ranker = TFIDFRanker(self.index)
                
                # Get the document's score
                score = self.ranker.score(query, doc_id)
                results.append((doc_id, document, score))
            else:
                results.append((doc_id, document, 1.0))
        
        # Sort by score if ranking is enabled
        if rank:
            results.sort(key=lambda x: x[2], reverse=True)
        
        return results