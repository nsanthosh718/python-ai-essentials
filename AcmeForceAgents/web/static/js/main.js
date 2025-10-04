// AcmeForce Web Interface JavaScript

// API Base URL
const API_BASE = '/api';

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg z-50 ${
        type === 'success' ? 'bg-green-600' : 
        type === 'error' ? 'bg-red-600' : 'bg-blue-600'
    }`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Agent management
async function createAgent(config) {
    try {
        const response = await fetch(`${API_BASE}/agents`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(config)
        });
        
        const data = await response.json();
        if (response.ok) {
            showNotification('Agent created successfully!', 'success');
            return data;
        } else {
            throw new Error(data.error || 'Failed to create agent');
        }
    } catch (error) {
        showNotification(error.message, 'error');
        throw error;
    }
}

async function getAgents() {
    try {
        const response = await fetch(`${API_BASE}/agents`);
        const data = await response.json();
        return data.agents;
    } catch (error) {
        showNotification('Failed to load agents', 'error');
        return [];
    }
}

// Real-time updates
function initializeWebSocket() {
    if (typeof WebSocket === 'undefined') return;
    
    const ws = new WebSocket(`ws://${window.location.host}/ws`);
    
    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        handleRealtimeUpdate(data);
    };
    
    ws.onclose = function() {
        // Reconnect after 5 seconds
        setTimeout(initializeWebSocket, 5000);
    };
}

function handleRealtimeUpdate(data) {
    switch(data.type) {
        case 'agent_status':
            updateAgentStatus(data.agent_id, data.status);
            break;
        case 'system_metric':
            updateSystemMetric(data.metric, data.value);
            break;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Initialize WebSocket for real-time updates
    if (window.location.pathname === '/dashboard') {
        initializeWebSocket();
    }
});