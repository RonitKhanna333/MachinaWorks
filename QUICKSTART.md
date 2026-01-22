# AI Consultant Chatbot - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Option 1: Quick Start with Sample Data (Recommended for Testing)

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
copy .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY or OPENAI_API_KEY
```

3. **Run quick start (uses sample data, no scraping):**
```bash
python quick_start.py
```

4. **Test the chatbot:**
```bash
python src/chatbot/consultant.py --mode interactive
```

That's it! You're ready to go.

---

### Option 2: Full Pipeline with Web Scraping

If you want to scrape real data from the curated sources:

1. **Install dependencies:**
```bash
pip install -r requirements.txt
playwright install chromium
```

2. **Set up environment:**
```bash
copy .env.example .env
# Edit .env and add your API keys
```

3. **Run full pipeline:**
```bash
# Priority sources only (5 sources - fastest)
python src/pipeline.py --mode priority

# Or all sources (takes longer)
python src/pipeline.py --mode all
```

4. **Use the chatbot:**
```bash
# Interactive mode
python src/chatbot/consultant.py --mode interactive

# API server
python src/chatbot/api.py
```

---

## 📚 Usage Examples

### Interactive Mode

```bash
python src/chatbot/consultant.py --mode interactive
```

Example interaction:
```
💼 Your problem: We need to automate invoice processing from PDFs

📝 Additional context: Finance department, 10k invoices/month

🔍 Analyzing problem and searching knowledge base...

📊 RECOMMENDATION
==============================================================
[AI Consultant provides detailed recommendation with specific models, reasoning, and implementation guidance]

🎯 Confidence: High
📚 Based on 5 similar use cases
```

### API Mode

```bash
# Start server
python src/chatbot/api.py

# In another terminal, test with curl:
curl -X POST "http://localhost:8000/api/consult" \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Customer churn prediction for SaaS",
    "context": "50k users, historical usage data",
    "n_examples": 5
  }'
```

### Programmatic Usage

```python
from src.chatbot.consultant import AIConsultant

consultant = AIConsultant(llm_provider="anthropic")

result = consultant.suggest(
    problem="Real-time fraud detection in payments",
    context="Processing 1M+ transactions per day"
)

print(result['recommendations'])
print(f"Confidence: {result['confidence']}")
```

---

## 🧪 Testing

Run the test suite:
```bash
python examples/test_consultant.py
```

This tests the consultant with 5 diverse business problems covering:
- Document processing (DL + NLP)
- Churn prediction (ML)
- Recommendations (ML + DL)
- Robot navigation (RL)
- Fraud detection (ML + Anomaly Detection)

---

## 📁 Project Structure

```
ai-consul/
├── src/
│   ├── scraper/              # Web scraping modules
│   │   ├── main.py           # Orchestrator
│   │   ├── base_scraper.py   # Static/Dynamic scrapers
│   │   └── api_scrapers.py   # API-specific scrapers
│   │
│   ├── processor/            # Data processing
│   │   ├── data_processor.py # Extract use cases
│   │   └── chunker.py        # Create chunks for RAG
│   │
│   ├── embeddings/           # Vector storage
│   │   └── vector_store.py   # ChromaDB + embeddings
│   │
│   ├── chatbot/              # Chatbot interface
│   │   ├── consultant.py     # Main consultant logic
│   │   └── api.py            # FastAPI server
│   │
│   └── pipeline.py           # End-to-end orchestrator
│
├── data/
│   ├── raw/                  # Scraped data
│   ├── processed/            # Structured use cases
│   └── vectordb/             # ChromaDB storage
│
├── configs/
│   └── sources.json          # Scraping configurations
│
├── examples/
│   └── test_consultant.py    # Test examples
│
├── quick_start.py            # Quick start with sample data
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🎯 What the Chatbot Does

The AI Consultant analyzes your business problem and provides:

1. **Problem Analysis**
   - Technical reframing
   - Problem type identification
   - Data type analysis

2. **Technology Recommendations**
   - When to use ML vs DL vs RL
   - Why each approach is appropriate
   - Requirements (data, compute, expertise)

3. **Specific Models & Architectures**
   - Concrete model suggestions
   - Why each model fits
   - Alternative approaches

4. **Implementation Guidance**
   - Data requirements
   - Potential challenges
   - ROI considerations

5. **Similar Success Stories**
   - References from knowledge base
   - How they relate to your problem

---

## 🔧 Customization

### Add Your Own Data Sources

Edit `configs/sources.json` to add new sources:

```json
{
  "name": "Your Source",
  "category": "industry",
  "urls": ["https://example.com/ai-use-cases"],
  "scraping_strategy": "static",
  "selectors": {
    "title": "h1",
    "content": "article"
  }
}
```

### Change LLM Provider

```python
# Use OpenAI instead of Anthropic
consultant = AIConsultant(llm_provider="openai")
```

### Adjust Retrieval

```python
# Get more similar examples
result = consultant.suggest(
    problem="your problem",
    n_examples=10  # Default is 5
)
```

---

## 📊 Data Sources

The system learns from:

### Priority Sources (Minimal Set)
1. **Google Cloud Solutions** - Problem → Solution mappings
2. **AWS ML Use Cases** - When to use ML/DL/RL
3. **Azure AI Architectures** - End-to-end architectures
4. **DeepLearning.AI Blog** - Best practices & reasoning
5. **Hugging Face Models** - Model capabilities

### Extended Sources
- McKinsey AI Insights (business framing)
- IBM AI Use Cases (enterprise focus)
- OpenAI Research (RL explanations)
- Towards Data Science (practical guides)

---

## 🐛 Troubleshooting

### "No module named 'anthropic'"
```bash
pip install -r requirements.txt
```

### "ANTHROPIC_API_KEY not found"
```bash
# Make sure .env file exists and contains:
ANTHROPIC_API_KEY=your_key_here
```

### "Collection is empty" when running chatbot
```bash
# Run pipeline first to create embeddings
python quick_start.py
# OR
python src/pipeline.py --mode priority
```

### Scraping fails with timeout
```bash
# Increase timeout in configs/sources.json
"timeout": 60  # seconds
```

---

## 🚀 Next Steps

1. **Try it out** - Run quick_start.py and test with examples
2. **Add real data** - Run the full scraping pipeline
3. **Customize sources** - Add your industry-specific sources
4. **Deploy** - Run as API server for integration
5. **Evaluate** - Test accuracy with your domain problems

---

## 💡 Tips

- Start with **quick_start.py** to test everything works
- Use **priority mode** for faster initial setup (5 sources)
- The chatbot gets better with more diverse data sources
- Add industry-specific sources for your domain
- Review and curate scraped data for best results

---

## 📝 License

MIT License - feel free to use and modify!

---

**Need help?** Check the examples/ directory for more usage patterns.
