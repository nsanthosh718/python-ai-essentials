"""
AcmeForce Inc - PayPal Payment Integration
Contact: info@acme-force.com
"""

import requests
import json
from datetime import datetime, timedelta
import os

class PayPalIntegration:
    def __init__(self, client_id, client_secret, sandbox=True):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api.sandbox.paypal.com" if sandbox else "https://api.paypal.com"
        self.access_token = None
    
    def get_access_token(self):
        """Get PayPal access token"""
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en_US',
        }
        data = 'grant_type=client_credentials'
        
        response = requests.post(url, headers=headers, data=data, 
                               auth=(self.client_id, self.client_secret))
        
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            return self.access_token
        return None
    
    def create_subscription_plan(self, plan_name, price, billing_cycle="MONTH"):
        """Create subscription plan"""
        if not self.access_token:
            self.get_access_token()
        
        url = f"{self.base_url}/v1/billing/plans"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }
        
        plan_data = {
            "product_id": f"ACMEFORCE_{plan_name.upper()}",
            "name": f"AcmeForce {plan_name}",
            "description": f"AcmeForceAgents {plan_name} Plan",
            "billing_cycles": [{
                "frequency": {
                    "interval_unit": billing_cycle,
                    "interval_count": 1
                },
                "tenure_type": "REGULAR",
                "sequence": 1,
                "total_cycles": 0,
                "pricing_scheme": {
                    "fixed_price": {
                        "value": str(price),
                        "currency_code": "USD"
                    }
                }
            }],
            "payment_preferences": {
                "auto_bill_outstanding": True,
                "setup_fee_failure_action": "CONTINUE",
                "payment_failure_threshold": 3
            }
        }
        
        response = requests.post(url, headers=headers, json=plan_data)
        return response.json() if response.status_code == 201 else None

# Subscription Plans Configuration
SUBSCRIPTION_PLANS = {
    "starter": {
        "name": "Starter",
        "price": 299,
        "features": ["Basic AFA System", "Email Support", "5 Agents Max"]
    },
    "professional": {
        "name": "Professional", 
        "price": 999,
        "features": ["Full AFA System", "Priority Support", "Unlimited Agents", "2 Consulting Hours/Month"]
    },
    "enterprise": {
        "name": "Enterprise",
        "price": 2999,
        "features": ["Custom Deployment", "Dedicated Support", "Unlimited Everything", "Weekly Consulting"]
    }
}

def setup_paypal_plans():
    """Initialize all subscription plans"""
    # Use environment variables for production
    paypal = PayPalIntegration(
        client_id=os.getenv('PAYPAL_CLIENT_ID', 'your_client_id'),
        client_secret=os.getenv('PAYPAL_CLIENT_SECRET', 'your_client_secret'),
        sandbox=True
    )
    
    for plan_key, plan_info in SUBSCRIPTION_PLANS.items():
        result = paypal.create_subscription_plan(
            plan_info["name"], 
            plan_info["price"]
        )
        print(f"Created {plan_info['name']} plan: {result}")

if __name__ == "__main__":
    setup_paypal_plans()