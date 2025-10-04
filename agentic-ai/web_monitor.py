"""
Web Interface for Real-time Agentic AI Monitoring
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json
import threading
import time
from coordinator import AgentCoordinator
from llm_agent import LLMAgent, create_intelligent_task
from openai_integration import OpenAIAgent

app = Flask(__name__)
app.config['SECRET_KEY'] = 'agentic-ai-monitor'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global coordinator instance with LLM agents
coordinator = AgentCoordinator()
coordinator.agents.extend([LLMAgent(), OpenAIAgent()])
monitoring_active = False

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    return jsonify(coordinator.get_system_status())

@app.route('/api/add_task', methods=['POST'])
def add_task():
    data = request.json
    
    # Use LLM to create intelligent task
    if data.get('use_llm', False):
        task = create_intelligent_task(data['description'])
        coordinator.task_queue.append(task)
        task_id = task.id
    else:
        task_id = coordinator.add_task(data['description'], data.get('priority', 1))
    
    # Emit real-time update
    socketio.emit('task_added', {
        'task_id': task_id,
        'description': data['description'],
        'priority': data.get('priority', 1)
    })
    
    return jsonify({'task_id': task_id, 'status': 'added'})

@app.route('/api/execute_task', methods=['POST'])
def execute_task():
    result = coordinator.execute_next_task()
    
    # Emit real-time update
    socketio.emit('task_executed', result)
    
    return jsonify(result)

@socketio.on('start_monitoring')
def start_monitoring():
    global monitoring_active
    monitoring_active = True
    
    def monitor_loop():
        while monitoring_active:
            status = coordinator.get_system_status()
            socketio.emit('status_update', status)
            time.sleep(2)
    
    thread = threading.Thread(target=monitor_loop)
    thread.daemon = True
    thread.start()
    
    emit('monitoring_started', {'status': 'active'})

@socketio.on('stop_monitoring')
def stop_monitoring():
    global monitoring_active
    monitoring_active = False
    emit('monitoring_stopped', {'status': 'inactive'})

@socketio.on('auto_execute')
def auto_execute():
    def execute_loop():
        for _ in range(5):  # Execute up to 5 tasks
            if coordinator.task_queue:
                result = coordinator.execute_next_task()
                socketio.emit('task_executed', result)
                time.sleep(1)
    
    thread = threading.Thread(target=execute_loop)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    # Add sample tasks
    coordinator.add_task("Analyze customer behavior data", 3)
    coordinator.add_task("Train recommendation model", 2)
    coordinator.add_task("Plan ML deployment strategy", 1)
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)