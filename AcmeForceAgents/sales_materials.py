"""
AcmeForce Inc - Sales Materials Generator
Contact: info@acme-force.com
"""

# Value Propositions by Industry
INDUSTRY_VALUE_PROPS = {
    "fintech": {
        "headline": "Autonomous Trading & Risk Management",
        "benefits": [
            "24/7 market monitoring with evolution-based adaptation",
            "Quantum reasoning for complex financial modeling",
            "Swarm intelligence for portfolio optimization",
            "Regulatory compliance automation"
        ],
        "roi": "Average 23% improvement in trading performance"
    },
    
    "healthcare": {
        "headline": "Intelligent Patient Care & Research",
        "benefits": [
            "Autonomous patient monitoring systems",
            "Drug discovery acceleration with AI evolution",
            "Multi-agent coordination for hospital operations",
            "Predictive health analytics"
        ],
        "roi": "Reduce operational costs by 31%"
    },
    
    "manufacturing": {
        "headline": "Smart Factory Automation",
        "benefits": [
            "Self-optimizing production lines",
            "Predictive maintenance with evolution engine",
            "Supply chain coordination via swarm intelligence",
            "Quality control automation"
        ],
        "roi": "Increase efficiency by 40%"
    },
    
    "retail": {
        "headline": "Personalized Customer Experience",
        "benefits": [
            "Dynamic pricing optimization",
            "Inventory management with predictive AI",
            "Customer behavior analysis and prediction",
            "Automated marketing campaign optimization"
        ],
        "roi": "Boost revenue by 28%"
    }
}

# Competitive Advantages
COMPETITIVE_ADVANTAGES = [
    {
        "feature": "Evolution Engine",
        "advantage": "Self-improving AI that gets smarter over time",
        "competitor_gap": "Static AI models that require manual updates"
    },
    {
        "feature": "Swarm Intelligence", 
        "advantage": "Coordinated multi-agent problem solving",
        "competitor_gap": "Single-agent solutions with limited scope"
    },
    {
        "feature": "Quantum Reasoning",
        "advantage": "Advanced reasoning with superposition concepts",
        "competitor_gap": "Traditional logic-based AI reasoning"
    },
    {
        "feature": "Autonomous Operation",
        "advantage": "Minimal human intervention required",
        "competitor_gap": "Requires constant monitoring and adjustment"
    }
]

# ROI Calculator
def calculate_roi(company_size, use_case, current_costs):
    """Calculate potential ROI for prospect"""
    efficiency_gains = {
        "small": 0.25,    # 25% efficiency gain
        "medium": 0.35,   # 35% efficiency gain  
        "large": 0.45     # 45% efficiency gain
    }
    
    use_case_multipliers = {
        "automation": 1.2,
        "analytics": 1.0,
        "optimization": 1.5,
        "prediction": 1.3
    }
    
    base_gain = efficiency_gains.get(company_size, 0.25)
    multiplier = use_case_multipliers.get(use_case, 1.0)
    
    annual_savings = current_costs * base_gain * multiplier
    afa_annual_cost = 999 * 12  # Professional plan
    
    net_roi = ((annual_savings - afa_annual_cost) / afa_annual_cost) * 100
    payback_months = afa_annual_cost / (annual_savings / 12)
    
    return {
        "annual_savings": annual_savings,
        "net_roi_percent": round(net_roi, 1),
        "payback_months": round(payback_months, 1),
        "three_year_value": annual_savings * 3 - (afa_annual_cost * 3)
    }

# Sales Email Templates
EMAIL_TEMPLATES = {
    "cold_outreach": """
Subject: Reduce AI Development Time by 70% - AcmeForceAgents

Hi {name},

I noticed {company} is investing heavily in AI initiatives. Most companies struggle with:
- AI models that don't improve over time
- Complex multi-agent coordination
- Months of development for basic automation

AcmeForceAgents solves this with autonomous AI that evolves and coordinates automatically.

{industry_specific_benefit}

Would you be interested in a 15-minute demo showing how we helped similar companies achieve {roi_metric}?

Best regards,
AcmeForce Sales Team
info@acme-force.com
""",
    
    "follow_up": """
Subject: Re: AcmeForceAgents Demo for {company}

Hi {name},

Following up on our conversation about autonomous AI for {company}.

Key points from our discussion:
- Your current challenge: {pain_point}
- AFA solution: {solution}
- Potential impact: {roi_estimate}

Next steps:
1. 14-day free trial (no credit card required)
2. Custom demo with your data
3. ROI analysis for your specific use case

Ready to start your trial?

Best,
AcmeForce Team
"""
}

def generate_proposal(company_info):
    """Generate custom proposal"""
    return {
        "executive_summary": f"AcmeForceAgents will help {company_info['name']} achieve autonomous AI operations",
        "recommended_plan": "professional" if company_info.get('size') == 'medium' else "enterprise",
        "implementation_timeline": "2-4 weeks",
        "expected_roi": calculate_roi(company_info.get('size', 'medium'), 
                                    company_info.get('use_case', 'automation'),
                                    company_info.get('current_costs', 100000))
    }