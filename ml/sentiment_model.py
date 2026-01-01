import numpy as np
import pickle
from tensorflow import keras
from keras.models import Sequential, load_model
from keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import config
import os

class SentimentModel:
    """Bi-LSTM model for sentiment analysis"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.label_encoder = None
        self.max_length = config.MAX_SEQUENCE_LENGTH
        self.max_vocab = config.MAX_VOCAB_SIZE
        self.embedding_dim = config.EMBEDDING_DIM
        
    def build_model(self, vocab_size: int, num_classes: int = 3):
        """
        Build Bi-LSTM architecture for sentiment classification
        
        Architecture:
        - Embedding layer
        - Bidirectional LSTM
        - Dropout for regularization
        - Dense layer with softmax activation
        """
        model = Sequential([
            Embedding(input_dim=vocab_size, 
                     output_dim=self.embedding_dim, 
                     input_length=self.max_length),
            
            Bidirectional(LSTM(64, return_sequences=True)),
            Dropout(0.3),
            
            Bidirectional(LSTM(32)),
            Dropout(0.3),
            
            Dense(64, activation='relu'),
            Dropout(0.2),
            
            Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def prepare_data(self, texts: list, labels: list = None):
        """
        Prepare text data for training/inference
        
        Args:
            texts: List of text strings
            labels: List of sentiment labels (for training)
        
        Returns:
            Padded sequences and encoded labels (if labels provided)
        """
        # Initialize tokenizer if not exists
        if self.tokenizer is None:
            self.tokenizer = Tokenizer(num_words=self.max_vocab, oov_token='<OOV>')
            self.tokenizer.fit_on_texts(texts)
        
        # Convert texts to sequences
        sequences = self.tokenizer.texts_to_sequences(texts)
        padded = pad_sequences(sequences, maxlen=self.max_length, padding='post', truncating='post')
        
        # Encode labels if provided
        if labels is not None:
            if self.label_encoder is None:
                self.label_encoder = LabelEncoder()
                self.label_encoder.fit(config.SENTIMENT_CLASSES)
            
            encoded_labels = self.label_encoder.transform(labels)
            return padded, encoded_labels
        
        return padded
    
    def train(self, texts: list, labels: list, epochs: int = 10, batch_size: int = 32, 
              validation_split: float = 0.2):
        """
        Train the sentiment model
        
        Args:
            texts: List of training texts
            labels: List of sentiment labels
            epochs: Number of training epochs
            batch_size: Batch size for training
            validation_split: Fraction of data for validation
        
        Returns:
            Training history
        """
        # Prepare data
        X, y = self.prepare_data(texts, labels)
        
        # Build model if not exists
        if self.model is None:
            vocab_size = min(len(self.tokenizer.word_index) + 1, self.max_vocab)
            self.build_model(vocab_size, num_classes=len(config.SENTIMENT_CLASSES))
        
        # Train model
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1
        )
        
        return history
    
    def predict(self, texts: list or str) -> list:
        """
        Predict sentiment for given texts
        
        Args:
            texts: Single text string or list of texts
        
        Returns:
            List of predictions with sentiment and confidence score
        """
        # Handle single text input
        if isinstance(texts, str):
            texts = [texts]
            single_input = True
        else:
            single_input = False
        
        # Prepare data
        X = self.prepare_data(texts)
        
        # Get predictions
        predictions = self.model.predict(X, verbose=0)
        
        # Convert to sentiment labels and scores
        results = []
        for pred in predictions:
            class_idx = np.argmax(pred)
            confidence = float(pred[class_idx])
            sentiment = self.label_encoder.inverse_transform([class_idx])[0]
            
            results.append({
                'sentiment': sentiment,
                'confidence': confidence,
                'probabilities': {
                    self.label_encoder.inverse_transform([i])[0]: float(pred[i])
                    for i in range(len(pred))
                }
            })
        
        return results[0] if single_input else results
    
    def save_model(self, model_path: str = None, tokenizer_path: str = None, 
                   encoder_path: str = None):
        """Save model and preprocessing artifacts"""
        model_path = model_path or str(config.SENTIMENT_MODEL_PATH)
        tokenizer_path = tokenizer_path or str(config.TOKENIZER_PATH)
        encoder_path = encoder_path or str(config.LABEL_ENCODER_PATH)
        
        # Save model
        self.model.save(model_path)
        
        # Save tokenizer
        with open(tokenizer_path, 'wb') as f:
            pickle.dump(self.tokenizer, f)
        
        # Save label encoder
        with open(encoder_path, 'wb') as f:
            pickle.dump({
                'sentiment': self.label_encoder
            }, f)
        
        print(f"Model saved to {model_path}")
        print(f"Tokenizer saved to {tokenizer_path}")
        print(f"Label encoders saved to {encoder_path}")
    
    def load_model(self, model_path: str = None, tokenizer_path: str = None, 
                   encoder_path: str = None):
        """Load model and preprocessing artifacts"""
        model_path = model_path or str(config.SENTIMENT_MODEL_PATH)
        tokenizer_path = tokenizer_path or str(config.TOKENIZER_PATH)
        encoder_path = encoder_path or str(config.LABEL_ENCODER_PATH)
        
        # Load model
        if os.path.exists(model_path):
            self.model = load_model(model_path)
            print(f"Model loaded from {model_path}")
        else:
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        # Load tokenizer
        if os.path.exists(tokenizer_path):
            with open(tokenizer_path, 'rb') as f:
                self.tokenizer = pickle.load(f)
            print(f"Tokenizer loaded from {tokenizer_path}")
        else:
            raise FileNotFoundError(f"Tokenizer not found at {tokenizer_path}")
        
        # Load label encoder
        if os.path.exists(encoder_path):
            with open(encoder_path, 'rb') as f:
                encoders = pickle.load(f)
                self.label_encoder = encoders.get('sentiment')
            print(f"Label encoder loaded from {encoder_path}")
        else:
            raise FileNotFoundError(f"Label encoder not found at {encoder_path}")


# Create singleton instance
sentiment_model = SentimentModel()
