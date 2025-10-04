/**
 * Commercial License Management System
 */

const crypto = require('crypto');
const axios = require('axios');

class LicenseManager {
    constructor() {
        this.licenseServer = 'https://license.n8n-ai-nodes.com';
        this.cache = new Map();
        this.cacheTimeout = 3600000; // 1 hour
    }

    async validateLicense(licenseKey, nodeType = 'any') {
        // Check cache first
        const cacheKey = `${licenseKey}_${nodeType}`;
        const cached = this.cache.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }

        try {
            const response = await axios.post(`${this.licenseServer}/validate`, {
                license_key: licenseKey,
                node_type: nodeType,
                timestamp: Date.now(),
            }, {
                timeout: 5000,
                headers: {
                    'User-Agent': 'n8n-ai-nodes/1.0.0',
                    'Content-Type': 'application/json',
                }
            });

            const validation = {
                valid: response.data.valid,
                tier: response.data.tier,
                features: response.data.features,
                usage: response.data.usage,
                limits: response.data.limits,
                expires: response.data.expires,
            };

            // Cache the result
            this.cache.set(cacheKey, {
                data: validation,
                timestamp: Date.now(),
            });

            return validation;

        } catch (error) {
            // Fallback for offline mode (limited functionality)
            if (this.isValidFormat(licenseKey)) {
                return {
                    valid: true,
                    tier: 'starter',
                    features: ['basic_sentiment'],
                    usage: { current: 0, limit: 100 },
                    limits: { monthly: 100 },
                    expires: Date.now() + 86400000, // 24 hours
                    offline_mode: true,
                };
            }
            
            throw new Error(`License validation failed: ${error.message}`);
        }
    }

    isValidFormat(licenseKey) {
        // Basic format validation
        const pattern = /^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/;
        return pattern.test(licenseKey);
    }

    async checkUsageLimit(licenseKey, operation) {
        const validation = await this.validateLicense(licenseKey, operation);
        
        if (!validation.valid) {
            throw new Error('Invalid license key');
        }

        if (validation.usage.current >= validation.limits.monthly) {
            throw new Error(`Monthly usage limit exceeded (${validation.limits.monthly})`);
        }

        return validation;
    }

    async recordUsage(licenseKey, operation, count = 1) {
        try {
            await axios.post(`${this.licenseServer}/usage`, {
                license_key: licenseKey,
                operation: operation,
                count: count,
                timestamp: Date.now(),
            });
        } catch (error) {
            // Log but don't fail the operation
            console.warn('Failed to record usage:', error.message);
        }
    }

    generateTrialLicense() {
        // Generate 7-day trial license
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        const segments = [];
        
        for (let i = 0; i < 4; i++) {
            let segment = '';
            for (let j = 0; j < 4; j++) {
                segment += chars.charAt(Math.floor(Math.random() * chars.length));
            }
            segments.push(segment);
        }
        
        return `TRIAL-${segments.join('-')}`;
    }

    getFeatureAccess(tier) {
        const features = {
            starter: [
                'basic_sentiment',
                'simple_reports',
                'standard_support'
            ],
            professional: [
                'basic_sentiment',
                'ml_sentiment',
                'advanced_reports',
                'batch_processing',
                'priority_support'
            ],
            enterprise: [
                'basic_sentiment',
                'ml_sentiment',
                'deep_analysis',
                'custom_models',
                'white_label',
                'unlimited_processing',
                'dedicated_support'
            ]
        };

        return features[tier] || features.starter;
    }

    getLimits(tier) {
        const limits = {
            starter: {
                monthly: 1000,
                batch_size: 10,
                api_calls: 100
            },
            professional: {
                monthly: 10000,
                batch_size: 100,
                api_calls: 1000
            },
            enterprise: {
                monthly: -1, // unlimited
                batch_size: 1000,
                api_calls: -1 // unlimited
            }
        };

        return limits[tier] || limits.starter;
    }
}

module.exports = LicenseManager;