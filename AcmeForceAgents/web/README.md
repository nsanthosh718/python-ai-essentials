# AcmeForceAgents Web Interface

Professional web interface for the AcmeForceAgents autonomous AI system.

## Quick Start

```bash
cd web
pip install -r requirements.txt
python app.py
```

Visit: http://localhost:5000

## Features

- **Landing Page** - Professional marketing site
- **Interactive Demo** - Try agents without signup
- **Pricing Plans** - Subscription management
- **Dashboard** - Agent fleet management
- **PayPal Integration** - Automated billing

## Pages

- `/` - Homepage with features
- `/pricing` - Subscription plans
- `/demo` - Interactive agent demo  
- `/dashboard` - Agent management

## API Endpoints

- `POST /api/subscribe` - Create subscription
- `GET /api/agents` - List agents
- `POST /api/agents` - Create agent

## Deployment

Set environment variables:
```bash
export SECRET_KEY="your-secret-key"
export PAYPAL_CLIENT_ID="your-paypal-client-id"
export PAYPAL_CLIENT_SECRET="your-paypal-secret"
```

For production, use gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---
**AcmeForce Inc**  
Contact: info@acme-force.com