# Security Guidelines

## 🔐 API Key Management

**NEVER commit API keys to version control!**

### Setup Instructions:

1. **Create .env file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your API key to .env:**
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```

3. **Verify .env is in .gitignore:**
   ```bash
   grep ".env" .gitignore
   ```

### Using the Setup Script:

```bash
python setup_api.py
```

This will guide you through secure API key configuration.

## 🛡️ Security Best Practices

- ✅ Use environment variables for secrets
- ✅ Keep .env files local only
- ✅ Use .env.example for templates
- ❌ Never commit actual API keys
- ❌ Never hardcode secrets in source code
- ❌ Never share API keys in chat/email

## 🔍 If API Key is Compromised

1. **Immediately revoke** the key in OpenAI dashboard
2. **Generate new key**
3. **Update .env file** with new key
4. **Check git history** for any accidental commits

## 💡 Mock Mode

The system works without API keys using mock responses for testing and development.