import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="Customer Feedback Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Base URL
API_BASE_URL = "http://localhost:8000/api"

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions
def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_analytics_summary():
    """Fetch analytics summary from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/summary")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_all_feedback(source=None, sentiment=None, limit=None):
    """Fetch all feedback with optional filters"""
    try:
        params = {}
        if source:
            params['source'] = source
        if sentiment:
            params['sentiment'] = sentiment
        if limit:
            params['limit'] = limit
        
        response = requests.get(f"{API_BASE_URL}/feedback/all", params=params)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def analyze_text(text):
    """Analyze text using API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json={"text": text}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def add_feedback(feedback_data):
    """Add new feedback via API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/feedback/add",
            json=feedback_data
        )
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"message": str(e)}

def analyze_all_feedback():
    """Trigger analysis of all feedback"""
    try:
        response = requests.post(f"{API_BASE_URL}/feedback/analyze-all")
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"message": str(e)}

def upload_csv_feedback(df):
    """Upload CSV feedback data"""
    try:
        feedbacks = df.to_dict('records')
        response = requests.post(
            f"{API_BASE_URL}/feedback/bulk",
            json={"feedbacks": feedbacks}
        )
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"message": str(e)}

# Main App
def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Smart Customer Feedback Intelligence Platform</h1>', 
                unsafe_allow_html=True)
    
    # Check API status
    api_status = check_api_health()
    
    if not api_status:
        st.error("⚠️ **API Server is not running!**")
        st.info("Please start the FastAPI server first:")
        st.code("python backend/main.py", language="bash")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=80)
        st.title("Navigation")
        
        page = st.radio(
            "Select Page",
            ["📈 Dashboard", "🔍 Deep Dive", "📝 Add Feedback", "💬 Live Analyzer", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        st.subheader("Quick Actions")
        if st.button("🔄 Analyze All Feedback", use_container_width=True):
            with st.spinner("Analyzing all feedback..."):
                success, result = analyze_all_feedback()
                if success:
                    st.success(result.get('message', 'Analysis complete!'))
                else:
                    st.error(f"Error: {result.get('message', 'Unknown error')}")
        
        st.divider()
        st.caption("Powered by AI & Deep Learning")
    
    # Page routing
    if page == "📈 Dashboard":
        show_dashboard()
    elif page == "🔍 Deep Dive":
        show_deep_dive()
    elif page == "📝 Add Feedback":
        show_add_feedback()
    elif page == "💬 Live Analyzer":
        show_live_analyzer()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """Main dashboard with overview metrics and visualizations"""
    st.header("📈 Analytics Dashboard")
    
    # Fetch data
    analytics = get_analytics_summary()
    
    if not analytics:
        st.warning("No data available. Please add feedback first.")
        return
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Feedback",
            value=analytics['total_feedback'],
            delta=None
        )
    
    with col2:
        avg_score = analytics['avg_sentiment_score']
        st.metric(
            label="😊 Avg Sentiment Score",
            value=f"{avg_score:.2f}",
            delta=f"{(avg_score - 0.5) * 100:.1f}%" if avg_score else None
        )
    
    with col3:
        st.metric(
            label="🎯 Top Intent",
            value=analytics['top_intent'],
            delta=None
        )
    
    with col4:
        sentiment_dist = analytics.get('sentiment_distribution', {})
        negative_count = sentiment_dist.get('Negative', 0)
        st.metric(
            label="⚠️ Negative Feedback",
            value=negative_count,
            delta=f"-{negative_count}" if negative_count > 0 else "0",
            delta_color="inverse"
        )
    
    st.divider()
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sentiment Distribution")
        sentiment_dist = analytics.get('sentiment_distribution', {})
        
        if sentiment_dist:
            fig = px.pie(
                values=list(sentiment_dist.values()),
                names=list(sentiment_dist.keys()),
                color=list(sentiment_dist.keys()),
                color_discrete_map={
                    'Positive': '#2ecc71',
                    'Neutral': '#f39c12',
                    'Negative': '#e74c3c'
                },
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sentiment data available")
    
    with col2:
        st.subheader("Feedback by Source")
        source_dist = analytics.get('source_distribution', {})
        
        if source_dist:
            fig = px.bar(
                x=list(source_dist.keys()),
                y=list(source_dist.values()),
                color=list(source_dist.values()),
                color_continuous_scale='Blues',
                labels={'x': 'Source', 'y': 'Count'}
            )
            fig.update_layout(
                showlegend=False,
                height=400,
                xaxis_title="Source",
                yaxis_title="Feedback Count"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No source data available")
    
    st.divider()
    
    # Intent Distribution
    st.subheader("Intent Classification Breakdown")
    intent_dist = analytics.get('intent_distribution', {})
    
    if intent_dist:
        # Sort by count
        sorted_intents = dict(sorted(intent_dist.items(), key=lambda x: x[1], reverse=True))
        
        fig = px.bar(
            x=list(sorted_intents.values()),
            y=list(sorted_intents.keys()),
            orientation='h',
            color=list(sorted_intents.values()),
            color_continuous_scale='Viridis',
            labels={'x': 'Count', 'y': 'Intent'}
        )
        fig.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Feedback Count",
            yaxis_title="Intent Category"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No intent data available")
    
    # Recent Feedback Table
    st.divider()
    st.subheader("📋 Recent Feedback")
    
    recent_feedback = get_all_feedback(limit=10)
    
    if recent_feedback:
        df = pd.DataFrame(recent_feedback)
        
        # Select and reorder columns
        display_cols = ['feedback_id', 'text', 'source', 'sentiment', 'intent', 'date']
        available_cols = [col for col in display_cols if col in df.columns]
        
        st.dataframe(
            df[available_cols],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No feedback available")

def show_deep_dive():
    """Deep dive analysis with word clouds and detailed filtering"""
    st.header("🔍 Deep Dive Analysis")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        source_filter = st.selectbox(
            "Filter by Source",
            ["All", "Mobile App", "Web", "Support"]
        )
    
    with col2:
        sentiment_filter = st.selectbox(
            "Filter by Sentiment",
            ["All", "Positive", "Neutral", "Negative"]
        )
    
    with col3:
        limit = st.number_input("Max Results", min_value=10, max_value=1000, value=100)
    
    # Fetch filtered data
    source = None if source_filter == "All" else source_filter
    sentiment = None if sentiment_filter == "All" else sentiment_filter
    
    feedback_data = get_all_feedback(source=source, sentiment=sentiment, limit=limit)
    
    if not feedback_data:
        st.warning("No feedback matches the selected filters.")
        return
    
    df = pd.DataFrame(feedback_data)
    
    st.success(f"Found {len(df)} feedback entries")
    
    # Word Cloud
    st.subheader("☁️ Word Cloud")
    
    if 'text' in df.columns and len(df) > 0:
        all_text = ' '.join(df['text'].astype(str).tolist())
        
        wordcloud = WordCloud(
            width=1200,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=100
        ).generate(all_text)
        
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    
    st.divider()
    
    # Sentiment over time
    if 'date' in df.columns and 'sentiment' in df.columns:
        st.subheader("📅 Sentiment Trends Over Time")
        
        # Group by date and sentiment
        trend_df = df.groupby(['date', 'sentiment']).size().reset_index(name='count')
        
        fig = px.line(
            trend_df,
            x='date',
            y='count',
            color='sentiment',
            color_discrete_map={
                'Positive': '#2ecc71',
                'Neutral': '#f39c12',
                'Negative': '#e74c3c'
            },
            markers=True
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Feedback Count",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Detailed Table
    st.subheader("📊 Detailed Feedback Table")
    
    # Add search
    search_term = st.text_input("🔎 Search in feedback text")
    
    if search_term:
        df = df[df['text'].str.contains(search_term, case=False, na=False)]
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"feedback_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

def show_add_feedback():
    """Page for adding new feedback"""
    st.header("📝 Add Customer Feedback")
    
    tab1, tab2 = st.tabs(["✍️ Manual Entry", "📤 CSV Upload"])
    
    with tab1:
        st.subheader("Add Single Feedback")
        
        with st.form("feedback_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                feedback_id = st.text_input("Feedback ID*", placeholder="e.g., F101")
                source = st.selectbox("Source*", ["Mobile App", "Web", "Support"])
            
            with col2:
                date = st.date_input("Date*", value=datetime.now())
            
            text = st.text_area(
                "Feedback Text*",
                placeholder="Enter customer feedback here...",
                height=150
            )
            
            submitted = st.form_submit_button("➕ Add Feedback", use_container_width=True)
            
            if submitted:
                if not feedback_id or not text:
                    st.error("Please fill in all required fields (marked with *)")
                else:
                    feedback_data = {
                        "feedback_id": feedback_id,
                        "text": text,
                        "source": source,
                        "date": str(date)
                    }
                    
                    success, result = add_feedback(feedback_data)
                    
                    if success:
                        st.success(f"✅ {result.get('message', 'Feedback added successfully!')}")
                    else:
                        st.error(f"❌ {result.get('detail', 'Error adding feedback')}")
    
    with tab2:
        st.subheader("Upload CSV File")
        
        st.info("📋 CSV should have columns: feedback_id, text, source, date")
        
        # Show example
        with st.expander("View CSV Format Example"):
            example_df = pd.DataFrame({
                'feedback_id': ['F101', 'F102'],
                'text': ['Great app!', 'App crashes frequently'],
                'source': ['Mobile App', 'Web'],
                'date': ['2026-01-01', '2026-01-01']
            })
            st.dataframe(example_df)
        
        uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                st.write("Preview:")
                st.dataframe(df.head(), use_container_width=True)
                
                if st.button("📤 Upload Feedback", use_container_width=True):
                    with st.spinner("Uploading feedback..."):
                        success, result = upload_csv_feedback(df)
                        
                        if success:
                            st.success(f"✅ {result.get('message', 'Upload successful!')}")
                        else:
                            st.error(f"❌ {result.get('message', 'Upload failed')}")
            
            except Exception as e:
                st.error(f"Error reading CSV: {e}")

def show_live_analyzer():
    """Live text analysis tool"""
    st.header("💬 Live Feedback Analyzer")
    
    st.write("Analyze any text in real-time using our AI models")
    
    text_input = st.text_area(
        "Enter feedback text to analyze:",
        placeholder="Type or paste customer feedback here...",
        height=150
    )
    
    if st.button("🔍 Analyze", use_container_width=True, type="primary"):
        if not text_input:
            st.warning("Please enter some text to analyze")
        else:
            with st.spinner("Analyzing..."):
                result = analyze_text(text_input)
                
                if result:
                    st.success("Analysis Complete!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("😊 Sentiment Analysis")
                        sentiment = result['sentiment']
                        score = result['sentiment_score']
                        
                        # Color based on sentiment
                        color = {
                            'Positive': 'green',
                            'Neutral': 'orange',
                            'Negative': 'red'
                        }.get(sentiment, 'gray')
                        
                        st.markdown(f"### :{color}[{sentiment}]")
                        st.progress(score)
                        st.caption(f"Confidence: {score:.2%}")
                    
                    with col2:
                        st.subheader("🎯 Intent Classification")
                        intent = result['intent']
                        intent_score = result['intent_score']
                        
                        st.markdown(f"### {intent}")
                        st.progress(intent_score)
                        st.caption(f"Confidence: {intent_score:.2%}")
                    
                    # Original text
                    st.divider()
                    st.subheader("Original Text")
                    st.info(text_input)
                else:
                    st.error("Analysis failed. Please ensure the API and models are running.")

def show_settings():
    """Settings and system information"""
    st.header("⚙️ Settings & Information")
    
    st.subheader("System Status")
    
    # API Health
    api_healthy = check_api_health()
    st.metric("API Status", "🟢 Online" if api_healthy else "🔴 Offline")
    
    # Database info
    analytics = get_analytics_summary()
    if analytics:
        st.metric("Database Records", analytics['total_feedback'])
    
    st.divider()
    
    st.subheader("About")
    st.write("""
    **Smart Customer Feedback Intelligence Platform (SCFIP)**
    
    An end-to-end AI-powered system for analyzing customer feedback using:
    - 🧠 **NLP**: spaCy, NLTK for text preprocessing
    - 🤖 **Deep Learning**: Bi-LSTM for sentiment, LSTM for intent classification
    - 🚀 **Backend**: FastAPI with RESTful endpoints
    - 📊 **Visualization**: Streamlit with Plotly charts
    - 💾 **Database**: SQLite for data persistence
    
    **Features:**
    - Real-time sentiment analysis (Positive/Neutral/Negative)
    - Intent classification (Bug Report, Feature Request, etc.)
    - Interactive dashboards and visualizations
    - Bulk CSV upload support
    - Trend analysis over time
    """)
    
    st.divider()
    
    st.subheader("API Endpoints")
    st.code("http://localhost:8000/docs", language="text")
    
    if st.button("📖 Open API Documentation"):
        st.write("[Open Swagger UI](http://localhost:8000/docs)")

if __name__ == "__main__":
    main()
