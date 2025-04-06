import spacy

class Tokenizer:
    """
    Handles text tokenization and preprocessing using spaCy.
    """
    
    def __init__(self, remove_stopwords=True, language_model="en_core_web_sm"):
        """
        Initialize the tokenizer.
        
        Args:
            remove_stopwords (bool): Whether to remove stopwords
            language_model (str): The spaCy language model to use
        """
        self.remove_stopwords = remove_stopwords
        self.nlp = spacy.load(language_model)
        
        # For better performance when we just need tokenization
        if not remove_stopwords:
            # Create a pipeline with only tokenization
            self.nlp = spacy.load(language_model, disable=["tagger", "parser", "ner", "lemmatizer"])
    
    def tokenize(self, text):
        """
        Tokenize and preprocess text.
        
        Args:
            text (str): The text to tokenize
            
        Returns:
            list: A list of preprocessed tokens
        """
        doc = self.nlp(text.lower())
        
        if self.remove_stopwords:
            tokens = [token.text for token in doc if not token.is_stop and not token.is_punct and token.text.strip()]
        else:
            tokens = [token.text for token in doc if not token.is_punct and token.text.strip()]
            
        return tokens
    
    def lemmatize(self, text):
        """
        Tokenize and lemmatize text.
        
        Args:
            text (str): The text to process
            
        Returns:
            list: A list of lemmatized tokens
        """
        doc = self.nlp(text.lower())
        
        if self.remove_stopwords:
            lemmas = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.text.strip()]
        else:
            lemmas = [token.lemma_ for token in doc if not token.is_punct and token.text.strip()]
            
        return lemmas