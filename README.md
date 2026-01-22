# AI Consultation Chatbot

A specialized chatbot that suggests appropriate AI/ML/DL/RL techniques based on business problems and use cases.

## Features

- **Web Scraping Pipeline**: Collects curated content from cloud providers, industry leaders, and AI research sources
- **Intelligent Chunking**: Structures scraped data into problem → solution mappings
- **HuggingFace Embeddings**: State-of-the-art sentence transformers for semantic search
- **ChromaDB Vector Store**: Fast, persistent vector database for similarity search
- **RAG (Retrieval Augmented Generation)**: Uses vector similarity search to find relevant use cases
- **Smart Reasoning**: Analyzes business problems and suggests appropriate AI techniques with justification

## Data Sources

### Priority Sources (Minimal Set)
1. Google Cloud Use Cases
2. AWS ML Use Cases  
3. Azure AI Architectures
4. DeepLearning.AI Blog
5. Hugging Face Model Cards

### Extended Sources
- McKinsey AI Insights
- IBM AI Use Cases
- OpenAI Research
- Towards Data Science

## Project Structure

```
ai-consul/
├── src/
│   ├── scraper/           # Web scraping modules
│   ├── processor/         # Data chunking & structuring
│   ├── embeddings/        # Vector embeddings & storage
│   ├── chatbot/           # RAG pipeline & LLM interface
│   └── utils/             # Helper functions
├── data/
│   ├── raw/               # Raw scraped content
│   ├── processed/         # Structured chunks
│   └── vectordb/          # Vector database storage
├── configs/
│   └── sources.json       # Scraping source configurations
├── requirements.txt
└── .env

```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the scraper:
```bash
python src/scraper/main.py
```

4. Process and embed data:
```bash
python src/processor/chunk_and_embed.py
```

5. Start the chatbot:
```bash
python src/chatbot/main.py
```

## Usage

```python
from src.chatbot import AIConsultant

consultant = AIConsultant()
response = consultant.suggest(
    problem="We need to automate invoice processing from PDFs",
    context="Finance department, 10k invoices/month"
)
print(response)
```

## Output Format

The chatbot provides structured recommendations:
- **Problem Analysis**: Understanding of the business problem
- **Recommended Techniques**: AI/ML/DL/RL suggestions
- **Specific Models/Architectures**: Concrete implementations
- **Reasoning**: Why these techniques are appropriate
- **References**: Similar use cases from knowledge base
