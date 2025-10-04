/**
 * Stripe Payment Integration for n8n AI Nodes
 */

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const express = require('express');
const router = express.Router();

// Pricing configuration
const PRICING_PLANS = {
    starter: {
        price_id: 'price_starter_monthly',
        amount: 2900, // $29.00
        features: ['1000_analyses', 'basic_sentiment', 'email_support'],
        limits: { monthly: 1000, batch_size: 10 }
    },
    professional: {
        price_id: 'price_professional_monthly',
        amount: 9900, // $99.00
        features: ['10000_analyses', 'ml_sentiment', 'priority_support', 'custom_branding'],
        limits: { monthly: 10000, batch_size: 100 }
    },
    enterprise: {
        price_id: 'price_enterprise_monthly',
        amount: 29900, // $299.00
        features: ['unlimited_analyses', 'custom_models', 'dedicated_support', 'white_label'],
        limits: { monthly: -1, batch_size: 1000 }
    }
};

// Create checkout session
router.post('/create-checkout-session', async (req, res) => {
    try {
        const { plan, email, trial = true } = req.body;
        
        if (!PRICING_PLANS[plan]) {
            return res.status(400).json({ error: 'Invalid plan selected' });
        }

        const session = await stripe.checkout.sessions.create({
            customer_email: email,
            payment_method_types: ['card'],
            line_items: [{
                price: PRICING_PLANS[plan].price_id,
                quantity: 1,
            }],
            mode: 'subscription',
            success_url: `${process.env.DOMAIN}/success?session_id={CHECKOUT_SESSION_ID}`,
            cancel_url: `${process.env.DOMAIN}/pricing`,
            subscription_data: trial ? {
                trial_period_days: 7,
                metadata: {
                    plan: plan,
                    features: JSON.stringify(PRICING_PLANS[plan].features)
                }
            } : {
                metadata: {
                    plan: plan,
                    features: JSON.stringify(PRICING_PLANS[plan].features)
                }
            },
            metadata: {
                plan: plan,
                email: email
            }
        });

        res.json({ checkout_url: session.url });

    } catch (error) {
        console.error('Stripe checkout error:', error);
        res.status(500).json({ error: 'Failed to create checkout session' });
    }
});

// Handle successful payment
router.post('/webhook', express.raw({type: 'application/json'}), async (req, res) => {
    const sig = req.headers['stripe-signature'];
    let event;

    try {
        event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
    } catch (err) {
        console.error('Webhook signature verification failed:', err.message);
        return res.status(400).send(`Webhook Error: ${err.message}`);
    }

    // Handle the event
    switch (event.type) {
        case 'checkout.session.completed':
            await handleCheckoutCompleted(event.data.object);
            break;
        
        case 'customer.subscription.created':
            await handleSubscriptionCreated(event.data.object);
            break;
        
        case 'customer.subscription.updated':
            await handleSubscriptionUpdated(event.data.object);
            break;
        
        case 'customer.subscription.deleted':
            await handleSubscriptionCanceled(event.data.object);
            break;
        
        case 'invoice.payment_succeeded':
            await handlePaymentSucceeded(event.data.object);
            break;
        
        case 'invoice.payment_failed':
            await handlePaymentFailed(event.data.object);
            break;
        
        default:
            console.log(`Unhandled event type ${event.type}`);
    }

    res.json({received: true});
});

async function handleCheckoutCompleted(session) {
    console.log('Checkout completed:', session.id);
    
    // Create user account and generate license key
    const licenseKey = generateLicenseKey();
    const plan = session.metadata.plan;
    
    // Store in database
    await createUserAccount({
        email: session.customer_email,
        stripe_customer_id: session.customer,
        stripe_subscription_id: session.subscription,
        license_key: licenseKey,
        plan: plan,
        status: 'active',
        trial_end: session.subscription ? null : new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
    });
    
    // Send welcome email with license key
    await sendWelcomeEmail(session.customer_email, licenseKey, plan);
}

async function handleSubscriptionCreated(subscription) {
    console.log('Subscription created:', subscription.id);
    
    // Update user record with subscription details
    await updateUserSubscription(subscription.customer, {
        stripe_subscription_id: subscription.id,
        status: subscription.status,
        current_period_start: new Date(subscription.current_period_start * 1000),
        current_period_end: new Date(subscription.current_period_end * 1000),
        trial_end: subscription.trial_end ? new Date(subscription.trial_end * 1000) : null
    });
}

async function handleSubscriptionUpdated(subscription) {
    console.log('Subscription updated:', subscription.id);
    
    // Update user subscription status
    await updateUserSubscription(subscription.customer, {
        status: subscription.status,
        current_period_start: new Date(subscription.current_period_start * 1000),
        current_period_end: new Date(subscription.current_period_end * 1000)
    });
}

async function handleSubscriptionCanceled(subscription) {
    console.log('Subscription canceled:', subscription.id);
    
    // Update user status but keep access until period end
    await updateUserSubscription(subscription.customer, {
        status: 'canceled',
        cancel_at_period_end: true
    });
    
    // Send cancellation email
    const user = await getUserByStripeCustomerId(subscription.customer);
    if (user) {
        await sendCancellationEmail(user.email, subscription.current_period_end);
    }
}

async function handlePaymentSucceeded(invoice) {
    console.log('Payment succeeded:', invoice.id);
    
    // Update usage limits for the new billing period
    const user = await getUserByStripeCustomerId(invoice.customer);
    if (user) {
        await resetUsageLimits(user.license_key);
        await sendPaymentSuccessEmail(user.email, invoice.amount_paid / 100);
    }
}

async function handlePaymentFailed(invoice) {
    console.log('Payment failed:', invoice.id);
    
    // Send payment failure notification
    const user = await getUserByStripeCustomerId(invoice.customer);
    if (user) {
        await sendPaymentFailedEmail(user.email, invoice.next_payment_attempt);
    }
}

function generateLicenseKey() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    const segments = [];
    
    for (let i = 0; i < 4; i++) {
        let segment = '';
        for (let j = 0; j < 4; j++) {
            segment += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        segments.push(segment);
    }
    
    return segments.join('-');
}

// Database operations (implement with your preferred database)
async function createUserAccount(userData) {
    // Implementation depends on your database choice
    console.log('Creating user account:', userData);
}

async function updateUserSubscription(customerId, updateData) {
    // Implementation depends on your database choice
    console.log('Updating subscription:', customerId, updateData);
}

async function getUserByStripeCustomerId(customerId) {
    // Implementation depends on your database choice
    console.log('Getting user by customer ID:', customerId);
    return null;
}

async function resetUsageLimits(licenseKey) {
    // Reset monthly usage counters
    console.log('Resetting usage limits for:', licenseKey);
}

// Email functions (implement with your preferred email service)
async function sendWelcomeEmail(email, licenseKey, plan) {
    console.log(`Sending welcome email to ${email} with license ${licenseKey} for plan ${plan}`);
}

async function sendCancellationEmail(email, periodEnd) {
    console.log(`Sending cancellation email to ${email}, access until ${periodEnd}`);
}

async function sendPaymentSuccessEmail(email, amount) {
    console.log(`Sending payment success email to ${email} for $${amount}`);
}

async function sendPaymentFailedEmail(email, nextAttempt) {
    console.log(`Sending payment failed email to ${email}, next attempt: ${nextAttempt}`);
}

module.exports = router;