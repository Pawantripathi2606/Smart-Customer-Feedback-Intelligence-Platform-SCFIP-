"""
Training script for sentiment and intent models
Generates synthetic training data and trains both models
"""

import sys
from pathlib import Path

# Add project root to Python path to support direct execution
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import numpy as np
import random
from ml.sentiment_model import sentiment_model
from ml.intent_model import intent_model
from ml.nlp_pipeline import preprocess_batch
import config

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

def generate_training_data():
    """Generate synthetic training data for both models"""
    
    # Sentiment training data
    sentiment_data = {
        'Positive': [
            "Love the new features! Great update!",
            "The app is amazing and works perfectly",
            "Excellent customer support, very helpful",
            "Best app I've ever used, highly recommend",
            "The interface is beautiful and intuitive",
            "Great value for money, worth every penny",
            "The app has transformed my workflow",
            "Fantastic experience, no complaints",
            "The team did an excellent job",
            "Very satisfied with the product",
            "The app is fast and responsive",
            "Love the customization options",
            "The app is reliable and stable",
            "Great design and user experience",
            "The app is perfect for my needs",
            "Highly impressed with the quality",
            "The app works flawlessly",
            "Excellent performance and speed",
            "The app is well-designed",
            "Very happy with my purchase",
            "The app exceeded my expectations",
            "Outstanding features and functionality",
            "The app is smooth and bug-free",
            "Wonderful experience overall",
            "The app is exactly what I needed",
            "Brilliant app, love it",
            "The app is superb",
            "Amazing features and great UI",
            "The app is top-notch",
            "Absolutely love this app",
        ],
        'Negative': [
            "The app crashes constantly, very frustrating",
            "Terrible experience, waste of money",
            "The app is slow and buggy",
            "Customer support is unresponsive",
            "The app doesn't work as advertised",
            "Too many bugs and issues",
            "The app is confusing and hard to use",
            "Very disappointed with this product",
            "The app freezes all the time",
            "Worst app I've ever used",
            "The app is unreliable",
            "Too expensive for what it offers",
            "The app is broken after the update",
            "Cannot recommend this app",
            "The app is unstable",
            "Very poor quality",
            "The app is unusable",
            "Extremely buggy and slow",
            "The app is a disaster",
            "Completely broken",
            "The app is terrible",
            "Very frustrating to use",
            "The app is poorly designed",
            "Waste of time and money",
            "The app is awful",
            "Horrible user experience",
            "The app is a mess",
            "Very disappointing",
            "The app is garbage",
            "Absolutely terrible",
        ],
        'Neutral': [
            "The app is okay, nothing special",
            "It works but could be better",
            "Average app, does the job",
            "The app is fine for basic use",
            "Not bad but not great either",
            "The app is acceptable",
            "It's an okay product",
            "The app is decent",
            "Nothing to complain about",
            "The app is alright",
            "It works as expected",
            "The app is satisfactory",
            "No major issues",
            "The app is functional",
            "It does what it says",
            "The app is reasonable",
            "It's a standard app",
            "The app is adequate",
            "No strong feelings either way",
            "The app is passable",
            "It's an average experience",
            "The app is moderate",
            "Neither good nor bad",
            "The app is fair",
            "It's a typical app",
            "The app is ordinary",
            "No complaints but no praise",
            "The app is mediocre",
            "It's just okay",
            "The app is so-so",
        ]
    }
    
    # Intent training data
    intent_data = {
        'Bug Report': [
            "The app crashes when I try to login",
            "Error message appears on startup",
            "The app freezes when uploading images",
            "Cannot save my work, app crashes",
            "The app doesn't load properly",
            "Getting error 404 on the main page",
            "The app crashes after the update",
            "Sync is broken, data doesn't update",
            "The app keeps logging me out",
            "Cannot delete my account",
            "The search function doesn't work",
            "App crashes during video calls",
            "The app is broken after update",
            "Cannot recover my password",
            "Data export feature is broken",
            "The app crashes on startup",
            "Login page doesn't load",
            "Notifications are not working",
            "The app crashes when switching tabs",
            "Offline mode doesn't work",
            "Cannot access my data after update",
            "The app crashes when sharing content",
            "The app doesn't remember preferences",
            "App crashes when uploading files",
            "The recent update broke features",
        ],
        'Feature Request': [
            "Would love to see dark mode feature",
            "Please add calendar integration",
            "Need export to PDF feature",
            "Please add two-factor authentication",
            "Would appreciate multiple language support",
            "Please add desktop application version",
            "Need more customization options",
            "Would like to see more templates",
            "Please add keyboard shortcuts",
            "Need better filtering options",
            "Would love integration with Google Calendar",
            "Please add offline support for all features",
            "Need more payment options",
            "Would like better error handling",
            "Please add more integrations",
            "Need collaboration features",
            "Would appreciate better documentation",
            "Please add widget feature",
            "Need analytics dashboard",
            "Would like customizable themes",
            "Please add batch processing",
            "Need advanced search filters",
            "Would appreciate auto-save feature",
            "Please add notification settings",
            "Need data visualization tools",
        ],
        'Performance Issue': [
            "The app is very slow",
            "Loading times are unacceptably long",
            "The app is laggy on my device",
            "Payment processing is extremely slow",
            "The app uses too much battery",
            "Sync is very slow",
            "The app is slow and unresponsive",
            "Loading screen takes forever",
            "The app drains battery quickly",
            "Performance is poor on older devices",
            "The app is sluggish",
            "Response time is too slow",
            "The app lags frequently",
            "Loading is painfully slow",
            "The app is slow to start",
            "Performance has degraded",
            "The app is not optimized",
            "Too much memory usage",
            "The app is resource-intensive",
            "Slow data synchronization",
            "The app takes too long to load",
            "Performance issues on mobile",
            "The app is choppy",
            "Slow rendering of content",
            "The app is inefficient",
        ],
        'Pricing Issue': [
            "The pricing is too high",
            "Too expensive compared to competitors",
            "The subscription is not worth it",
            "Pricing is confusing",
            "The free tier is too limited",
            "Too expensive for students",
            "Subscription auto-renewal is unethical",
            "The premium features are overpriced",
            "Need better pricing options",
            "The cost is prohibitive",
            "Pricing model is unclear",
            "Too expensive for what it offers",
            "The subscription is too costly",
            "Need more affordable plans",
            "Pricing is not competitive",
            "The app is overpriced",
            "Need student discount",
            "The pricing structure is bad",
            "Too many paid features",
            "The cost is unreasonable",
            "Pricing is not transparent",
            "Need family plan pricing",
            "The subscription is expensive",
            "Better value needed",
            "Pricing is a barrier",
        ],
        'General Feedback': [
            "The app is great overall",
            "Good experience so far",
            "The app is useful",
            "Nice design and features",
            "The app is helpful",
            "Enjoying the app",
            "The app is convenient",
            "Good product",
            "The app is well-made",
            "Positive experience",
            "The app is effective",
            "Satisfied with the app",
            "The app is practical",
            "Good job on the app",
            "The app is beneficial",
            "Happy with the service",
            "The app is worthwhile",
            "Good overall impression",
            "The app is valuable",
            "Pleased with the app",
            "The app is solid",
            "Good work",
            "The app is commendable",
            "Nice app",
            "The app is appreciated",
        ]
    }
    
    # Expand dataset with variations
    def expand_data(data_dict, multiplier=2):
        """Create variations of existing samples"""
        expanded = {}
        for label, samples in data_dict.items():
            expanded[label] = samples.copy()
            # Add variations with minor modifications
            for _ in range(multiplier - 1):
                for sample in samples:
                    # Add punctuation variations
                    variations = [
                        sample + "!",
                        sample + ".",
                        sample.replace(".", "!"),
                        sample.capitalize(),
                    ]
                    expanded[label].extend(variations[:2])
        return expanded
    
    # Expand datasets
    sentiment_data = expand_data(sentiment_data, multiplier=3)
    intent_data = expand_data(intent_data, multiplier=3)
    
    return sentiment_data, intent_data


def train_models():
    """Train both sentiment and intent models"""
    
    print("=" * 60)
    print("GENERATING TRAINING DATA")
    print("=" * 60)
    
    sentiment_data, intent_data = generate_training_data()
    
    # Prepare sentiment training data
    sentiment_texts = []
    sentiment_labels = []
    for label, samples in sentiment_data.items():
        sentiment_texts.extend(samples)
        sentiment_labels.extend([label] * len(samples))
    
    print(f"\nSentiment training samples: {len(sentiment_texts)}")
    print(f"Sentiment classes: {set(sentiment_labels)}")
    
    # Prepare intent training data
    intent_texts = []
    intent_labels = []
    for label, samples in intent_data.items():
        intent_texts.extend(samples)
        intent_labels.extend([label] * len(samples))
    
    print(f"\nIntent training samples: {len(intent_texts)}")
    print(f"Intent classes: {set(intent_labels)}")
    
    # Preprocess texts
    print("\n" + "=" * 60)
    print("PREPROCESSING TEXTS")
    print("=" * 60)
    
    sentiment_texts_clean = preprocess_batch(sentiment_texts)
    intent_texts_clean = preprocess_batch(intent_texts)
    
    print(f"Preprocessing complete!")
    
    # Train sentiment model
    print("\n" + "=" * 60)
    print("TRAINING SENTIMENT MODEL (Bi-LSTM)")
    print("=" * 60)
    
    sentiment_history = sentiment_model.train(
        sentiment_texts_clean,
        sentiment_labels,
        epochs=15,
        batch_size=32,
        validation_split=0.2
    )
    
    # Save sentiment model
    sentiment_model.save_model()
    
    # Train intent model (use same tokenizer as sentiment model)
    print("\n" + "=" * 60)
    print("TRAINING INTENT MODEL (LSTM)")
    print("=" * 60)
    
    intent_model.set_tokenizer(sentiment_model.tokenizer)
    
    intent_history = intent_model.train(
        intent_texts_clean,
        intent_labels,
        epochs=15,
        batch_size=32,
        validation_split=0.2
    )
    
    # Save intent model
    intent_model.save_model()
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    
    # Print final accuracies
    sentiment_acc = sentiment_history.history['accuracy'][-1]
    sentiment_val_acc = sentiment_history.history['val_accuracy'][-1]
    
    intent_acc = intent_history.history['accuracy'][-1]
    intent_val_acc = intent_history.history['val_accuracy'][-1]
    
    print(f"\nSentiment Model:")
    print(f"  Training Accuracy: {sentiment_acc:.4f}")
    print(f"  Validation Accuracy: {sentiment_val_acc:.4f}")
    
    print(f"\nIntent Model:")
    print(f"  Training Accuracy: {intent_acc:.4f}")
    print(f"  Validation Accuracy: {intent_val_acc:.4f}")
    
    # Test predictions
    print("\n" + "=" * 60)
    print("TESTING PREDICTIONS")
    print("=" * 60)
    
    test_samples = [
        "The app crashes after login. Very frustrating!",
        "Love the new dark mode feature!",
        "The app is slow and laggy",
        "Please add calendar integration",
        "The pricing is too expensive"
    ]
    
    for sample in test_samples:
        clean_sample = preprocess_batch([sample])[0]
        sentiment_pred = sentiment_model.predict(clean_sample)
        intent_pred = intent_model.predict(clean_sample)
        
        print(f"\nText: {sample}")
        print(f"  Sentiment: {sentiment_pred['sentiment']} (confidence: {sentiment_pred['confidence']:.2f})")
        print(f"  Intent: {intent_pred['intent']} (confidence: {intent_pred['confidence']:.2f})")
    
    print("\n" + "=" * 60)
    print("Models trained and saved successfully!")
    print("=" * 60)


if __name__ == "__main__":
    train_models()
