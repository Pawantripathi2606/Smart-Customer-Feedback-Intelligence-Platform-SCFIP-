import sys
from pathlib import Path

# Add project root to Python path to support direct execution
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import feedback
from ml.sentiment_model import sentiment_model
from ml.intent_model import intent_model
import config
import os

# Create FastAPI app
app = FastAPI(
    title="Smart Customer Feedback Intelligence Platform",
    description="AI-powered customer feedback analysis system with NLP and Deep Learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(feedback.router)


@app.on_event("startup")
async def startup_event():
    """Load models on startup if they exist"""
    print("=" * 60)
    print("Starting Smart Customer Feedback Intelligence Platform")
    print("=" * 60)
    
    # Check if models exist
    models_exist = (
        os.path.exists(str(config.SENTIMENT_MODEL_PATH)) and
        os.path.exists(str(config.INTENT_MODEL_PATH)) and
        os.path.exists(str(config.TOKENIZER_PATH))
    )
    
    if models_exist:
        try:
            print("\nLoading trained models...")
            sentiment_model.load_model()
            intent_model.load_model()
            intent_model.set_tokenizer(sentiment_model.tokenizer)
            print("\n✓ Models loaded successfully!")
        except Exception as e:
            print(f"\n✗ Error loading models: {e}")
            print("Please run 'python ml/train_models.py' to train the models.")
    else:
        print("\n⚠ Models not found!")
        print("Please run 'python ml/train_models.py' to train the models first.")
    
    print("\n" + "=" * 60)
    print("API Server Ready!")
    print("=" * 60)
    print(f"Docs: http://localhost:{config.API_PORT}/docs")
    print("=" * 60 + "\n")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Smart Customer Feedback Intelligence Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "add_feedback": "POST /api/feedback/add",
            "bulk_upload": "POST /api/feedback/bulk",
            "analyze_text": "POST /api/analyze",
            "analyze_feedback": "POST /api/feedback/analyze/{feedback_id}",
            "analyze_all": "POST /api/feedback/analyze-all",
            "get_all_feedback": "GET /api/feedback/all",
            "get_feedback": "GET /api/feedback/{feedback_id}",
            "get_analytics": "GET /api/analytics/summary",
            "get_trends": "GET /api/analytics/trends",
            "get_negative": "GET /api/analytics/negative-feedback"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    models_loaded = (
        sentiment_model.model is not None and
        intent_model.model is not None
    )
    
    return {
        "status": "healthy",
        "models_loaded": models_loaded,
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.API_RELOAD
    )
