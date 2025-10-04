"""
AcmeForce Inc - Product Packaging & Feature Management
Contact: info@acme-force.com
"""

class ProductTier:
    def __init__(self, name, price, features, limits):
        self.name = name
        self.price = price
        self.features = features
        self.limits = limits

# Product Tiers Configuration
PRODUCT_TIERS = {
    "starter": ProductTier(
        name="Starter",
        price=299,
        features=[
            "Basic Evolution Engine",
            "5 Concurrent Agents",
            "Email Support",
            "Standard Documentation",
            "Community Forum Access"
        ],
        limits={
            "max_agents": 5,
            "api_calls_per_hour": 1000,
            "evolution_cycles": 10,
            "support_response": "48h",
            "data_retention": "30 days"
        }
    ),
    
    "professional": ProductTier(
        name="Professional", 
        price=999,
        features=[
            "Full Evolution Engine",
            "Complete Swarm Intelligence",
            "Unlimited Agents",
            "Priority Support",
            "2 Consulting Hours/Month",
            "Advanced Analytics",
            "API Access",
            "Custom Integrations"
        ],
        limits={
            "max_agents": "unlimited",
            "api_calls_per_hour": 10000,
            "evolution_cycles": "unlimited",
            "support_response": "8h",
            "data_retention": "1 year",
            "consulting_hours": 2
        }
    ),
    
    "enterprise": ProductTier(
        name="Enterprise",
        price=2999,
        features=[
            "Full AFA System",
            "Quantum Reasoning Engine",
            "Custom Deployment",
            "Dedicated Support Rep",
            "Weekly Consulting Calls",
            "White-label Options",
            "Source Code Escrow",
            "SLA Guarantees",
            "Custom Training"
        ],
        limits={
            "max_agents": "unlimited",
            "api_calls_per_hour": "unlimited",
            "evolution_cycles": "unlimited", 
            "support_response": "2h",
            "data_retention": "unlimited",
            "consulting_hours": "weekly",
            "uptime_sla": "99.95%"
        }
    )
}

# Add-on Services
ADD_ON_SERVICES = {
    "training_workshop": {
        "name": "2-Day Training Workshop",
        "price": 2999,
        "description": "Intensive hands-on training for your team"
    },
    "custom_implementation": {
        "name": "Custom Implementation",
        "price": 15000,
        "description": "Tailored deployment and integration"
    },
    "dedicated_support": {
        "name": "Dedicated Support Engineer",
        "price": 5000,
        "description": "Monthly dedicated support retainer"
    }
}

def get_tier_features(tier_name):
    """Get features for a specific tier"""
    return PRODUCT_TIERS.get(tier_name, {}).features

def validate_tier_limits(tier_name, usage):
    """Validate if usage is within tier limits"""
    tier = PRODUCT_TIERS.get(tier_name)
    if not tier:
        return False
    
    for limit_key, limit_value in tier.limits.items():
        if limit_key in usage:
            if limit_value != "unlimited" and usage[limit_key] > limit_value:
                return False
    return True