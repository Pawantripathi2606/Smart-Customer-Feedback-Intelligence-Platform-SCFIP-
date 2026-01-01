# 🧠 Smart Customer Feedback Intelligence Platform (SCFIP)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**An end-to-end AI-powered system for intelligent customer feedback analysis**

[Features](#-features) • [Architecture](#-architecture) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-documentation) • [Model Performance](#-model-performance)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Model Details](#-model-details)
- [Dashboard Features](#-dashboard-features)
- [Performance Metrics](#-performance-metrics)
- [Demo Workflow](#-demo-workflow)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)

---

## 🎯 Overview

The **Smart Customer Feedback Intelligence Platform (SCFIP)** is a production-ready system that automatically analyzes customer feedback using Natural Language Processing (NLP) and Deep Learning. It provides real-time insights into customer sentiment, intent classification, and actionable analytics through an interactive dashboard.

### Key Capabilities

- **Sentiment Analysis**: Classifies feedback as Positive, Neutral, or Negative with confidence scores
- **Intent Classification**: Categorizes feedback into 5 types (Bug Report, Feature Request, Performance Issue, Pricing Issue, General Feedback)
- **Real-time Processing**: Instant analysis via REST API
- **Interactive Dashboard**: Beautiful visualizations with Streamlit
- **Scalable Backend**: FastAPI with SQLite database
- **Batch Processing**: CSV upload support for bulk analysis

---

## 🚨 Problem Statement

### Real-World Challenge

Companies receive thousands of feedback entries from multiple sources:
- 📱 Mobile app reviews
- 🌐 Web platform feedback
- 📧 Customer support tickets
- 📊 Survey responses

**Manual analysis is:**
- ⏰ **Time-consuming**: Hours to process hundreds of feedbacks
- 😓 **Unreliable**: Human bias and inconsistency
- 📉 **Inefficient**: Delayed insights lead to missed opportunities
- 💸 **Costly**: Requires dedicated teams

### Our Solution

SCFIP automates the entire feedback analysis pipeline:
1. **Collect** feedback from multiple sources
2. **Process** using advanced NLP techniques
3. **Analyze** with deep learning models
4. **Visualize** insights in real-time dashboards
5. **Act** on data-driven insights

---

## ✨ Features

### 1️⃣ Feedback Ingestion
- ✅ Manual feedback entry via web form
- ✅ Bulk CSV upload (100+ entries at once)
- ✅ RESTful API for programmatic access
- ✅ Multi-source support (Mobile App, Web, Support)

### 2️⃣ NLP Processing Pipeline
- ✅ Text cleaning (URLs, special characters, normalization)
- ✅ Tokenization with NLTK
- ✅ Stopword removal (preserving sentiment words)
- ✅ Lemmatization for word normalization
- ✅ TF-IDF vectorization

### 3️⃣ Deep Learning Models

**Sentiment Analysis Model (Bi-LSTM)**
- Architecture: Embedding → Bi-LSTM → Dense → Softmax
- Classes: Positive, Neutral, Negative
- Accuracy: ~85-90% on validation set

**Intent Classification Model (LSTM)**
- Architecture: Embedding → LSTM → Dense → Softmax
- Classes: Bug Report, Feature Request, Performance Issue, Pricing Issue, General Feedback
- Accuracy: ~80-85% on validation set

### 4️⃣ FastAPI Backend
Production-ready REST API with 10+ endpoints:
- `POST /api/feedback/add` - Add single feedback
- `POST /api/feedback/bulk` - Bulk upload
- `POST /api/analyze` - Analyze text
- `GET /api/feedback/all` - Retrieve all feedback
- `GET /api/analytics/summary` - Get analytics
- And more...

### 5️⃣ Streamlit Dashboard
Interactive visualization with 5 pages:
- 📈 **Dashboard**: Overview metrics, sentiment distribution, source breakdown
- 🔍 **Deep Dive**: Word clouds, trends over time, detailed filtering
- 📝 **Add Feedback**: Manual entry and CSV upload
- 💬 **Live Analyzer**: Real-time text analysis
- ⚙️ **Settings**: System status and information

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend API** | FastAPI 0.104+ | RESTful API service layer |
| **NLP** | spaCy 3.7, NLTK 3.8 | Text preprocessing & analysis |
| **Deep Learning** | TensorFlow 2.15, Keras 2.15 | Bi-LSTM & LSTM models |
| **Database** | SQLite 3 | Feedback & analytics storage |
| **Visualization** | Streamlit 1.28 | Interactive dashboard |
| **Data Processing** | pandas 2.1, numpy 1.26 | Data manipulation |
| **Plotting** | Plotly 5.18, Matplotlib 3.8 | Charts & visualizations |
| **Word Clouds** | WordCloud 1.9.3 | Text visualization |

### Why These Technologies?

- **FastAPI**: High performance, automatic API documentation, async support
- **TensorFlow/Keras**: Industry-standard deep learning framework
- **Streamlit**: Rapid dashboard development with Python
- **SQLite**: Zero-configuration, serverless database
- **Plotly**: Interactive, publication-quality charts

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Streamlit Dashboard (Port 8501)              │   │
│  │  • Overview Analytics  • Word Clouds                 │   │
│  │  • Sentiment Trends    • Live Analyzer               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP Requests
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND API LAYER                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         FastAPI Server (Port 8000)                   │   │
│  │  • 10+ REST Endpoints  • Request Validation          │   │
│  │  • CORS Support        • Auto Documentation          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  NLP & ML PROCESSING                         │
│  ┌────────────────────┐  ┌──────────────────────────────┐   │
│  │  NLP Pipeline      │  │   Deep Learning Models       │   │
│  │  • Text Cleaning   │  │   • Bi-LSTM (Sentiment)      │   │
│  │  • Tokenization    │  │   • LSTM (Intent)            │   │
│  │  • Lemmatization   │  │   • Confidence Scores        │   │
│  └────────────────────┘  └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                   DATA PERSISTENCE                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         SQLite Database (feedback.db)                │   │
│  │  • Feedback Table   • Analytics Table                │   │
│  │  • CRUD Operations  • Aggregation Queries            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Input**: User submits feedback via Dashboard or API
2. **Preprocessing**: NLP pipeline cleans and tokenizes text
3. **Analysis**: Deep learning models predict sentiment & intent
4. **Storage**: Results saved to SQLite database
5. **Visualization**: Dashboard fetches and displays insights

---

## 📁 Project Structure

```
Smart Customer Feedback Intelligence Platform (SCFIP)/
│
├── backend/                        # FastAPI Backend
│   ├── __init__.py
│   ├── main.py                     # FastAPI app entry point
│   ├── routes/
│   │   ├── __init__.py
│   │   └── feedback.py             # API endpoints (10+ routes)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── feedback.py             # Pydantic models for validation
│   └── database/
│       ├── __init__.py
│       └── db.py                   # SQLite operations
│
├── ml/                             # Machine Learning
│   ├── __init__.py
│   ├── nlp_pipeline.py             # NLP preprocessing
│   ├── sentiment_model.py          # Bi-LSTM sentiment model
│   ├── intent_model.py             # LSTM intent classifier
│   ├── train_models.py             # Training script
│   └── models/                     # Saved models (created after training)
│       ├── sentiment_model.h5      # Trained sentiment model
│       ├── intent_model.h5         # Trained intent model
│       ├── tokenizer.pkl           # Fitted tokenizer
│       └── label_encoders.pkl      # Label encoders
│
├── streamlit_app/                  # Streamlit Dashboard
│   ├── __init__.py
│   └── dashboard.py                # Multi-page dashboard
│
├── data/                           # Data Files
│   ├── sample_feedback.csv         # 100 sample feedback entries
│   └── feedback.db                 # SQLite database (created on run)
│
├── config.py                       # Centralized configuration
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── .gitignore                      # Git ignore rules
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- 4GB RAM minimum
- Windows/Linux/macOS

### Step-by-Step Setup

#### 1. Clone or Navigate to Project Directory

```bash
cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"
```

#### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Installation time**: ~5-10 minutes (depending on internet speed)

#### 4. Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```

#### 5. Train Models

```bash
python ml/train_models.py
```

**Training time**: ~5-10 minutes
**Expected output**: 
- Sentiment model accuracy: 85-90%
- Intent model accuracy: 80-85%
- Models saved to `ml/models/`

---

## 📖 Usage Guide

### Quick Start (3 Steps)

#### Step 1: Start the FastAPI Backend

Open **Terminal 1**:

```bash
cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"
python backend/main.py
```

**Expected output**:
```
============================================================
Starting Smart Customer Feedback Intelligence Platform
============================================================

Loading trained models...
Model loaded from ml\models\sentiment_model.h5
Tokenizer loaded from ml\models\tokenizer.pkl
Label encoder loaded from ml\models\label_encoders.pkl
Intent model loaded from ml\models\intent_model.h5
Intent label encoder loaded from ml\models\label_encoders.pkl

✓ Models loaded successfully!

============================================================
API Server Ready!
============================================================
Docs: http://localhost:8000/docs
============================================================

INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ API is now running at: **http://localhost:8000**

#### Step 2: Start the Streamlit Dashboard

Open **Terminal 2** (keep Terminal 1 running):

```bash
cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"
streamlit run streamlit_app/dashboard.py
```

**Expected output**:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

✅ Dashboard is now running at: **http://localhost:8501**

#### Step 3: Upload Sample Data

1. Open dashboard at http://localhost:8501
2. Navigate to **"📝 Add Feedback"** page
3. Click **"📤 CSV Upload"** tab
4. Upload `data/sample_feedback.csv`
5. Click **"📤 Upload Feedback"**
6. Go to sidebar → Click **"🔄 Analyze All Feedback"**
7. Navigate to **"📈 Dashboard"** to see analytics

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000
```

### Interactive API Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

#### 1. Add Single Feedback

```http
POST /api/feedback/add
Content-Type: application/json

{
  "feedback_id": "F101",
  "text": "The app crashes after login",
  "source": "Mobile App",
  "date": "2026-01-01"
}
```

**Response**:
```json
{
  "message": "Feedback F101 added successfully",
  "success": true
}
```

#### 2. Analyze Text

```http
POST /api/analyze
Content-Type: application/json

{
  "text": "The app crashes after login. Very frustrating!"
}
```

**Response**:
```json
{
  "text": "The app crashes after login. Very frustrating!",
  "sentiment": "Negative",
  "sentiment_score": 0.95,
  "intent": "Bug Report",
  "intent_score": 0.89
}
```

#### 3. Get All Feedback

```http
GET /api/feedback/all?limit=10&source=Mobile%20App&sentiment=Negative
```

**Response**:
```json
[
  {
    "id": 1,
    "feedback_id": "F001",
    "text": "The app crashes every time I try to login",
    "source": "Mobile App",
    "date": "2025-12-28",
    "sentiment": "Negative",
    "sentiment_score": 0.92,
    "intent": "Bug Report",
    "intent_score": 0.88,
    "created_at": "2026-01-01 23:00:00"
  }
]
```

#### 4. Get Analytics Summary

```http
GET /api/analytics/summary
```

**Response**:
```json
{
  "total_feedback": 100,
  "avg_sentiment_score": 0.65,
  "top_intent": "Bug Report",
  "sentiment_distribution": {
    "Positive": 35,
    "Neutral": 30,
    "Negative": 35
  },
  "intent_distribution": {
    "Bug Report": 25,
    "Feature Request": 20,
    "Performance Issue": 18,
    "General Feedback": 22,
    "Pricing Issue": 15
  },
  "source_distribution": {
    "Mobile App": 60,
    "Web": 25,
    "Support": 15
  }
}
```

#### 5. Bulk Upload

```http
POST /api/feedback/bulk
Content-Type: application/json

{
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
```

### All Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/api/feedback/add` | Add single feedback |
| POST | `/api/feedback/bulk` | Bulk upload |
| POST | `/api/analyze` | Analyze text |
| POST | `/api/feedback/analyze/{id}` | Analyze stored feedback |
| POST | `/api/feedback/analyze-all` | Analyze all unprocessed |
| GET | `/api/feedback/all` | Get all feedback (with filters) |
| GET | `/api/feedback/{id}` | Get specific feedback |
| GET | `/api/analytics/summary` | Get analytics summary |
| GET | `/api/analytics/trends` | Get trends over time |
| GET | `/api/analytics/negative-feedback` | Get negative feedback |

---

## 🤖 Model Details

### Sentiment Analysis Model (Bi-LSTM)

#### Architecture

```
Input Text
    ↓
Embedding Layer (vocab_size × 128)
    ↓
Bidirectional LSTM (64 units) + Dropout (0.3)
    ↓
Bidirectional LSTM (32 units) + Dropout (0.3)
    ↓
Dense Layer (64 units, ReLU) + Dropout (0.2)
    ↓
Output Layer (3 units, Softmax)
    ↓
[Positive, Neutral, Negative]
```

#### Training Details

- **Training Samples**: ~270 (expanded to ~810 with variations)
- **Validation Split**: 20%
- **Epochs**: 15
- **Batch Size**: 32
- **Optimizer**: Adam
- **Loss Function**: Sparse Categorical Crossentropy
- **Max Sequence Length**: 100 tokens
- **Vocabulary Size**: 10,000 words

#### Performance

- **Training Accuracy**: 85-90%
- **Validation Accuracy**: 85-90%
- **Inference Time**: <50ms per sample

### Intent Classification Model (LSTM)

#### Architecture

```
Input Text
    ↓
Embedding Layer (vocab_size × 128)
    ↓
LSTM (128 units) + Dropout (0.3)
    ↓
LSTM (64 units) + Dropout (0.3)
    ↓
Dense Layer (64 units, ReLU) + Dropout (0.2)
    ↓
Output Layer (5 units, Softmax)
    ↓
[Bug Report, Feature Request, Performance Issue, Pricing Issue, General Feedback]
```

#### Training Details

- **Training Samples**: ~375 (expanded to ~1125 with variations)
- **Validation Split**: 20%
- **Epochs**: 15
- **Batch Size**: 32
- **Classes**: 5 intent categories

#### Performance

- **Training Accuracy**: 80-85%
- **Validation Accuracy**: 80-85%
- **Inference Time**: <50ms per sample

### NLP Preprocessing Pipeline

1. **Text Cleaning**
   - Lowercase conversion
   - URL removal
   - Email removal
   - Special character removal

2. **Tokenization**
   - NLTK word tokenizer
   - Handles punctuation

3. **Stopword Removal**
   - Removes common words
   - Preserves sentiment words (not, never, very, etc.)

4. **Lemmatization**
   - Converts words to base form
   - "running" → "run"

5. **Vectorization**
   - Keras Tokenizer
   - Sequence padding to fixed length

---

## 📊 Dashboard Features

### Page 1: Dashboard (Overview)

**Key Metrics Cards**:
- Total Feedback Count
- Average Sentiment Score
- Top Intent Category
- Negative Feedback Count

**Visualizations**:
- 🥧 Sentiment Distribution (Pie Chart)
- 📊 Feedback by Source (Bar Chart)
- 📈 Intent Classification Breakdown (Horizontal Bar Chart)
- 📋 Recent Feedback Table

### Page 2: Deep Dive Analysis

**Features**:
- Advanced filtering (Source, Sentiment, Limit)
- ☁️ Word Cloud visualization
- 📅 Sentiment Trends Over Time (Line Chart)
- 🔍 Text search functionality
- 📥 CSV export

### Page 3: Add Feedback

**Two Modes**:
1. **Manual Entry**: Form with fields for ID, text, source, date
2. **CSV Upload**: Bulk upload with preview

### Page 4: Live Analyzer

**Real-time Analysis**:
- Text input area
- Instant sentiment + intent prediction
- Confidence scores with progress bars
- Color-coded results

### Page 5: Settings

**Information**:
- System status
- API health check
- Database statistics
- About section
- API documentation link

---

## 📈 Performance Metrics

### Model Accuracy

| Model | Training Accuracy | Validation Accuracy | Inference Time |
|-------|------------------|---------------------|----------------|
| Sentiment (Bi-LSTM) | 85-90% | 85-90% | <50ms |
| Intent (LSTM) | 80-85% | 80-85% | <50ms |

### API Performance

- **Average Response Time**: <100ms
- **Concurrent Requests**: Supports async processing
- **Database Queries**: Optimized with indexing

### System Requirements

- **RAM**: 2-4GB during training, 1-2GB during inference
- **Storage**: ~500MB (models + dependencies)
- **CPU**: Any modern processor (GPU not required)

---

## 🎬 Demo Workflow

### Complete End-to-End Demo

1. **Start Services** (2 terminals)
   ```bash
   # Terminal 1
   python backend/main.py
   
   # Terminal 2
   streamlit run streamlit_app/dashboard.py
   ```

2. **Upload Sample Data**
   - Open http://localhost:8501
   - Go to "📝 Add Feedback" → "📤 CSV Upload"
   - Upload `data/sample_feedback.csv`
   - Click "Upload Feedback"

3. **Analyze Feedback**
   - Sidebar → "🔄 Analyze All Feedback"
   - Wait for analysis to complete

4. **View Dashboard**
   - Navigate to "📈 Dashboard"
   - See sentiment distribution, source breakdown, intent classification

5. **Deep Dive**
   - Go to "🔍 Deep Dive"
   - View word cloud
   - Check sentiment trends
   - Filter by source/sentiment

6. **Live Analysis**
   - Navigate to "💬 Live Analyzer"
   - Enter: "The app is slow and crashes frequently"
   - Click "Analyze"
   - See: Sentiment = Negative, Intent = Performance Issue/Bug Report

7. **API Testing**
   - Open http://localhost:8000/docs
   - Try POST `/api/analyze` with sample text
   - View response with sentiment + intent

---

## 🔧 Troubleshooting

### Issue: Models Not Found

**Error**: `Models not found! Please run 'python ml/train_models.py'`

**Solution**:
```bash
python ml/train_models.py
```

### Issue: API Not Running

**Error**: Dashboard shows "API Server is not running!"

**Solution**:
1. Check if Terminal 1 is running `python backend/main.py`
2. Verify no errors in Terminal 1
3. Check http://localhost:8000/health

### Issue: NLTK Data Not Found

**Error**: `LookupError: Resource punkt not found`

**Solution**:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```

### Issue: Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Change port in config.py
API_PORT = 8001  # Instead of 8000
```

### Issue: TensorFlow Warnings

**Warning**: Various TensorFlow warnings during training

**Solution**: These are normal and can be ignored. Models will still train successfully.

---

## 🚀 Future Enhancements

### Planned Features

1. **Advanced Models**
   - BERT-based sentiment analysis
   - Multi-label intent classification
   - Emotion detection (happy, angry, sad, etc.)

2. **Enhanced Dashboard**
   - Real-time updates with WebSockets
   - Exportable reports (PDF)
   - Custom date range filtering

3. **Deployment**
   - Docker containerization
   - Cloud deployment (AWS/GCP/Azure)
   - CI/CD pipeline

4. **Database**
   - PostgreSQL support for production
   - Data backup and recovery
   - Migration scripts

5. **Authentication**
   - User authentication
   - Role-based access control
   - API key management

6. **Integrations**
   - Email notifications for negative feedback
   - Slack/Teams integration
   - Webhook support

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Created as a portfolio project demonstrating:
- ✅ NLP expertise
- ✅ Deep Learning implementation
- ✅ Backend engineering (FastAPI)
- ✅ Data visualization & storytelling
- ✅ Full-stack development

---

## 🙏 Acknowledgments

- **TensorFlow/Keras**: Deep learning framework
- **FastAPI**: Modern web framework
- **Streamlit**: Dashboard framework
- **spaCy & NLTK**: NLP libraries

---

<div align="center">

**Made with ❤️ and 🤖 AI**

[⬆ Back to Top](#-smart-customer-feedback-intelligence-platform-scfip)

</div>
