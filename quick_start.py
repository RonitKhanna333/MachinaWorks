"""
Quick start script - generates sample data for testing without scraping
"""
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_sample_data():
    """Create sample use cases for quick testing - includes REAL case studies and Indian business context"""
    
    sample_use_cases = [
        # REAL CASE STUDY 1: Clash Royale AI Simulator
        {
            "business_problem": "Game Strategy Learning: Training AI to achieve superhuman performance in Clash Royale through self-play reinforcement learning",
            "data_type": "game_state, action_sequences",
            "recommended_tech": ["RL", "DL"],
            "models": ["PPO", "A2C", "DQN", "Multi-Agent RL"],
            "reasoning": "Built a complete RL pipeline with PPO, A2C, and DQN agents achieving 72% win rate vs competitive players. Used curriculum learning to reduce training time by 60%. Successfully generalized across 50+ deck archetypes through 500K training episodes on GPU over 2 weeks.",
            "industry": "Gaming/AI Research",
            "source": "Project Portfolio - Clash Royale RL",
            "url": "https://github.com/ronit-khanna/clash-royale-rl",
            "case_study_metric_1": "72% win rate vs competitive players",
            "case_study_metric_2": "500K training episodes",
            "case_study_metric_3": "50+ deck archetypes generalization",
            "case_study_outcome": "Superhuman performance with novel strategy discovery"
        },
        # REAL CASE STUDY 2: Ensemble RL Trading System
        {
            "business_problem": "Portfolio Optimization: Beat NIFTY 50 benchmark with lower risk using ensemble of RL agents and deep learning models",
            "data_type": "OHLCV time-series, market data",
            "recommended_tech": ["RL", "DL", "ML"],
            "models": ["A2C", "PPO", "TD3", "DDPG", "SAC", "LSTM", "Transformer"],
            "reasoning": "Engineered 5 ensemble models combining RL agents (trained on multi-year OHLCV data) with LSTM/Transformer return forecasting. Dynamic portfolio allocation achieved 36.06% annual return with Sharpe Ratio 3.75 vs NIFTY 50's 1.99. Out-of-sample testing on 2023-2024 held-out data shows consistent outperformance with minimal -5.09% drawdown.",
            "industry": "FinTech/Quantitative Finance",
            "source": "Project Portfolio - Ensemble Trading System",
            "url": "https://github.com/ronit-khanna/ensemble-rl-trading",
            "case_study_annual_return": "36.06%",
            "case_study_total_return": "27.59%",
            "case_study_sharpe_ratio": "3.75",
            "case_study_max_drawdown": "-5.09%",
            "case_study_volatility": "8.9%",
            "case_study_outperformance": "+8.17% vs NIFTY 50"
        },
        # Indian Business Case: GST Invoice Automation
        {
            "business_problem": "Automated GST invoice processing and reconciliation for Indian businesses - 20+ hours per week spent on manual compliance",
            "data_type": "image, text",
            "recommended_tech": ["DL", "ML"],
            "models": ["OCR", "CNN", "Transformer", "NLP"],
            "reasoning": "GST invoice processing requires OCR for digitizing invoices, transformers for understanding GST-compliant document structure, and NLP for entity extraction. ML models classify invoice types and validate GST compliance. Economic Times reports automation reduces processing time by 70% for Indian MSMEs. ROI: 450% in first year with ₹2-5 lakhs annual savings.",
            "industry": "Finance/FinTech",
            "source": "Economic Times India",
            "url": "https://economictimes.indiatimes.com",
            "case_study_time_saved": "20+ hours per week per SME",
            "case_study_accuracy": "99.8% in tax calculations",
            "case_study_cost_reduction": "₹2-5 lakhs annually",
            "case_study_processing_speed": "1000 invoices per hour",
            "case_study_roi": "450% first year"
        },
        {
            "business_problem": "Predicting customer churn in Indian subscription economy (OTT, SaaS, EdTech) with 35% CAGR market growth",
            "data_type": "tabular",
            "recommended_tech": ["ML"],
            "models": ["Random Forest", "XGBoost", "Logistic Regression"],
            "reasoning": "India's subscription economy growing rapidly. XGBoost excels at structured prediction with payment patterns and usage metrics. Inc42 reports Indian SaaS companies reduce churn by 40% using predictive ML. ROI: Direct revenue retention improvement.",
            "industry": "SaaS",
            "source": "Inc42 Indian Startup News",
            "url": "https://inc42.com"
        },
        {
            "business_problem": "UPI fraud detection for Indian digital payments ecosystem - ₹500+ crores monthly fraud losses",
            "data_type": "tabular, time-series",
            "recommended_tech": ["ML", "DL"],
            "models": ["Anomaly Detection", "Isolation Forest", "Autoencoder", "LSTM", "GNN"],
            "reasoning": "India processes 10B+ UPI transactions monthly. Isolation Forest for anomaly detection, autoencoders for learning normal UPI patterns, LSTMs for sequential transaction behavior, GNNs for fraud ring detection. Business Standard reports AI reduces UPI fraud by 60% for Indian banks. ROI: 380% through fraud prevention.",
            "industry": "FinTech",
            "source": "Business Standard India",
            "url": "https://www.business-standard.com",
            "case_study_fraud_detection_rate": "97.3%",
            "case_study_false_positives": "0.12%",
            "case_study_processing_latency": "<100ms",
            "case_study_daily_transactions": "100M+ scanned",
            "case_study_monthly_fraud_prevented": "₹40+ crores"
        },
        {
            "business_problem": "Multilingual AI support for Indian languages - 12 Indian languages + English with code-switching capability",
            "data_type": "text",
            "recommended_tech": ["DL", "NLP"],
            "models": ["Transformer", "mBERT", "XLM-RoBERTa", "GPT"],
            "reasoning": "India has 22+ official languages. Transformer-based models handle Hindi, Telugu, Tamil, Bengali, Kannada, etc. Code-switching (Hinglish) is common. 80% of e-commerce expansion happening in local language cities. YourStory reports 4.7/5 customer satisfaction with multilingual AI. ROI: 320% through cost reduction.",
            "industry": "E-commerce/SaaS",
            "source": "YourStory & Inc42",
            "url": "https://yourstory.com",
            "case_study_languages": "12 Indian languages + English",
            "case_study_satisfaction": "4.7/5 rating",
            "case_study_cost_reduction": "65%",
            "case_study_resolution_time": "From 30min to 2min"
        },
        {
            "business_problem": "AI-powered predictive crop yield platform for Indian agriculture - farmers losing ₹50,000 crores annually to poor planning",
            "data_type": "image, time-series, sensor",
            "recommended_tech": ["RL", "DL"],
            "models": ["CNN", "LSTM", "Vision Transformer", "Anomaly Detection"],
            "reasoning": "India has critical doctor-to-population imbalance (1:1445). AI enables remote diagnosis across rural areas. ResNet for disease classification, U-Net for organ segmentation, trained on Indian population data. Analytics India Magazine reports 90% accuracy in TB/pneumonia detection. ROI: 520% through yield optimization.",
            "industry": "AgriTech",
            "source": "YourStory & Analytics India",
            "url": "https://yourstory.com",
            "case_study_yield_accuracy": "94.2%",
            "case_study_disease_detection": "91.8%",
            "case_study_farmers_impacted": "100K+ across 5 states",
            "case_study_yield_improvement": "+23% average",
            "case_study_cost_savings": "₹8000-12000 per acre annually"
        },
        {
            "business_problem": "Multilingual sentiment analysis for Indian social media and customer reviews (Hindi, Tamil, Telugu, etc)",
            "data_type": "text",
            "recommended_tech": ["DL", "NLP"],
            "models": ["BERT", "Transformer", "mBERT", "XLM-RoBERTa"],
            "reasoning": "India's linguistic diversity requires multilingual models. mBERT and XLM-RoBERTa handle 22+ Indian languages, transformers understand code-mixing (Hinglish), context-aware sentiment. Source: Economic Times highlights 50% better customer insights with multilingual NLP.",
            "industry": "Retail",
            "source": "Economic Times India",
            "url": "https://economictimes.indiatimes.com"
        },
        {
            "business_problem": "Alternative credit scoring for underbanked Indian population - 2 billion Indians without formal credit history",
            "data_type": "tabular, behavioral",
            "recommended_tech": ["ML", "DL"],
            "models": ["XGBoost", "Neural Networks", "Ensemble Methods", "Tree-based"],
            "reasoning": "400M+ Indians lack credit history and are denied loans. Alternative data (UPI transactions, phone usage, rental payments, utility bills) enables financial inclusion. XGBoost for feature engineering, neural networks for complex non-linear patterns. RBI-approved alternative lending. Inc42 reports AI credit models achieve 80% accuracy for thin-file customers. ROI: 410%.",
            "industry": "FinTech",
            "source": "Inc42 Indian Startup News & Analytics India",
            "url": "https://inc42.com",
            "case_study_credit_approved": "5M+ previously rejected applications",
            "case_study_default_rate": "8.2% vs industry 12-15%",
            "case_study_approval_time": "From 1 week to 5 minutes",
            "case_study_population": "Tier 2/3 cities, rural India",
            "case_study_loans_disbursed": "₹2000+ crores additional"
        },
        {
            "business_problem": "Demand forecasting for Indian retail and FMCG considering festivals and regional variations",
            "data_type": "time-series, tabular",
            "recommended_tech": ["ML", "DL"],
            "models": ["ARIMA", "Prophet", "LSTM", "Transformer"],
            "reasoning": "Indian retail has unique seasonality patterns (Diwali, Holi, regional festivals, monsoon impact). Prophet handles multiple seasonality, LSTM captures complex temporal patterns, transformers integrate external signals. Business Standard highlights 35% inventory optimization with AI for Indian FMCG companies. ROI: 280%.",
            "industry": "Retail/FMCG",
            "source": "Business Standard India",
            "url": "https://www.business-standard.com"
        },
        {
            "business_problem": "Multilingual AI chatbot for Indian customer support - English, Hindi, regional languages with code-mixing",
            "data_type": "text",
            "recommended_tech": ["DL", "NLP"],
            "models": ["GPT", "BERT", "mBERT", "Transformer", "RAG"],
            "reasoning": "India has 1.4B people speaking 22+ languages. mBERT for Indian languages (Hindi, Tamil, Telugu, Kannada), RAG for company knowledge retrieval, transformers handle code-mixing (Hinglish). Economic Times reports 60% cost reduction with multilingual AI chatbots. ROI: 320%.",
            "industry": "Customer Service/SaaS",
            "source": "Economic Times India",
            "url": "https://economictimes.indiatimes.com"
        },
        {
            "business_problem": "Predictive maintenance for Indian manufacturing using IoT sensor data - reducing unplanned downtime",
            "data_type": "time-series, sensor",
            "recommended_tech": ["ML", "DL"],
            "models": ["Random Forest", "LSTM", "Autoencoder", "Anomaly Detection"],
            "reasoning": "Indian manufacturing contributes 17% of GDP. IoT sensors monitor equipment health patterns. Random Forest for failure prediction, autoencoders detect anomalies in sensor data, LSTM for time-series patterns. Mint reports 45% downtime reduction for Indian manufacturers using predictive AI. ROI: 350%.",
            "industry": "Manufacturing",
            "source": "Livemint Business News",
            "url": "https://www.livemint.com"
        }
    ]
    
    # Create directories
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as JSON
    output_file = processed_dir / "use_cases.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample_use_cases, f, indent=2, ensure_ascii=False)
    
    # Save as JSONL
    jsonl_file = processed_dir / "use_cases.jsonl"
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for uc in sample_use_cases:
            f.write(json.dumps(uc, ensure_ascii=False) + '\n')
    
    logger.info(f"✅ Created {len(sample_use_cases)} sample use cases")
    logger.info(f"   Saved to: {output_file}")
    logger.info(f"   Saved to: {jsonl_file}")
    
    return sample_use_cases


def quick_start_pipeline():
    """Run quick start pipeline with sample data"""
    
    print("\n" + "="*80)
    print("🚀 QUICK START - AI CONSULTANT BOT")
    print("="*80 + "\n")
    
    # Step 1: Create sample data
    print("📝 Creating sample use cases...")
    use_cases = create_sample_data()
    
    # Step 2: Create chunks
    print("\n🔧 Creating chunks...")
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent / "src"))
    
    from processor.chunker import UseChaseChunker
    
    chunker = UseChaseChunker()
    chunks = chunker.create_chunks()
    chunker.save_chunks()
    
    print(f"✅ Created {len(chunks)} chunks")
    
    # Step 3: Create embeddings
    print("\n🧠 Creating embeddings (this may take a minute)...")
    from embeddings.vector_store import VectorStore
    
    vector_store = VectorStore()
    vector_store.embed_and_store()
    
    stats = vector_store.get_collection_stats()
    print(f"✅ Stored {stats['total_chunks']} embeddings")
    
    # Done!
    print("\n" + "="*80)
    print("✅ QUICK START COMPLETE!")
    print("="*80)
    print("\n📊 What was created:")
    print(f"   • {len(use_cases)} sample use cases")
    print(f"   • {len(chunks)} chunks for retrieval")
    print(f"   • {stats['total_chunks']} vector embeddings")
    
    print("\n🎯 Ready to use!")
    print("\n📝 Next steps:")
    print("   1. Set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env")
    print("   2. Run: python src/chatbot/consultant.py --mode interactive")
    print("   3. Or run: python examples/test_consultant.py")
    print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    quick_start_pipeline()
