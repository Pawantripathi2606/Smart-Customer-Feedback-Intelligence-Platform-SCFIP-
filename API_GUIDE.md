# API Usage Guide - Smart Customer Feedback Intelligence Platform

## Quick Reference

**Base URL**: `http://localhost:8000`  
**API Docs**: `http://localhost:8000/docs`  
**Health Check**: `http://localhost:8000/health`

---

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

---

## Endpoints Overview

### 1. Health & Status

#### GET `/health`
Check if the API and models are loaded.

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": true,
  "database": "connected"
}
```

---

### 2. Feedback Management

#### POST `/api/feedback/add`
Add a single feedback entry.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/feedback/add" \
  -H "Content-Type: application/json" \
  -d '{
    "feedback_id": "F101",
    "text": "The app crashes after login",
    "source": "Mobile App",
    "date": "2026-01-01"
  }'
```

**Response:**
```json
{
  "message": "Feedback F101 added successfully",
  "success": true
}
```

**Parameters:**
- `feedback_id` (string, required): Unique identifier
- `text` (string, required): Feedback content
- `source` (string, required): "Mobile App", "Web", or "Support"
- `date` (string, required): Date in YYYY-MM-DD format

---

#### POST `/api/feedback/bulk`
Upload multiple feedback entries at once.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/feedback/bulk" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

**Response:**
```json
{
  "message": "Added 2 feedback entries. 0 duplicates skipped.",
  "success": true
}
```

---

#### GET `/api/feedback/all`
Retrieve all feedback with optional filters.

**Request:**
```bash
# Get all feedback
curl "http://localhost:8000/api/feedback/all"

# With filters
curl "http://localhost:8000/api/feedback/all?limit=10&source=Mobile%20App&sentiment=Negative"
```

**Query Parameters:**
- `limit` (integer, optional): Maximum number of results
- `source` (string, optional): Filter by source
- `sentiment` (string, optional): Filter by sentiment

**Response:**
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

---

#### GET `/api/feedback/{feedback_id}`
Get a specific feedback entry.

**Request:**
```bash
curl "http://localhost:8000/api/feedback/F001"
```

**Response:**
```json
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
```

---

### 3. Analysis

#### POST `/api/analyze`
Analyze any text for sentiment and intent.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The app crashes after login. Very frustrating!"
  }'
```

**Response:**
```json
{
  "text": "The app crashes after login. Very frustrating!",
  "sentiment": "Negative",
  "sentiment_score": 0.95,
  "intent": "Bug Report",
  "intent_score": 0.89
}
```

**Sentiment Classes:**
- `Positive`: Happy, satisfied feedback
- `Neutral`: Neutral or mixed feedback
- `Negative`: Unhappy, dissatisfied feedback

**Intent Classes:**
- `Bug Report`: Technical issues, crashes, errors
- `Feature Request`: Requests for new features
- `Performance Issue`: Speed, lag, battery drain
- `Pricing Issue`: Cost, subscription concerns
- `General Feedback`: General comments

---

#### POST `/api/feedback/analyze/{feedback_id}`
Analyze a specific feedback entry already in the database.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/feedback/analyze/F001"
```

**Response:**
```json
{
  "message": "Feedback F001 analyzed and updated successfully",
  "success": true
}
```

---

#### POST `/api/feedback/analyze-all`
Analyze all unprocessed feedback in the database.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/feedback/analyze-all"
```

**Response:**
```json
{
  "message": "Analyzed 100 feedback entries",
  "success": true
}
```

---

### 4. Analytics

#### GET `/api/analytics/summary`
Get aggregated analytics and insights.

**Request:**
```bash
curl "http://localhost:8000/api/analytics/summary"
```

**Response:**
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

---

#### GET `/api/analytics/trends`
Get feedback trends over time.

**Request:**
```bash
curl "http://localhost:8000/api/analytics/trends"
```

**Response:**
```json
{
  "trends": [
    {
      "date": "2025-12-28",
      "sentiment": "Positive",
      "count": 5
    },
    {
      "date": "2025-12-28",
      "sentiment": "Negative",
      "count": 3
    }
  ]
}
```

---

#### GET `/api/analytics/negative-feedback`
Get most recent negative feedback.

**Request:**
```bash
curl "http://localhost:8000/api/analytics/negative-feedback?limit=5"
```

**Query Parameters:**
- `limit` (integer, optional): Number of results (default: 10)

**Response:**
```json
[
  {
    "id": 1,
    "feedback_id": "F001",
    "text": "The app crashes every time",
    "sentiment": "Negative",
    "intent": "Bug Report",
    ...
  }
]
```

---

## Python Examples

### Using `requests` library

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Add feedback
response = requests.post(
    f"{BASE_URL}/api/feedback/add",
    json={
        "feedback_id": "F101",
        "text": "Great app!",
        "source": "Mobile App",
        "date": "2026-01-01"
    }
)
print(response.json())

# 2. Analyze text
response = requests.post(
    f"{BASE_URL}/api/analyze",
    json={"text": "The app is slow and buggy"}
)
result = response.json()
print(f"Sentiment: {result['sentiment']}")
print(f"Intent: {result['intent']}")

# 3. Get analytics
response = requests.get(f"{BASE_URL}/api/analytics/summary")
analytics = response.json()
print(f"Total Feedback: {analytics['total_feedback']}")
print(f"Sentiment Distribution: {analytics['sentiment_distribution']}")

# 4. Get all feedback with filters
response = requests.get(
    f"{BASE_URL}/api/feedback/all",
    params={"source": "Mobile App", "limit": 10}
)
feedbacks = response.json()
for feedback in feedbacks:
    print(f"{feedback['feedback_id']}: {feedback['text']}")
```

---

## JavaScript Examples

### Using `fetch` API

```javascript
const BASE_URL = "http://localhost:8000";

// 1. Add feedback
async function addFeedback() {
  const response = await fetch(`${BASE_URL}/api/feedback/add`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      feedback_id: "F101",
      text: "Great app!",
      source: "Mobile App",
      date: "2026-01-01"
    })
  });
  const data = await response.json();
  console.log(data);
}

// 2. Analyze text
async function analyzeText(text) {
  const response = await fetch(`${BASE_URL}/api/analyze`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text})
  });
  const result = await response.json();
  console.log(`Sentiment: ${result.sentiment}`);
  console.log(`Intent: ${result.intent}`);
}

// 3. Get analytics
async function getAnalytics() {
  const response = await fetch(`${BASE_URL}/api/analytics/summary`);
  const analytics = await response.json();
  console.log(analytics);
}

// Usage
addFeedback();
analyzeText("The app crashes frequently");
getAnalytics();
```

---

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Feedback with ID F101 already exists"
}
```

#### 404 Not Found
```json
{
  "detail": "Feedback with ID F999 not found"
}
```

#### 503 Service Unavailable
```json
{
  "detail": "Models not trained yet. Please run 'python ml/train_models.py' first."
}
```

### Error Handling Example

```python
import requests

try:
    response = requests.post(
        "http://localhost:8000/api/analyze",
        json={"text": "Sample feedback"}
    )
    response.raise_for_status()  # Raises HTTPError for bad status
    result = response.json()
    print(result)
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e.response.status_code}")
    print(f"Detail: {e.response.json()['detail']}")
except requests.exceptions.ConnectionError:
    print("Error: Cannot connect to API. Is the server running?")
```

---

## Rate Limiting

Currently, there are no rate limits. In production, consider implementing rate limiting to prevent abuse.

---

## Best Practices

1. **Always validate input**: Ensure feedback_id is unique before adding
2. **Handle errors gracefully**: Check response status codes
3. **Use bulk upload**: For large datasets, use `/api/feedback/bulk`
4. **Analyze in batches**: Use `/api/feedback/analyze-all` instead of individual calls
5. **Cache analytics**: Analytics data doesn't change frequently

---

## Testing with Swagger UI

1. Open http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"
6. View response

---

## Integration Examples

### Integrating with a Web Form

```html
<!DOCTYPE html>
<html>
<head>
    <title>Feedback Form</title>
</head>
<body>
    <form id="feedbackForm">
        <input type="text" id="feedbackId" placeholder="Feedback ID" required>
        <textarea id="feedbackText" placeholder="Your feedback" required></textarea>
        <select id="source">
            <option value="Mobile App">Mobile App</option>
            <option value="Web">Web</option>
            <option value="Support">Support</option>
        </select>
        <button type="submit">Submit</button>
    </form>

    <div id="result"></div>

    <script>
        document.getElementById('feedbackForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const feedback = {
                feedback_id: document.getElementById('feedbackId').value,
                text: document.getElementById('feedbackText').value,
                source: document.getElementById('source').value,
                date: new Date().toISOString().split('T')[0]
            };

            try {
                const response = await fetch('http://localhost:8000/api/feedback/add', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(feedback)
                });
                
                const result = await response.json();
                document.getElementById('result').textContent = result.message;
            } catch (error) {
                document.getElementById('result').textContent = 'Error: ' + error.message;
            }
        });
    </script>
</body>
</html>
```

---

## Support

For issues or questions:
1. Check the main README.md
2. Review the Swagger documentation at /docs
3. Check the troubleshooting section in README.md

---

**Last Updated**: January 1, 2026
