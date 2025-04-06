from collections import defaultdict
from .tokenizer import Tokenizer

class InvertedIndex:
    """
    Implementation of an inverted index, which maps terms to the documents 
    that contain them.
    """
    
    def __init__(self, tokenizer=None):
        """
        Initialize the inverted index.
        
        Args:
            tokenizer: The tokenizer to use for processing text
        """
        # Term -> set of doc_ids
        self.index = defaultdict(set)  
        # Document ID -> original document content
        self.documents = {} 
        self.tokenizer = tokenizer or Tokenizer()
    
    def add_document(self, doc_id, content):
        """
        Add a document to the index.
        
        Args:
            doc_id: A unique identifier for the document
            content: The document's text content
        """
        self.documents[doc_id] = content
        
        tokens = self.tokenizer.tokenize(content)
        
        for token in tokens:
            self.index[token].add(doc_id)
    
    def lookup(self, term):
        """
        Look up a term in the index.
        
        Args:
            term: The term to look up
            
        Returns:
            A set of document IDs that contain the term
        """
        processed_terms = self.tokenizer.tokenize(term)
        if not processed_terms:
            return set()
        
        return self.index.get(processed_terms[0], set())
    
    def get_document(self, doc_id):
        """
        Retrieve a document by its ID.
        
        Args:
            doc_id: The document ID
            
        Returns:
            The document content, or None if not found
        """
        return self.documents.get(doc_id)