import re
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords

class Tokenizer:
    """
    Handles text tokenization and preprocessing.
    """
    
    def __init__(self, remove_stopwords=True):
        """
        Initialize the tokenizer.
        
        Args:
            remove_stopwords (bool): Whether to remove stopwords
        """
        self.remove_stopwords = remove_stopwords
        
        self.stop_words = set(stopwords.words('english')) if remove_stopwords else set()
    
    
    def tokenize(self, text):
        """
        Tokenize and preprocess text.
        
        Args:
            text (str): The text to tokenize
            
        Returns:
            list: A list of preprocessed tokens
        """
        tokens = re.findall(r'\w+', text.lower())
    
        if self.remove_stopwords:
            tokens = [token for token in tokens if token not in self.stop_words]
        
        return tokens