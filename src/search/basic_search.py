from ..indexing.inverted_index import InvertedIndex

class BasicSearch:
    """Provides basic search functionality using an inverted index
    """
    
    def __init__(self, index):
        """
        Initialize the BasicSearch with an inverted index.
        
        Args:
            index: An instance of InvertedIndex
        """
        self.index = index or InvertedIndex()
        
    
    def search(self, query, mode="AND"):        
        """
        Search for documents that match the query.
        
        query (str): The search query containing terms to look for
        mode (str): The search mode - "AND" requires all terms to match,
                        "OR" requires any term to match
            
        Returns:
            list: A list of document IDs that match the query
        """
        tokens = self.index.tokenizer.tokenize(query)
        
        if not tokens:
            return []
        
        result_docs = self.index.lookup(tokens[0])
        
        for token in tokens[1:]:
            docs = self.index.lookup(token)
            if mode == "AND":
                result_docs = result_docs.intersection(docs)
            else: # OR mode
                result_docs = result_docs.union(docs)
            
            if mode == "AND" and not result_docs:
                break
        
        # Return the matching documents
        return [(doc_id, self.index.get_document(doc_id)) 
                for doc_id in result_docs]