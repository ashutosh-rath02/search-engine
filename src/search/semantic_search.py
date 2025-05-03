import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from ..indexing.inverted_index import InvertedIndex

class SemanticSearch:
    def __init__(self, index=None, model_name='all-MiniLM-L6-v2'):
        self.index = index or InvertedIndex()
        
        print(f"Loading semantic model: {model_name}")
        self.model = SentenceTransformer(model_name)
        
        self.doc_embeddings = {}  # doc_id -> embedding
        self.doc_ids = [] 
        self.embeddings_matrix = None  
        
        if self.index.documents:
            self._generate_embeddings()
    
    def _generate_embeddings(self):
        documents = []
        self.doc_ids = []
        
        for doc_id, content in self.index.documents.items():
            documents.append(content)
            self.doc_ids.append(doc_id)
        
        if documents:
            print(f"Generating embeddings for {len(documents)} documents...")
            embeddings = self.model.encode(documents, show_progress_bar=True)
            
            self.embeddings_matrix = np.array(embeddings)
            for i, doc_id in enumerate(self.doc_ids):
                self.doc_embeddings[doc_id] = embeddings[i]
                
            print(f"Embeddings generated. Shape: {self.embeddings_matrix.shape}")
    
    def add_document(self, doc_id, content):
        self.index.add_document(doc_id, content)
        
        embedding = self.model.encode(content)
        
        self.doc_embeddings[doc_id] = embedding
        
        if self.embeddings_matrix is None:
            self.embeddings_matrix = np.array([embedding])
            self.doc_ids = [doc_id]
        else:
            self.embeddings_matrix = np.vstack([self.embeddings_matrix, embedding])
            self.doc_ids.append(doc_id)
    
    def search(self, query, top_k=5):
        if not self.embeddings_matrix is not None:
            return []
        
        query_embedding = self.model.encode(query)
        
        similarity_scores = cosine_similarity(
            [query_embedding], 
            self.embeddings_matrix
        )[0]
        
        top_indices = np.argsort(similarity_scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            doc_id = self.doc_ids[idx]
            document = self.index.get_document(doc_id)
            score = similarity_scores[idx]
            results.append((doc_id, document, float(score)))
        
        return results