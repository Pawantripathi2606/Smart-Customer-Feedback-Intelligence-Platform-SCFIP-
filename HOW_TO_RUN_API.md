# 🚀 How to Run the API - Terminal Commands

## ✅ Prerequisites
- Virtual environment activated
- Dependencies installed
- Models trained

---

## 🔥 Start the Backend API

### Option 1: Using Python directly (Recommended)

```bash
# Navigate to project directory
cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"

# Activate virtual environment
venv\Scripts\activate

# Run the backend
python backend/main.py
```

### Option 2: Using Uvicorn directly

```bash
# Navigate to project directory
cd "C:\Users\Lenovo\Desktop\Smart Customer Feedback Intelligence Platform (SCFIP)"

# Activate virtual environment
venv\Scripts\activate

# Run with uvicorn
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Using the helper script (Easiest!)

```bash
# Just double-click or run:
run_backend.bat
```

---

## ✅ Expected Output

When the API starts successfully, you should see:

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

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 🌐 Access the API

Once running, you can access:

- **API Base**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 🧪 Test the API

### Method 1: Browser (Easiest)

1. Open http://localhost:8000/docs
2. Click on `POST /api/analyze`
3. Click "Try it out"
4. Enter:
   ```json
   {
     "text": "The app crashes after login"
   }
   ```
5. Click "Execute"
6. See the result!

### Method 2: Command Line (curl)

```bash
# Test analyze endpoint
curl -X POST "http://localhost:8000/api/analyze" ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"The app crashes after login\"}"

# Test health endpoint
curl http://localhost:8000/health

# Test analytics
curl http://localhost:8000/api/analytics/summary
```

### Method 3: Python Script

```python
import requests

# Analyze text
response = requests.post(
    "http://localhost:8000/api/analyze",
    json={"text": "The app is slow and buggy"}
)
print(response.json())
```

---

## 🛑 Stop the API

Press `Ctrl+C` in the terminal where the API is running.

---

## 🔄 Common Commands

| Task | Command |
|------|---------|
| Start API | `python backend/main.py` |
| Start API (uvicorn) | `uvicorn backend.main:app --reload` |
| Start Dashboard | `streamlit run streamlit_app/dashboard.py` |
| Train Models | `python ml/train_models.py` |
| Test API | Open http://localhost:8000/docs |

---

## ❌ Troubleshooting

### Error: "Models not found"
```bash
python ml/train_models.py
```

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"
```bash
# Find and kill the process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Error: "Virtual environment not activated"
```bash
venv\Scripts\activate
```

---

## 📚 More Information

- **Full Documentation**: README.md
- **Quick Start Guide**: QUICKSTART.md
- **API Reference**: API_GUIDE.md

---

**Pro Tip**: Use `run_backend.bat` and `run_dashboard.bat` for the easiest startup experience!
