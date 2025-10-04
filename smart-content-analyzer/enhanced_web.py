"""
Enhanced Web Interface with Real-time Analytics and File Upload
"""

import sys
import os
sys.path.append('../agentic-ai')

from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import json
import threading
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

from enhanced_agents import RealDataCollectorAgent, MLSentimentAgent, AdvancedTrendAgent
from api_integrations import APIManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'enhanced-content-analysis'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
socketio = SocketIO(app, cors_allowed_origins="*")

# Global instances
data_collector = RealDataCollectorAgent()
ml_sentiment = MLSentimentAgent()
trend_analyzer = AdvancedTrendAgent()
api_manager = APIManager()

@app.route('/')
def enhanced_dashboard():
    return render_template('enhanced_dashboard.html')

@app.route('/api/enhanced_analyze', methods=['POST'])
def enhanced_analysis():
    data = request.json
    source = data.get('source', 'mixed')
    query = data.get('query', 'AI')
    use_ml = data.get('use_ml', True)
    
    def run_enhanced_analysis():
        try:
            socketio.emit('analysis_started', {'source': source, 'query': query})
            
            # Step 1: Enhanced data collection
            socketio.emit('analysis_step', {'step': 1, 'message': 'Collecting data from real sources...'})
            
            if source == 'api_all':
                collection_result = api_manager.collect_from_all_sources(query)
                content_data = {
                    "source": "api_all",
                    "content": collection_result["sources"],
                    "count": collection_result["total_items"]
                }
            else:
                # Use enhanced data collector
                from agent import Task
                task = Task(id="collect", description=f"Collect {source} content about {query}")
                content_data = data_collector.execute_task(task)
            
            socketio.emit('analysis_step', {'step': 2, 'message': 'Analyzing sentiment with ML...'})
            
            # Step 2: ML Sentiment Analysis
            sentiment_task = Task(id="sentiment", description="ML sentiment analysis")
            sentiment_task.content_data = content_data
            
            if use_ml:
                sentiment_data = ml_sentiment.execute_task(sentiment_task)
            else:
                # Fallback to basic sentiment
                from content_agents import SentimentAnalysisAgent
                basic_sentiment = SentimentAnalysisAgent()
                sentiment_data = basic_sentiment.execute_task(sentiment_task)
            
            socketio.emit('analysis_step', {'step': 3, 'message': 'Performing advanced trend analysis...'})
            
            # Step 3: Advanced Trend Analysis
            trend_task = Task(id="trends", description="Advanced trend analysis")
            trend_task.sentiment_data = sentiment_data
            trend_data = trend_analyzer.execute_task(trend_task)
            
            # Step 4: Generate visualizations
            socketio.emit('analysis_step', {'step': 4, 'message': 'Generating visualizations...'})
            charts = generate_charts(sentiment_data, trend_data)
            
            result = {
                "status": "success",
                "content_data": content_data,
                "sentiment_data": sentiment_data,
                "trend_data": trend_data,
                "charts": charts,
                "analysis_complete": True
            }
            
            socketio.emit('enhanced_analysis_complete', result)
            
        except Exception as e:
            socketio.emit('analysis_error', {'error': str(e)})
    
    thread = threading.Thread(target=run_enhanced_analysis)
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'started', 'source': source, 'query': query})

@app.route('/api/upload_file', methods=['POST'])
def upload_file():
    """Handle file upload for content analysis"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    try:
        # Read file content
        content = file.read().decode('utf-8')
        
        # Process content (split by lines, filter empty)
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Create content data structure
        content_data = {
            "source": "uploaded_file",
            "content": [{"text": line} for line in lines],
            "count": len(lines),
            "filename": file.filename
        }
        
        # Store in database
        data_collector._store_content("uploaded_file", content_data["content"])
        
        return jsonify({
            'success': True,
            'filename': file.filename,
            'lines_processed': len(lines),
            'content_data': content_data
        })
        
    except Exception as e:
        return jsonify({'error': f'File processing failed: {str(e)}'})

@app.route('/api/historical_data')
def get_historical_data():
    """Get historical analysis data"""
    try:
        conn = sqlite3.connect(data_collector.db_path)
        
        # Get data from last 30 days
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        
        query = """
        SELECT source, COUNT(*) as count, DATE(collected_at) as date
        FROM content 
        WHERE collected_at > ?
        GROUP BY source, DATE(collected_at)
        ORDER BY date DESC
        """
        
        df = pd.read_sql_query(query, conn, params=(thirty_days_ago,))
        conn.close()
        
        # Convert to format suitable for charts
        historical_data = df.to_dict('records')
        
        return jsonify({
            'historical_data': historical_data,
            'total_records': len(historical_data)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get historical data: {str(e)}'})

@app.route('/api/api_status')
def get_api_status():
    """Get status of external APIs"""
    status = api_manager.get_api_status()
    return jsonify(status)

@app.route('/api/export_results')
def export_results():
    """Export analysis results to CSV"""
    try:
        conn = sqlite3.connect(data_collector.db_path)
        
        # Get recent data
        query = """
        SELECT source, content, collected_at
        FROM content 
        ORDER BY collected_at DESC
        LIMIT 1000
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Create CSV in memory
        output = BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'content_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'})

def generate_charts(sentiment_data, trend_data):
    """Generate visualization charts"""
    charts = {}
    
    try:
        # Sentiment distribution pie chart
        if sentiment_data and "summary" in sentiment_data:
            summary = sentiment_data["summary"]
            
            plt.figure(figsize=(8, 6))
            labels = list(summary.keys())
            sizes = list(summary.values())
            colors = ['#ff9999', '#66b3ff', '#99ff99']
            
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.title('Sentiment Distribution')
            
            # Convert to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            chart_data = base64.b64encode(buffer.getvalue()).decode()
            charts['sentiment_pie'] = f"data:image/png;base64,{chart_data}"
            plt.close()
        
        # Confidence distribution histogram
        if sentiment_data and "individual_results" in sentiment_data:
            confidences = [r.get("confidence", 0) for r in sentiment_data["individual_results"]]
            
            plt.figure(figsize=(10, 6))
            plt.hist(confidences, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            plt.xlabel('Confidence Score')
            plt.ylabel('Frequency')
            plt.title('Sentiment Analysis Confidence Distribution')
            plt.grid(True, alpha=0.3)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            chart_data = base64.b64encode(buffer.getvalue()).decode()
            charts['confidence_hist'] = f"data:image/png;base64,{chart_data}"
            plt.close()
        
    except Exception as e:
        print(f"Chart generation error: {e}")
        charts['error'] = str(e)
    
    return charts

@socketio.on('request_enhanced_status')
def handle_enhanced_status():
    """Send enhanced system status"""
    try:
        # Get database stats
        conn = sqlite3.connect(data_collector.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM content")
        total_content = cursor.fetchone()[0]
        
        cursor.execute("SELECT source, COUNT(*) FROM content GROUP BY source")
        source_counts = dict(cursor.fetchall())
        
        conn.close()
        
        # Get API status
        api_status = api_manager.get_api_status()
        
        status = {
            'total_content_items': total_content,
            'source_breakdown': source_counts,
            'api_status': api_status,
            'ml_model_loaded': ml_sentiment.model is not None,
            'database_connected': True
        }
        
        emit('enhanced_status_update', status)
        
    except Exception as e:
        emit('enhanced_status_update', {'error': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8082)