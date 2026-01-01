import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np

# Download required NLTK data (will only download if not present)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading punkt...")
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading stopwords...")
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    print("Downloading wordnet...")
    nltk.download('wordnet', quiet=True)

# Try to download punkt_tab, but don't fail if it doesn't exist
try:
    nltk.data.find('tokenizers/punkt_tab')
except (LookupError, OSError):
    try:
        print("Downloading punkt_tab...")
        nltk.download('punkt_tab', quiet=True)
    except:
        # punkt_tab might not be available in all NLTK versions
        # punkt alone is sufficient for tokenization
        pass

class NLPPipeline:
    """Complete NLP preprocessing pipeline for customer feedback"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
        # Keep some sentiment-bearing words that are usually stopwords
        self.stop_words -= {'not', 'no', 'never', 'very', 'too', 'but', 'however'}
    
    def clean_text(self, text: str) -> str:
        """
        Clean text by:
        - Converting to lowercase
        - Removing URLs
        - Removing special characters
        - Removing extra whitespace
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Remove numbers (optional - keep if numbers are meaningful)
        # text = re.sub(r'\d+', '', text)
        
        # Remove punctuation but keep sentence structure
        # We'll keep periods and commas for better tokenization
        text = re.sub(r'[^\w\s.,!?]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text: str) -> list:
        """Tokenize text into words"""
        try:
            tokens = word_tokenize(text)
        except:
            # Fallback to simple split if punkt tokenizer fails
            tokens = text.split()
        return tokens
    
    def remove_stopwords(self, tokens: list) -> list:
        """Remove stopwords while keeping sentiment-bearing words"""
        return [token for token in tokens if token not in self.stop_words]
    
    def lemmatize(self, tokens: list) -> list:
        """Lemmatize tokens to their base form"""
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def remove_punctuation(self, tokens: list) -> list:
        """Remove punctuation tokens"""
        return [token for token in tokens if token not in string.punctuation]
    
    def preprocess_text(self, text: str, return_string: bool = True) -> str or list:
        """
        Complete preprocessing pipeline
        
        Args:
            text: Input text to preprocess
            return_string: If True, return joined string; if False, return list of tokens
        
        Returns:
            Preprocessed text as string or list of tokens
        """
        # Step 1: Clean text
        cleaned = self.clean_text(text)
        
        # Step 2: Tokenize
        tokens = self.tokenize(cleaned)
        
        # Step 3: Remove punctuation
        tokens = self.remove_punctuation(tokens)
        
        # Step 4: Remove stopwords
        tokens = self.remove_stopwords(tokens)
        
        # Step 5: Lemmatize
        tokens = self.lemmatize(tokens)
        
        # Step 6: Remove empty tokens
        tokens = [token for token in tokens if token.strip()]
        
        if return_string:
            return ' '.join(tokens)
        return tokens
    
    def extract_keywords(self, text: str, top_n: int = 5) -> list:
        """Extract top keywords from text"""
        tokens = self.preprocess_text(text, return_string=False)
        
        # Simple frequency-based keyword extraction
        from collections import Counter
        word_freq = Counter(tokens)
        
        return [word for word, _ in word_freq.most_common(top_n)]
    
    def get_text_stats(self, text: str) -> dict:
        """Get statistics about the text"""
        tokens = self.preprocess_text(text, return_string=False)
        
        return {
            "original_length": len(text),
            "token_count": len(tokens),
            "unique_tokens": len(set(tokens)),
            "avg_word_length": np.mean([len(token) for token in tokens]) if tokens else 0
        }


# Singleton instance
nlp_pipeline = NLPPipeline()


def preprocess_text(text: str) -> str:
    """Convenience function for text preprocessing"""
    return nlp_pipeline.preprocess_text(text)


def preprocess_batch(texts: list) -> list:
    """Preprocess a batch of texts"""
    return [nlp_pipeline.preprocess_text(text) for text in texts]
