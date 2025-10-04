"""
Web Interface for Smart Content Analysis System
"""

import sys
import os
sys.path.append('../agentic-ai')

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import threading
from content_coordinator import ContentAnalysisCoordinator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'content-analysis-system'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global coordinator
coordinator = ContentAnalysisCoordinator()

@app.route('/')
def dashboard():
    return render_template('content_dashboard.html')

@app.route('/api/analyze', methods=['POST'])
def start_analysis():
    data = request.json
    source = data.get('source', 'mixed')
    
    def run_analysis():
        try:
            socketio.emit('analysis_started', {'source': source})
            result = coordinator.run_complete_analysis(source)
            socketio.emit('analysis_complete', result)
        except Exception as e:
            socketio.emit('analysis_error', {'error': str(e)})
    
    thread = threading.Thread(target=run_analysis)
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'started', 'source': source})

@app.route('/api/analyze_text', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'})
    
    result = coordinator.analyze_custom_content(text)
    return jsonify(result)

@app.route('/api/results')
def get_results():
    return jsonify(coordinator.analysis_results)

@app.route('/api/summary')
def get_summary():
    summary = coordinator.get_analysis_summary()
    return jsonify({'summary': summary})

@socketio.on('request_status')
def handle_status_request():
    status = {
        'agents': len(coordinator.agents),
        'has_results': bool(coordinator.analysis_results),
        'last_analysis': coordinator.get_analysis_summary()
    }
    emit('status_update', status)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8081)