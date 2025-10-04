"""
AcmeForce Inc - Freemium Trial System
Contact: info@acme-force.com
"""

from datetime import datetime, timedelta
import json

class TrialManager:
    def __init__(self):
        self.trial_duration = 14  # days
        self.trial_limits = {
            "max_agents": 2,
            "api_calls_per_day": 100,
            "evolution_cycles": 5,
            "features": ["basic_evolution", "simple_swarm"]
        }
    
    def create_trial(self, user_email):
        """Create new trial account"""
        trial_data = {
            "email": user_email,
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=self.trial_duration)).isoformat(),
            "usage": {
                "agents_created": 0,
                "api_calls_today": 0,
                "evolution_cycles_used": 0
            },
            "status": "active"
        }
        return trial_data
    
    def check_trial_status(self, trial_data):
        """Check if trial is still valid"""
        end_date = datetime.fromisoformat(trial_data["end_date"])
        if datetime.now() > end_date:
            return "expired"
        return trial_data["status"]
    
    def can_perform_action(self, trial_data, action, count=1):
        """Check if trial user can perform action"""
        if self.check_trial_status(trial_data) != "active":
            return False
        
        usage = trial_data["usage"]
        limits = self.trial_limits
        
        if action == "create_agent":
            return usage["agents_created"] + count <= limits["max_agents"]
        elif action == "api_call":
            return usage["api_calls_today"] + count <= limits["api_calls_per_day"]
        elif action == "evolution_cycle":
            return usage["evolution_cycles_used"] + count <= limits["evolution_cycles"]
        
        return False
    
    def record_usage(self, trial_data, action, count=1):
        """Record usage for trial account"""
        if action == "create_agent":
            trial_data["usage"]["agents_created"] += count
        elif action == "api_call":
            trial_data["usage"]["api_calls_today"] += count
        elif action == "evolution_cycle":
            trial_data["usage"]["evolution_cycles_used"] += count
        
        return trial_data

# Trial conversion hooks
CONVERSION_TRIGGERS = {
    "agent_limit_reached": {
        "message": "You've reached your 2-agent limit. Upgrade to create unlimited agents!",
        "cta": "Upgrade to Professional",
        "discount": 20  # 20% first month discount
    },
    "api_limit_reached": {
        "message": "Daily API limit reached. Upgrade for 10,000+ calls per hour!",
        "cta": "Upgrade Now",
        "discount": 15
    },
    "trial_expiring": {
        "message": "Your trial expires in 2 days. Continue your AI journey!",
        "cta": "Choose Your Plan",
        "discount": 25
    }
}