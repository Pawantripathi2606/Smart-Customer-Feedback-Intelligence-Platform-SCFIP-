# 🚀 Quick Start Guide - Smart Customer Feedback Intelligence Platform

## Prerequisites
- Python 3.9+ installed
- Virtual environment activated

---

## ⚡ Quick Setup (First Time Only)

### Step 1: Activate Virtual Environment
```bash
# Navigate to project directory
cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"

# Activate virtual environment
venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```

### Step 4: Train Models (5-10 minutes)
```bash
python ml/train_models.py
```

**Expected Output:**
```
============================================================
TRAINING SENTIMENT MODEL (Bi-LSTM)
============================================================
Epoch 1/15
...
Epoch 15/15
Training Accuracy: 0.8750
Validation Accuracy: 0.8500

============================================================
TRAINING INTENT MODEL (LSTM)
============================================================
Epoch 1/15
...
Epoch 15/15
Training Accuracy: 0.8200
Validation Accuracy: 0.8000

Models trained and saved successfully!
```

---

## 🔥 Running the Application

### Method 1: Run Backend API

**Terminal 1 - Start FastAPI Backend:**
```bash
# Make sure you're in the project directory with venv activated
cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"
venv\Scripts\activate

# Run the backend
python backend/main.py
```

**Expected Output:**
```
============================================================
Starting Smart Customer Feedback Intelligence Platform
============================================================

Loading trained models...
Model loaded from ml\models\sentiment_model.h5
Tokenizer loaded from ml\models\tokenizer.pkl
Label encoder loaded from ml\models\label_encoders.pkl
Intent model loaded from ml\models\intent_model.h5

✓ Models loaded successfully!

============================================================
API Server Ready!
============================================================
Docs: http://localhost:8000/docs
============================================================

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **API is now running at:** http://localhost:8000  
✅ **API Documentation:** http://localhost:8000/docs

---

### Method 2: Run Streamlit Dashboard

**Terminal 2 - Start Streamlit Dashboard (keep Terminal 1 running):**
```bash
# Open a NEW terminal window
cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"
venv\Scripts\activate

# Run the dashboard
streamlit run streamlit_app/dashboard.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

✅ **Dashboard is now running at:** http://localhost:8501

---

## 🧪 Testing the API

### Option 1: Using Browser (Swagger UI)
1. Open http://localhost:8000/docs
2. Click on any endpoint (e.g., `POST /api/analyze`)
3. Click "Try it out"
4. Enter test data:
   ```json
   {
     "text": "The app crashes after login. Very frustrating!"
   }
   ```
5. Click "Execute"
6. View the response

### Option 2: Using curl (Command Line)

**Test 1: Analyze Text**
```bash
curl -X POST "http://localhost:8000/api/analyze" ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"The app crashes after login\"}"
```

**Expected Response:**
```json
{
  "text": "The app crashes after login",
  "sentiment": "Negative",
  "sentiment_score": 0.92,
  "intent": "Bug Report",
  "intent_score": 0.88
}
```

**Test 2: Add Feedback**
```bash
curl -X POST "http://localhost:8000/api/feedback/add" ^
  -H "Content-Type: application/json" ^
  -d "{\"feedback_id\": \"F101\", \"text\": \"Great app!\", \"source\": \"Mobile App\", \"date\": \"2026-01-01\"}"
```

**Test 3: Get Analytics**
```bash
curl "http://localhost:8000/api/analytics/summary"
```

### Option 3: Using Python

Create a test file `test_api.py`:
```python
import requests

BASE_URL = "http://localhost:8000"

# Test 1: Analyze text
print("Test 1: Analyzing text...")
response = requests.post(
    f"{BASE_URL}/api/analyze",
    json={"text": "The app is slow and crashes frequently"}
)
result = response.json()
print(f"Sentiment: {result['sentiment']} ({result['sentiment_score']:.2%})")
print(f"Intent: {result['intent']} ({result['intent_score']:.2%})")
print()

# Test 2: Add feedback
print("Test 2: Adding feedback...")
response = requests.post(
    f"{BASE_URL}/api/feedback/add",
    json={
        "feedback_id": "TEST001",
        "text": "Love the new features!",
        "source": "Mobile App",
        "date": "2026-01-01"
    }
)
print(response.json())
print()

# Test 3: Get analytics
print("Test 3: Getting analytics...")
response = requests.get(f"{BASE_URL}/api/analytics/summary")
analytics = response.json()
print(f"Total Feedback: {analytics['total_feedback']}")
print(f"Sentiment Distribution: {analytics['sentiment_distribution']}")
```

Run it:
```bash
python test_api.py
```

---

## 📊 Using the Dashboard

1. **Upload Sample Data:**
   - Go to "📝 Add Feedback" page
   - Click "📤 CSV Upload" tab
   - Upload `data/sample_feedback.csv`
   - Click "Upload Feedback"

2. **Analyze Feedback:**
   - Sidebar → Click "🔄 Analyze All Feedback"
   - Wait for processing

3. **View Analytics:**
   - Navigate to "📈 Dashboard"
   - See sentiment distribution, trends, and insights

4. **Live Analysis:**
   - Go to "💬 Live Analyzer"
   - Enter any text
   - Click "Analyze"
   - See instant results

---

## 🛑 Stopping the Services

### Stop Backend (Terminal 1):
Press `Ctrl+C`

### Stop Dashboard (Terminal 2):
Press `Ctrl+C`

---

## 🔄 Restarting the Application

**Every time you want to run the app:**

1. **Activate virtual environment:**
   ```bash
   cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"
   venv\Scripts\activate
   ```

2. **Start backend (Terminal 1):**
   ```bash
   python backend/main.py
   ```

3. **Start dashboard (Terminal 2):**
   ```bash
   streamlit run streamlit_app/dashboard.py
   ```

---

## 🐛 Common Issues

### Issue 1: "Models not found"
**Solution:**
```bash
python ml/train_models.py
```

### Issue 2: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue 3: "Port already in use"
**Solution:**
```bash
# Kill the process using the port or change port in config.py
# For port 8000:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue 4: "API not responding"
**Solution:**
1. Check if backend is running in Terminal 1
2. Visit http://localhost:8000/health
3. Check for errors in Terminal 1

---

## 📝 Quick Command Reference

| Task | Command |
|------|---------|
| Activate venv | `venv\Scripts\activate` |
| Install deps | `pip install -r requirements.txt` |
| Train models | `python ml/train_models.py` |
| Start backend | `python backend/main.py` |
| Start dashboard | `streamlit run streamlit_app/dashboard.py` |
| Test API | Open http://localhost:8000/docs |
| View dashboard | Open http://localhost:8501 |

---

## 🎯 API Endpoints Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check API status |
| `/api/analyze` | POST | Analyze text |
| `/api/feedback/add` | POST | Add feedback |
| `/api/feedback/all` | GET | Get all feedback |
| `/api/analytics/summary` | GET | Get analytics |

**Full API documentation:** http://localhost:8000/docs

---

## 💡 Tips

1. **Always activate virtual environment** before running commands
2. **Keep both terminals running** for full functionality
3. **Use Swagger UI** at /docs for easy API testing
4. **Check Terminal 1** for backend logs and errors
5. **Refresh dashboard** if data doesn't update immediately

---

## 📚 More Information

- **Full Documentation:** See README.md
- **API Guide:** See API_GUIDE.md
- **Project Walkthrough:** See walkthrough.md (in artifacts)

---

**Last Updated:** January 1, 2026
