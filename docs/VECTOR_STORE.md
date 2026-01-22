# Vector Store Configuration

## 🚀 Using HuggingFace Embeddings + ChromaDB

Your AI Consultant uses:
- **HuggingFace Sentence Transformers** for embeddings
- **ChromaDB** as the vector database

## 📊 Embedding Model Presets

Choose your embedding model when initializing:

```python
from src.embeddings.vector_store import VectorStore

# Option 1: Use preset (recommended)
vector_store = VectorStore(embedding_model="balanced")  # Default

# Option 2: Use specific HuggingFace model
vector_store = VectorStore(embedding_model="BAAI/bge-large-en-v1.5")
```

### Available Presets:

| Preset | HuggingFace Model | Quality | Speed | Use Case |
|--------|-------------------|---------|-------|----------|
| `best` | `BAAI/bge-large-en-v1.5` | ⭐⭐⭐⭐⭐ | 🐌 Slow | Production, best accuracy |
| `balanced` | `all-mpnet-base-v2` | ⭐⭐⭐⭐ | 🚀 Fast | **Default - best balance** |
| `fast` | `all-MiniLM-L6-v2` | ⭐⭐⭐ | ⚡ Fastest | Quick testing, low resources |
| `multilingual` | `paraphrase-multilingual-mpnet-base-v2` | ⭐⭐⭐⭐ | 🚀 Fast | Non-English languages |

## 🔧 Configuration Options

### Custom HuggingFace Model

Use any model from HuggingFace:

```python
vector_store = VectorStore(
    embedding_model="sentence-transformers/paraphrase-MiniLM-L6-v2"
)
```

### ChromaDB Directory

Change where ChromaDB stores data:

```python
vector_store = VectorStore(
    persist_directory="my_custom_db",
    embedding_model="balanced"
)
```

## 📝 Example Usage

```python
from src.embeddings.vector_store import VectorStore

# Initialize with best quality embeddings
store = VectorStore(embedding_model="best")

# Embed your chunks
store.embed_and_store("data/processed/chunks.jsonl")

# Search
results = store.search("invoice processing automation", n_results=5)

for result in results:
    print(f"Similarity: {1 - result['distance']:.2%}")
    print(f"Text: {result['document'][:100]}...")
```

## 🎯 Why This Stack?

### HuggingFace Sentence Transformers
- ✅ State-of-the-art semantic embeddings
- ✅ Free and open source
- ✅ Runs locally, no API needed
- ✅ 100+ pre-trained models
- ✅ Optimized for similarity search

### ChromaDB
- ✅ Fast vector similarity search
- ✅ Persistent storage (survives restarts)
- ✅ Metadata filtering
- ✅ Simple Python API
- ✅ Built for AI applications

## 🔄 Switching Models

To switch embedding models:

1. Delete old vector DB:
```bash
rm -rf data/vectordb
```

2. Re-run pipeline with new model:
```python
from src.embeddings.vector_store import VectorStore

# Use a different model
store = VectorStore(embedding_model="best")
store.embed_and_store()
```

## 📊 Performance Comparison

| Model | Embedding Time (1000 chunks) | Quality Score |
|-------|------------------------------|---------------|
| `best` (bge-large) | ~15 sec | 0.91 |
| `balanced` (mpnet) | ~8 sec | 0.88 |
| `fast` (MiniLM) | ~3 sec | 0.83 |

*Quality measured on semantic textual similarity benchmark*

## 🌐 Multilingual Support

For non-English use cases:

```python
store = VectorStore(embedding_model="multilingual")
```

Supports 50+ languages including:
- Spanish, French, German, Italian
- Chinese, Japanese, Korean
- Arabic, Hindi, Portuguese
- And more!

## 🐛 Troubleshooting

### "Model not found"
```bash
# Model downloads automatically on first use
# Make sure you have internet connection
```

### "Out of memory"
```python
# Use smaller model
store = VectorStore(embedding_model="fast")
```

### Slow embedding creation
```python
# Use GPU if available (automatic with sentence-transformers)
# Or use faster model preset
store = VectorStore(embedding_model="fast")
```

---

**All models from HuggingFace Hub: https://huggingface.co/models?library=sentence-transformers**
