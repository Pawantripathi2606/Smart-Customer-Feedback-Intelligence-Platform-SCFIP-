from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FeedbackInput(BaseModel):
    """Schema for incoming feedback"""
    feedback_id: str = Field(..., description="Unique feedback identifier")
    text: str = Field(..., min_length=1, description="Feedback text content")
    source: str = Field(..., description="Source of feedback (Mobile App, Web, Support)")
    date: str = Field(..., description="Date of feedback (YYYY-MM-DD)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "feedback_id": "F101",
                "text": "The app crashes after login",
                "source": "Mobile App",
                "date": "2026-01-01"
            }
        }

class AnalysisRequest(BaseModel):
    """Schema for text analysis request"""
    text: str = Field(..., min_length=1, description="Text to analyze")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "The app crashes after login. Very frustrating!"
            }
        }

class AnalysisResult(BaseModel):
    """Schema for analysis results"""
    text: str
    sentiment: str = Field(..., description="Sentiment: Positive, Neutral, or Negative")
    sentiment_score: float = Field(..., ge=0, le=1, description="Confidence score for sentiment")
    intent: str = Field(..., description="Intent category")
    intent_score: float = Field(..., ge=0, le=1, description="Confidence score for intent")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "The app crashes after login",
                "sentiment": "Negative",
                "sentiment_score": 0.95,
                "intent": "Bug Report",
                "intent_score": 0.89
            }
        }

class FeedbackResponse(BaseModel):
    """Schema for feedback response"""
    id: int
    feedback_id: str
    text: str
    source: str
    date: str
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    intent: Optional[str] = None
    intent_score: Optional[float] = None
    created_at: str
    
    class Config:
        from_attributes = True

class AnalyticsSummary(BaseModel):
    """Schema for analytics summary"""
    total_feedback: int
    avg_sentiment_score: float
    top_intent: str
    sentiment_distribution: dict
    intent_distribution: dict
    source_distribution: dict
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_feedback": 100,
                "avg_sentiment_score": 0.65,
                "top_intent": "Bug Report",
                "sentiment_distribution": {
                    "Positive": 40,
                    "Neutral": 30,
                    "Negative": 30
                },
                "intent_distribution": {
                    "Bug Report": 35,
                    "Feature Request": 25,
                    "General Feedback": 20,
                    "Performance Issue": 15,
                    "Pricing Issue": 5
                },
                "source_distribution": {
                    "Mobile App": 60,
                    "Web": 25,
                    "Support": 15
                }
            }
        }

class BulkFeedbackInput(BaseModel):
    """Schema for bulk feedback upload"""
    feedbacks: list[FeedbackInput]
    
    class Config:
        json_schema_extra = {
            "example": {
                "feedbacks": [
                    {
                        "feedback_id": "F101",
                        "text": "Great app!",
                        "source": "Mobile App",
                        "date": "2026-01-01"
                    },
                    {
                        "feedback_id": "F102",
                        "text": "Needs improvement",
                        "source": "Web",
                        "date": "2026-01-01"
                    }
                ]
            }
        }

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Feedback added successfully",
                "success": True
            }
        }
