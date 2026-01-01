# 🚀 Complete Terminal Commands Reference

## ✅ **Your Backend is NOW RUNNING!**

The FastAPI backend is currently running at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📋 **Complete Setup Commands (First Time Only)**

Run these commands **ONCE** when setting up the project for the first time:

### **Step 1: Navigate to Project**
```powershell
cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"
```

### **Step 2: Activate Virtual Environment**
```powershell
venv\Scripts\activate
```

### **Step 3: Download NLTK Data** ✅ (Already Done!)
```powershell
python download_nltk_data.py
```

### **Step 4: Train ML Models** ✅ (Already Done!)
```powershell
python ml\train_models.py
```

**Training Time**: ~2-5 minutes  
**Output**: Models saved to `ml\models\` directory

---

## 🔥 **Daily Usage Commands**

Use these commands **every time** you want to run the project:

### **Terminal 1 - Start Backend API** ✅ (Currently Running!)

```powershell
cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"
venv\Scripts\activate
python backend\main.py
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

INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

✅ **Backend URL**: http://localhost:8000  
✅ **API Documentation**: http://localhost:8000/docs

---

### **Terminal 2 - Start Streamlit Dashboard** (Open a NEW terminal)

```powershell
cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"
venv\Scripts\activate
streamlit run streamlit_app\dashboard.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

✅ **Dashboard URL**: http://localhost:8501

---

## 🧪 **Testing the API**

### **Option 1: Using Browser (Swagger UI)**
1. Open http://localhost:8000/docs
2. Click on any endpoint (e.g., `POST /api/analyze`)
3. Click **"Try it out"**
4. Enter test data:
   ```json
   {
     "text": "The app crashes after login. Very frustrating!"
   }
   ```
5. Click **"Execute"**
6. View the response

---

### **Option 2: Using PowerShell (curl)**

**Test 1: Health Check**
```powershell
curl http://localhost:8000/health
```

**Test 2: Analyze Text**
```powershell
curl -X POST "http://localhost:8000/api/analyze" `
  -H "Content-Type: application/json" `
  -d '{\"text\": \"The app crashes after login\"}'
```

**Test 3: Get Analytics Summary**
```powershell
curl http://localhost:8000/api/analytics/summary
```

**Test 4: Add Feedback**
```powershell
curl -X POST "http://localhost:8000/api/feedback/add" `
  -H "Content-Type: application/json" `
  -d '{\"feedback_id\": \"F101\", \"text\": \"Great app!\", \"source\": \"Mobile App\", \"date\": \"2026-01-01\"}'
```

---

### **Option 3: Using Python Script**

Create a file `test_api.py`:
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
```powershell
python test_api.py
```

---

## 📊 **Using the Streamlit Dashboard**

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

## 🛑 **Stopping the Services**

### **Stop Backend (Terminal 1):**
Press `Ctrl+C`

### **Stop Dashboard (Terminal 2):**
Press `Ctrl+C`

---

## 🔄 **Quick Restart Commands**

If you need to restart the services:

**Terminal 1 (Backend):**
```powershell
cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"
venv\Scripts\activate
python backend\main.py
```

**Terminal 2 (Dashboard):**
```powershell
cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"
venv\Scripts\activate
streamlit run streamlit_app\dashboard.py
```

---

## 📚 **All Available API Endpoints**

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

## 🐛 **Troubleshooting**

### **Issue: Models not found**
**Solution:**
```powershell
python ml\train_models.py
```

### **Issue: NLTK data not found**
**Solution:**
```powershell
python download_nltk_data.py
```

### **Issue: Module not found**
**Solution:**
```powershell
pip install -r requirements.txt
```

### **Issue: Port already in use**
**Solution:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace <PID> with actual process ID)
taskkill /PID <PID> /F
```

---

## 📊 **Summary of URLs**

| Service | URL |
|---------|-----|
| **Backend API** | http://localhost:8000 |
| **API Documentation (Swagger)** | http://localhost:8000/docs |
| **API Documentation (ReDoc)** | http://localhost:8000/redoc |
| **Streamlit Dashboard** | http://localhost:8501 |
| **Health Check** | http://localhost:8000/health |

---

## ✅ **Current Status**

- ✅ Virtual environment created
- ✅ Dependencies installed
- ✅ NLTK data downloaded
- ✅ ML models trained
- ✅ **Backend API is RUNNING** at http://localhost:8000
- ⏳ Dashboard needs to be started in Terminal 2

---

## 🎯 **Next Steps**

1. **Open a NEW terminal window** (Terminal 2)
2. **Run the dashboard:**
   ```powershell
   cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"
   venv\Scripts\activate
   streamlit run streamlit_app\dashboard.py
   ```
3. **Open your browser:**
   - Dashboard: http://localhost:8501
   - API Docs: http://localhost:8000/docs

---

**Last Updated:** January 1, 2026  
**Status:** ✅ Backend Running | ⏳ Dashboard Pending
