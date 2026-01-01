from fastapi import APIRouter, HTTPException, status
from backend.schemas.feedback import (
    FeedbackInput, AnalysisRequest, AnalysisResult,
    FeedbackResponse, AnalyticsSummary, MessageResponse,
    BulkFeedbackInput
)
from backend.database.db import db
from ml.sentiment_model import sentiment_model
from ml.intent_model import intent_model
from ml.nlp_pipeline import preprocess_text
from typing import List, Optional
import os
import config

router = APIRouter(prefix="/api", tags=["feedback"])

# Check if models are trained
MODELS_TRAINED = (
    os.path.exists(str(config.SENTIMENT_MODEL_PATH)) and
    os.path.exists(str(config.INTENT_MODEL_PATH)) and
    os.path.exists(str(config.TOKENIZER_PATH))
)


@router.post("/feedback/add", response_model=MessageResponse)
async def add_feedback(feedback: FeedbackInput):
    """
    Add new customer feedback to the database
    
    - **feedback_id**: Unique identifier for the feedback
    - **text**: The feedback text content
    - **source**: Source of feedback (Mobile App, Web, Support)
    - **date**: Date of feedback (YYYY-MM-DD format)
    """
    feedback_dict = feedback.model_dump()
    
    # Initialize sentiment and intent as None
    feedback_dict['sentiment'] = None
    feedback_dict['sentiment_score'] = None
    feedback_dict['intent'] = None
    feedback_dict['intent_score'] = None
    
    success = db.add_feedback(feedback_dict)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Feedback with ID {feedback.feedback_id} already exists"
        )
    
    return MessageResponse(
        message=f"Feedback {feedback.feedback_id} added successfully",
        success=True
    )


@router.post("/feedback/bulk", response_model=MessageResponse)
async def add_bulk_feedback(bulk_input: BulkFeedbackInput):
    """
    Add multiple feedback entries at once
    
    - **feedbacks**: List of feedback objects to add
    """
    added_count = 0
    failed_count = 0
    
    for feedback in bulk_input.feedbacks:
        feedback_dict = feedback.model_dump()
        feedback_dict['sentiment'] = None
        feedback_dict['sentiment_score'] = None
        feedback_dict['intent'] = None
        feedback_dict['intent_score'] = None
        
        success = db.add_feedback(feedback_dict)
        if success:
            added_count += 1
        else:
            failed_count += 1
    
    return MessageResponse(
        message=f"Added {added_count} feedback entries. {failed_count} duplicates skipped.",
        success=True
    )


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_feedback(request: AnalysisRequest):
    """
    Analyze feedback text using NLP and Deep Learning models
    
    Returns sentiment (Positive/Neutral/Negative) and intent classification
    
    - **text**: The feedback text to analyze
    """
    if not MODELS_TRAINED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Models not trained yet. Please run 'python ml/train_models.py' first."
        )
    
    # Preprocess text
    clean_text = preprocess_text(request.text)
    
    # Get predictions
    sentiment_pred = sentiment_model.predict(clean_text)
    intent_pred = intent_model.predict(clean_text)
    
    return AnalysisResult(
        text=request.text,
        sentiment=sentiment_pred['sentiment'],
        sentiment_score=sentiment_pred['confidence'],
        intent=intent_pred['intent'],
        intent_score=intent_pred['confidence']
    )


@router.post("/feedback/analyze/{feedback_id}", response_model=MessageResponse)
async def analyze_stored_feedback(feedback_id: str):
    """
    Analyze a specific feedback entry already in the database
    
    - **feedback_id**: The ID of the feedback to analyze
    """
    if not MODELS_TRAINED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Models not trained yet. Please run 'python ml/train_models.py' first."
        )
    
    # Get feedback from database
    feedback = db.get_feedback_by_id(feedback_id)
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feedback with ID {feedback_id} not found"
        )
    
    # Preprocess and analyze
    clean_text = preprocess_text(feedback['text'])
    sentiment_pred = sentiment_model.predict(clean_text)
    intent_pred = intent_model.predict(clean_text)
    
    # Update database
    db.update_feedback_analysis(
        feedback_id=feedback_id,
        sentiment=sentiment_pred['sentiment'],
        sentiment_score=sentiment_pred['confidence'],
        intent=intent_pred['intent'],
        intent_score=intent_pred['confidence']
    )
    
    return MessageResponse(
        message=f"Feedback {feedback_id} analyzed and updated successfully",
        success=True
    )


@router.post("/feedback/analyze-all", response_model=MessageResponse)
async def analyze_all_feedback():
    """
    Analyze all feedback entries in the database that haven't been analyzed yet
    """
    if not MODELS_TRAINED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Models not trained yet. Please run 'python ml/train_models.py' first."
        )
    
    # Get all feedback
    all_feedback = db.get_all_feedback()
    
    analyzed_count = 0
    for feedback in all_feedback:
        # Skip if already analyzed
        if feedback.get('sentiment') is not None:
            continue
        
        # Analyze
        clean_text = preprocess_text(feedback['text'])
        sentiment_pred = sentiment_model.predict(clean_text)
        intent_pred = intent_model.predict(clean_text)
        
        # Update database
        db.update_feedback_analysis(
            feedback_id=feedback['feedback_id'],
            sentiment=sentiment_pred['sentiment'],
            sentiment_score=sentiment_pred['confidence'],
            intent=intent_pred['intent'],
            intent_score=intent_pred['confidence']
        )
        
        analyzed_count += 1
    
    return MessageResponse(
        message=f"Analyzed {analyzed_count} feedback entries",
        success=True
    )


@router.get("/feedback/all", response_model=List[FeedbackResponse])
async def get_all_feedback(
    limit: Optional[int] = None,
    source: Optional[str] = None,
    sentiment: Optional[str] = None
):
    """
    Retrieve all feedback with optional filters
    
    - **limit**: Maximum number of results to return
    - **source**: Filter by source (Mobile App, Web, Support)
    - **sentiment**: Filter by sentiment (Positive, Neutral, Negative)
    """
    feedback_list = db.get_all_feedback(limit=limit, source=source, sentiment=sentiment)
    return feedback_list


@router.get("/feedback/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(feedback_id: str):
    """
    Get a specific feedback entry by ID
    
    - **feedback_id**: The unique identifier of the feedback
    """
    feedback = db.get_feedback_by_id(feedback_id)
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feedback with ID {feedback_id} not found"
        )
    
    return feedback


@router.get("/analytics/summary", response_model=AnalyticsSummary)
async def get_analytics_summary():
    """
    Get aggregated analytics and insights
    
    Returns overall statistics, sentiment distribution, intent distribution, and source breakdown
    """
    summary_stats = db.get_summary_stats()
    sentiment_dist = db.get_sentiment_distribution()
    intent_dist = db.get_intent_distribution()
    source_dist = db.get_source_distribution()
    
    return AnalyticsSummary(
        total_feedback=summary_stats['total_feedback'],
        avg_sentiment_score=summary_stats['avg_sentiment_score'],
        top_intent=summary_stats['top_intent'],
        sentiment_distribution=sentiment_dist,
        intent_distribution=intent_dist,
        source_distribution=source_dist
    )


@router.get("/analytics/trends")
async def get_trends():
    """
    Get feedback trends over time
    
    Returns time-series data of sentiment trends
    """
    trends = db.get_trends_by_date()
    return {"trends": trends}


@router.get("/analytics/negative-feedback", response_model=List[FeedbackResponse])
async def get_negative_feedback(limit: int = 10):
    """
    Get most recent negative feedback for quick review
    
    - **limit**: Number of negative feedback entries to return (default: 10)
    """
    negative_feedback = db.get_negative_feedback(limit=limit)
    return negative_feedback
