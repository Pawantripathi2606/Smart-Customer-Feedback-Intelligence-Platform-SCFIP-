import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Database Configuration
DATABASE_PATH = BASE_DIR / "data" / "feedback.db"

# Model Paths
MODELS_DIR = BASE_DIR / "ml" / "models"
SENTIMENT_MODEL_PATH = MODELS_DIR / "sentiment_model.h5"
INTENT_MODEL_PATH = MODELS_DIR / "intent_model.h5"
TOKENIZER_PATH = MODELS_DIR / "tokenizer.pkl"
LABEL_ENCODER_PATH = MODELS_DIR / "label_encoders.pkl"

# NLP Configuration
MAX_SEQUENCE_LENGTH = 100
MAX_VOCAB_SIZE = 10000
EMBEDDING_DIM = 128

# Model Parameters
SENTIMENT_CLASSES = ["Negative", "Neutral", "Positive"]
INTENT_CLASSES = [
    "Bug Report",
    "Feature Request",
    "Performance Issue",
    "Pricing Issue",
    "General Feedback"
]

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
API_RELOAD = True

# Streamlit Configuration
STREAMLIT_PORT = 8501

# Create necessary directories
os.makedirs(BASE_DIR / "data", exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
