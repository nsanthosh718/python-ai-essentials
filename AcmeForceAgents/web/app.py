"""
AcmeForce Inc - Web Interface
Contact: info@acme-force.com
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import sys
sys.path.append('..')
from payment_integration import PayPalIntegration, SUBSCRIPTION_PLANS

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

@app.route('/')
def home():
    return render_template('index.html', plans=SUBSCRIPTION_PLANS)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', plans=SUBSCRIPTION_PLANS)

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    plan = request.json.get('plan')
    if plan not in SUBSCRIPTION_PLANS:
        return jsonify({'error': 'Invalid plan'}), 400
    
    # PayPal subscription creation logic here
    return jsonify({'success': True, 'redirect_url': '/dashboard'})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/agents', methods=['GET', 'POST'])
def agents():
    if request.method == 'POST':
        # Create new agent
        agent_config = request.json
        return jsonify({'agent_id': 'agent_123', 'status': 'created'})
    
    # List agents
    return jsonify({'agents': []})

if __name__ == '__main__':
    app.run(debug=True, port=5000)