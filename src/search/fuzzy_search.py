import time
from ..indexing.inverted_index import InvertedIndex

class BKTreeNode:
    def __init__(self, term):
        self.term = term
        self.children = {} 

class FuzzySearch:
    def __init__(self, index=None, max_distance=2):
        self.index = index if index else InvertedIndex()
        self.max_distance = max_distance
        self.timing_stats = {'linear': [], 'bktree': []}
        self.bktree = None 
        
    def search(self, query, limit=10):
        if self.index.use_lemmatization:
            query_tokens = self.index.tokenizer.lemmatize(query)
        else:
            query_tokens = self.index.tokenizer.tokenize(query)   
            
        if not query_tokens:
            return []
        
        all_terms = set(self.index.index.keys())
        
        matches = {}
        
        for query_token in query_tokens:
            fuzzy_matches = self._get_fuzzy_matches(query_token, all_terms)
            
            for term, distance in fuzzy_matches:
                docs = self.index.index.get(term, set())
                
                fuzzy_score = 1.0/(distance + 1.0)

                for doc_id in docs:
                    if doc_id in matches:
                        matches[doc_id] += fuzzy_score
                    else:
                        matches[doc_id] = fuzzy_score
        results = []
        for doc_id, score in matches.items():
            document = self.index.get_document(doc_id)
            results.append((doc_id, document, score))
        
        results.sort(key=lambda x: x[2], reverse = True)
        return results[:limit]
    
    def _get_fuzzy_matches_linear(self, token, all_terms):
        """Linear search implementation for comparison"""
        matches = []
        for term in all_terms:
            distance = self._levenshtein_distance(token, term)
            if distance <= self.max_distance:
                matches.append((term, distance))
        matches.sort(key=lambda x: x[1])
        return matches

    def _get_fuzzy_matches(self, token, all_terms):
        # Build tree if not already built
        if self.bktree is None:
            self.build_bktree()

        start_time = time.time()
        linear_time = time.time() - start_time
        self.timing_stats['linear'].append(linear_time)

        start_time = time.time()
        matches = self.search_bk_tree(self.bktree, token, self.max_distance)
        matches.sort(key=lambda x: x[1])
        bktree_time = time.time() - start_time
        self.timing_stats['bktree'].append(bktree_time)

        return matches

    def get_average_times(self):
        """Get average execution times for both methods"""
        linear_avg = sum(self.timing_stats['linear']) / len(self.timing_stats['linear']) if self.timing_stats['linear'] else 0
        bktree_avg = sum(self.timing_stats['bktree']) / len(self.timing_stats['bktree']) if self.timing_stats['bktree'] else 0
        
        return {
            'linear_search_avg': linear_avg,
            'bktree_search_avg': bktree_avg,
            'speedup': linear_avg / bktree_avg if bktree_avg > 0 else 0
        }
    
    def _levenshtein_distance(self, s1, s2):
        m = len(s1)
        n = len(s2)
        
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
            
        for i in range(1, m + 1):
            for j in range(1, n+1):
                cost = 0 if s1[i-1] == s2[j-1] else 1
                dp[i][j] = min(
                    dp[i-1][j] + 1,      # deletion
                    dp[i][j-1] + 1,      # insertion
                    dp[i-1][j-1] + cost  # substitution
                )
        
        return dp[m][n]
    
    def bk_tree(self, term, all_terms):
        # build the bk tree
        root = BKTreeNode(term)
        all_terms.remove(term)  # Remove the root term from the set
        
        for other_term in all_terms:
            self._insert_term(root, other_term)
        
        return root

    def _insert_term(self, node, term):
        distance = self._levenshtein_distance(node.term, term)
        
        if distance == 0:
            return  # Term already exists in the tree
            
        if distance not in node.children:
            node.children[distance] = BKTreeNode(term)
        else:
            self._insert_term(node.children[distance], term)

    def search_bk_tree(self, node, query_term, max_distance):
        """
        Search for terms in the BK-tree within the given maximum distance.
        
        Args:
            node: The current node in the tree
            query_term: The term to search for
            max_distance: The maximum edit distance allowed
            
        Returns:
            List of tuples containing (term, distance) pairs
        """
        distance = self._levenshtein_distance(node.term, query_term)
        results = []
        
        if distance <= max_distance:
            results.append((node.term, distance))
        
        # Search child nodes that could contain matches
        for d in range(distance - max_distance, distance + max_distance + 1):
            if d in node.children:
                results.extend(self.search_bk_tree(node.children[d], query_term, max_distance))
        
        return results

    def build_bktree(self):
        """Build the BK-tree once for all terms in the index"""
        all_terms = set(self.index.index.keys())
        if all_terms:
            first_term = next(iter(all_terms))
            self.bktree = self.bk_tree(first_term, all_terms.copy())


