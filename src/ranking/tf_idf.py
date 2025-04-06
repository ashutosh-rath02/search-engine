import math
from collections import defaultdict, Counter

class TFIDFRanker:
    """
    Implements TF-IDF (Term Frequency-Inverse Document Frequency) ranking.
    """
    
    def __init__(self, index):
        """
        Initialize the TF-IDF ranker.

        Args:
            index : The inverted index to use for document retrieval.
        """
        self.index = index
        self.tf = {} # doc_id -> term -> frequency
        self.idf = {} # term -> inverse document frequency
        self.doc_lengths = {} # doc_id -> length of the document
        
        self._build_tf_idf()
        
    def _build_tf_idf(self):
        """
        Calculate TF and IDF values for all terms and documents
        """
        
        # Total number of documents
        N = len(self.index.documents)
        
        if N == 0:
            return
        
        # Calculate term frequency (TF) and document frequency (DF)
        df = defaultdict(int) # term -> document frequency
        
        for doc_id, content in self.index.documents.items():
            if self.index.use_lemmatization:
                tokens = self.index.tokenizer.lemmatize(content)
            else:
                tokens = self.index.tokenizer.tokenize(content)
           
            term_counts = Counter(tokens)
            self.tf[doc_id] = term_counts
            
            self.tf[doc_id] = {}
            for term, count in term_counts.items():
                # Calculate term frequency (TF)
                self.tf[doc_id][term] = count
                
                df[term] += 1
                
        # Calculate inverse document frequency (IDF)
        for term, doc_freq in df.items():
            # IDF = log(N / doc_freq)
            self.idf[term] = math.log(N / (doc_freq))
            
    # TF gives us information on how often a term appears in a document and IDF gives us information about the relative rarity of a term in the collection of documents. By multiplying these values together we can get our final TF-IDF value.
    
    # The higher the TF-IDF score the more important or relevant the term is; as a term gets less relevant, its TF-IDF score will approach 0.
    def score(self, query, doc_id):
        """
        Calculate the TF-IDF score for a query-document pair.
        
        Args:
            query: The search query
            doc_id: The document ID
            
        Returns:
            float: The TF-IDF score
        """
        # Process the query
        if self.index.use_lemmatization:
            query_terms = self.index.tokenizer.lemmatize(query)
        else:
            query_terms = self.index.tokenizer.tokenize(query)
        
        # No query terms or document not in index
        if not query_terms or doc_id not in self.tf:
            return 0.0
        
        score = 0.0
        
        # Calculate score for each query term
        for term in query_terms:
            if term in self.idf and term in self.tf.get(doc_id, {}):
                # TF-IDF score = TF * IDF
                tf = self.tf[doc_id][term]
                idf = self.idf[term]
                score += tf * idf
        
        # Normalize by document length to avoid bias towards longer documents
        if doc_id in self.doc_lengths and self.doc_lengths[doc_id] > 0:
            score /= self.doc_lengths[doc_id]
        
        return score
