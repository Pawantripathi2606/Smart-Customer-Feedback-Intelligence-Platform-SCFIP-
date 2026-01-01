import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import config

class FeedbackDatabase:
    """SQLite database operations for feedback management"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(config.DATABASE_PATH)
        self.init_database()
    
    def get_connection(self):
        """Create a database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feedback_id TEXT UNIQUE NOT NULL,
                text TEXT NOT NULL,
                source TEXT NOT NULL,
                date TEXT NOT NULL,
                sentiment TEXT,
                sentiment_score REAL,
                intent TEXT,
                intent_score REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create analytics table for aggregated data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value TEXT NOT NULL,
                calculated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_feedback(self, feedback_data: Dict) -> bool:
        """Add new feedback to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO feedback (feedback_id, text, source, date, sentiment, 
                                     sentiment_score, intent, intent_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                feedback_data.get('feedback_id'),
                feedback_data.get('text'),
                feedback_data.get('source'),
                feedback_data.get('date'),
                feedback_data.get('sentiment'),
                feedback_data.get('sentiment_score'),
                feedback_data.get('intent'),
                feedback_data.get('intent_score')
            ))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Feedback ID already exists
            return False
        except Exception as e:
            print(f"Error adding feedback: {e}")
            return False
    
    def get_all_feedback(self, limit: int = None, source: str = None, 
                        sentiment: str = None) -> List[Dict]:
        """Retrieve all feedback with optional filters"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM feedback WHERE 1=1"
        params = []
        
        if source:
            query += " AND source = ?"
            params.append(source)
        
        if sentiment:
            query += " AND sentiment = ?"
            params.append(sentiment)
        
        query += " ORDER BY created_at DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        cursor.execute(query, params)
        columns = [description[0] for description in cursor.description]
        results = []
        
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        conn.close()
        return results
    
    def get_feedback_by_id(self, feedback_id: str) -> Optional[Dict]:
        """Get specific feedback by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM feedback WHERE feedback_id = ?", (feedback_id,))
        columns = [description[0] for description in cursor.description]
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return dict(zip(columns, row))
        return None
    
    def update_feedback_analysis(self, feedback_id: str, sentiment: str, 
                                 sentiment_score: float, intent: str, 
                                 intent_score: float) -> bool:
        """Update feedback with analysis results"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE feedback 
                SET sentiment = ?, sentiment_score = ?, intent = ?, intent_score = ?
                WHERE feedback_id = ?
            ''', (sentiment, sentiment_score, intent, intent_score, feedback_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating feedback: {e}")
            return False
    
    def get_sentiment_distribution(self) -> Dict[str, int]:
        """Get count of feedback by sentiment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sentiment, COUNT(*) as count 
            FROM feedback 
            WHERE sentiment IS NOT NULL
            GROUP BY sentiment
        ''')
        
        results = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        return results
    
    def get_intent_distribution(self) -> Dict[str, int]:
        """Get count of feedback by intent"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT intent, COUNT(*) as count 
            FROM feedback 
            WHERE intent IS NOT NULL
            GROUP BY intent
            ORDER BY count DESC
        ''')
        
        results = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        return results
    
    def get_source_distribution(self) -> Dict[str, int]:
        """Get count of feedback by source"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT source, COUNT(*) as count 
            FROM feedback 
            GROUP BY source
        ''')
        
        results = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        return results
    
    def get_trends_by_date(self) -> List[Dict]:
        """Get feedback trends over time"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT date, sentiment, COUNT(*) as count 
            FROM feedback 
            WHERE sentiment IS NOT NULL
            GROUP BY date, sentiment
            ORDER BY date
        ''')
        
        columns = ['date', 'sentiment', 'count']
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_negative_feedback(self, limit: int = 10) -> List[Dict]:
        """Get most recent negative feedback"""
        return self.get_all_feedback(limit=limit, sentiment="Negative")
    
    def get_summary_stats(self) -> Dict:
        """Get overall summary statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total feedback count
        cursor.execute("SELECT COUNT(*) FROM feedback")
        total_count = cursor.fetchone()[0]
        
        # Average sentiment score
        cursor.execute("SELECT AVG(sentiment_score) FROM feedback WHERE sentiment_score IS NOT NULL")
        avg_sentiment = cursor.fetchone()[0] or 0
        
        # Most common intent
        cursor.execute('''
            SELECT intent, COUNT(*) as count 
            FROM feedback 
            WHERE intent IS NOT NULL
            GROUP BY intent 
            ORDER BY count DESC 
            LIMIT 1
        ''')
        top_intent_row = cursor.fetchone()
        top_intent = top_intent_row[0] if top_intent_row else "N/A"
        
        conn.close()
        
        return {
            "total_feedback": total_count,
            "avg_sentiment_score": round(avg_sentiment, 2),
            "top_intent": top_intent
        }
    
    def delete_all_feedback(self):
        """Delete all feedback (for testing purposes)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM feedback")
        conn.commit()
        conn.close()


# Singleton instance
db = FeedbackDatabase()
