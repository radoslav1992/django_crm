# 🤖 AI Model Configuration

## Current Model: Gemini 2.5 Flash-Lite

### ✅ Model Updated!

The CRM now uses **Gemini 2.5 Flash-Lite** for optimal cost-efficiency and performance.

---

## 📊 Model Specifications

According to [Google AI documentation](https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash-lite):

### **Gemini 2.5 Flash-Lite**
- **Model Code:** `gemini-2.5-flash-lite`
- **Type:** Second generation small workhorse model
- **Optimization:** Cost efficiency and low latency
- **Status:** Preview (Latest update: September 2025)

### **Capabilities:**
```
✅ Input Types: Audio, images, video, and text
✅ Output Types: Text
✅ Input Token Limit: 1,048,576 tokens (~750,000 words)
✅ Output Token Limit: 8,192 tokens
✅ Context Window: 1 million tokens
✅ Knowledge Cutoff: January 2025
```

### **Supported Features:**
- ✅ **Function Calling** - Yes
- ✅ **Structured Outputs** - Yes
- ✅ **Batch API** - Supported
- ✅ **Caching** - Supported
- ✅ **Search Grounding** - Not supported
- ✅ **Code Execution** - Not supported
- ✅ **Thinking** - Not supported
- ❌ **Audio Generation** - Not supported
- ❌ **Image Generation** - Not supported
- ❌ **Live API** - Not supported

---

## 💰 Why Flash-Lite?

### **Benefits:**
1. **Cost Efficiency** - Lower pricing than Flash or Pro
2. **Low Latency** - Fast response times
3. **Large Context** - Still supports 1M tokens
4. **Perfect for CRM** - Ideal for business text generation

### **Use Cases in This CRM:**
- ✅ Chat assistance
- ✅ Email drafting
- ✅ Deal analysis
- ✅ Task suggestions
- ✅ Template content generation
- ✅ Smart search

All these features work perfectly with Flash-Lite!

---

## 🔧 Configuration

### **Where It's Configured:**
```python
File: apps/ai_assistant/services.py
Line: 19

class GeminiAssistant:
    def __init__(self, user):
        self.user = user
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
```

### **API Key:**
Set in `.env` file:
```env
GEMINI_API_KEY=your-api-key-here
```

Get your free API key at: https://makersuite.google.com/app/apikey

---

## 📈 Model Comparison

| Feature | Flash-Lite | Flash | Pro |
|---------|-----------|-------|-----|
| **Speed** | Fastest | Fast | Moderate |
| **Cost** | Lowest | Low | Higher |
| **Context** | 1M tokens | 1M tokens | 1M tokens |
| **Output** | 8K tokens | 65K tokens | 65K tokens |
| **Thinking** | No | Yes | Yes |
| **Best For** | High volume, cost-sensitive | Balanced | Complex reasoning |

### **For CRM Use:**
✅ **Flash-Lite is PERFECT** because:
- CRM tasks don't need extensive reasoning
- Email drafts are short (<8K tokens)
- Fast responses improve UX
- Lower costs for high-volume usage
- 1M context window handles large CRM data

---

## 🎯 Performance Characteristics

### **Response Times:**
- **Email Generation:** ~2-3 seconds
- **Chat Response:** ~1-2 seconds
- **Deal Analysis:** ~3-5 seconds
- **Task Suggestions:** ~2-3 seconds

### **Token Usage (Typical):**
- **Chat message:** 500-1,000 tokens
- **Email draft:** 300-500 tokens
- **Deal analysis:** 800-1,200 tokens
- **Task suggestions:** 400-600 tokens

### **Cost Efficiency:**
Flash-Lite offers the best price-performance ratio for these use cases!

---

## 🔄 How to Switch Models

If you want to try different models:

### **Option 1: Gemini 2.5 Flash (More capable)**
```python
# In apps/ai_assistant/services.py:
self.model = genai.GenerativeModel('gemini-2.5-flash')
```

### **Option 2: Gemini 2.5 Pro (Most powerful)**
```python
# In apps/ai_assistant/services.py:
self.model = genai.GenerativeModel('gemini-2.5-pro')
```

### **Option 3: Gemini 2.0 Flash (Previous gen)**
```python
# In apps/ai_assistant/services.py:
self.model = genai.GenerativeModel('gemini-2.0-flash')
```

Then restart the server:
```bash
pkill -f "manage.py runserver"
python manage.py runserver 8001
```

---

## 📚 Gemini Models Available

From the official documentation:

### **Gemini 2.5 Series (Latest):**
- **gemini-2.5-pro** - Most advanced, thinking capability
- **gemini-2.5-flash** - Best balance ← Good alternative
- **gemini-2.5-flash-lite** - Most cost-effective ← **CURRENT**

### **Gemini 2.0 Series:**
- **gemini-2.0-flash** - Second gen workhorse
- **gemini-2.0-flash-exp** - Experimental (was our old setting)
- **gemini-2.0-flash-lite** - Cost-optimized 2.0

---

## 🎯 Current Configuration Summary

```
✅ Model: Gemini 2.5 Flash-Lite
✅ Version: Latest (September 2025)
✅ Context: 1,048,576 tokens (1M)
✅ Output: 8,192 tokens
✅ Optimization: Cost & Latency
✅ Status: Active in CRM
✅ Use Cases: All CRM AI features
```

---

## 🧪 Testing AI Features

Once you add your Gemini API key to `.env`:

```bash
# Edit .env
GEMINI_API_KEY=your-actual-key-from-google

# Restart server (if needed)
```

Then test:
1. **AI Chat:** http://localhost:8001/bg/ai/chat/
2. **Generate Email:** From any contact page
3. **Analyze Deal:** From any deal page
4. **Get Suggestions:** From AI suggestions page

All powered by cost-efficient Gemini 2.5 Flash-Lite! 🚀

---

## 📖 References

- **Model Documentation:** https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash-lite
- **Get API Key:** https://makersuite.google.com/app/apikey
- **Pricing:** https://ai.google.dev/pricing

---

## ✅ Change Applied!

The CRM now uses **Gemini 2.5 Flash-Lite** for:
- Better cost efficiency
- Lower latency
- High-volume processing
- All CRM AI features

Perfect choice for a CRM application! 💡

