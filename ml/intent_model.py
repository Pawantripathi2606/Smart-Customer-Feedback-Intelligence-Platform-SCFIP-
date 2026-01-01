import numpy as np
import pickle
from tensorflow import keras
from keras.models import Sequential, load_model
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import config
import os

class IntentModel:
    """LSTM model for intent classification"""
    
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.max_length = config.MAX_SEQUENCE_LENGTH
        self.embedding_dim = config.EMBEDDING_DIM
        # Will use the same tokenizer as sentiment model for consistency
        self.tokenizer = None
    
    def build_model(self, vocab_size: int, num_classes: int = 5):
        """
        Build LSTM architecture for intent classification
        
        Architecture:
        - Embedding layer
        - LSTM layers
        - Dropout for regularization
        - Dense layer with softmax activation
        """
        model = Sequential([
            Embedding(input_dim=vocab_size, 
                     output_dim=self.embedding_dim, 
                     input_length=self.max_length),
            
            LSTM(128, return_sequences=True),
            Dropout(0.3),
            
            LSTM(64),
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
    
    def set_tokenizer(self, tokenizer):
        """Set tokenizer (shared with sentiment model)"""
        self.tokenizer = tokenizer
    
    def prepare_data(self, texts: list, labels: list = None):
        """
        Prepare text data for training/inference
        
        Args:
            texts: List of text strings
            labels: List of intent labels (for training)
        
        Returns:
            Padded sequences and encoded labels (if labels provided)
        """
        if self.tokenizer is None:
            raise ValueError("Tokenizer not set. Use set_tokenizer() first.")
        
        # Convert texts to sequences
        sequences = self.tokenizer.texts_to_sequences(texts)
        padded = pad_sequences(sequences, maxlen=self.max_length, padding='post', truncating='post')
        
        # Encode labels if provided
        if labels is not None:
            if self.label_encoder is None:
                self.label_encoder = LabelEncoder()
                self.label_encoder.fit(config.INTENT_CLASSES)
            
            encoded_labels = self.label_encoder.transform(labels)
            return padded, encoded_labels
        
        return padded
    
    def train(self, texts: list, labels: list, epochs: int = 10, batch_size: int = 32, 
              validation_split: float = 0.2):
        """
        Train the intent model
        
        Args:
            texts: List of training texts
            labels: List of intent labels
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
            vocab_size = min(len(self.tokenizer.word_index) + 1, config.MAX_VOCAB_SIZE)
            self.build_model(vocab_size, num_classes=len(config.INTENT_CLASSES))
        
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
        Predict intent for given texts
        
        Args:
            texts: Single text string or list of texts
        
        Returns:
            List of predictions with intent and confidence score
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
        
        # Convert to intent labels and scores
        results = []
        for pred in predictions:
            class_idx = np.argmax(pred)
            confidence = float(pred[class_idx])
            intent = self.label_encoder.inverse_transform([class_idx])[0]
            
            results.append({
                'intent': intent,
                'confidence': confidence,
                'probabilities': {
                    self.label_encoder.inverse_transform([i])[0]: float(pred[i])
                    for i in range(len(pred))
                }
            })
        
        return results[0] if single_input else results
    
    def save_model(self, model_path: str = None):
        """Save intent model"""
        model_path = model_path or str(config.INTENT_MODEL_PATH)
        
        # Save model
        self.model.save(model_path)
        print(f"Intent model saved to {model_path}")
        
        # Update label encoders file with intent encoder
        encoder_path = str(config.LABEL_ENCODER_PATH)
        encoders = {}
        
        # Load existing encoders if file exists
        if os.path.exists(encoder_path):
            with open(encoder_path, 'rb') as f:
                encoders = pickle.load(f)
        
        # Add intent encoder
        encoders['intent'] = self.label_encoder
        
        # Save updated encoders
        with open(encoder_path, 'wb') as f:
            pickle.dump(encoders, f)
        
        print(f"Intent label encoder saved to {encoder_path}")
    
    def load_model(self, model_path: str = None, encoder_path: str = None):
        """Load intent model and label encoder"""
        model_path = model_path or str(config.INTENT_MODEL_PATH)
        encoder_path = encoder_path or str(config.LABEL_ENCODER_PATH)
        
        # Load model
        if os.path.exists(model_path):
            self.model = load_model(model_path)
            print(f"Intent model loaded from {model_path}")
        else:
            raise FileNotFoundError(f"Intent model not found at {model_path}")
        
        # Load label encoder
        if os.path.exists(encoder_path):
            with open(encoder_path, 'rb') as f:
                encoders = pickle.load(f)
                self.label_encoder = encoders.get('intent')
            print(f"Intent label encoder loaded from {encoder_path}")
        else:
            raise FileNotFoundError(f"Label encoder not found at {encoder_path}")


# Create singleton instance
intent_model = IntentModel()
