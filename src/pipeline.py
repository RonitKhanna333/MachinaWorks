"""
End-to-end pipeline orchestrator
Runs the complete pipeline: scrape -> process -> embed -> ready for chatbot
"""
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_pipeline(mode: str = 'priority', skip_scraping: bool = False):
    """
    Run the complete pipeline
    
    Args:
        mode: 'priority' (5 sources) or 'all' (all sources)
        skip_scraping: Skip scraping if data already exists
    """
    
    print("\n" + "="*80)
    print("🚀 AI CONSULTANT BOT - COMPLETE PIPELINE")
    print("="*80 + "\n")
    
    # Step 1: Scraping (optional)
    if not skip_scraping:
        print("\n📡 STEP 1/4: Web Scraping")
        print("-" * 80)
        
        from scraper.main import ScraperOrchestrator
        
        orchestrator = ScraperOrchestrator()
        
        if mode == 'priority':
            logger.info("Scraping priority sources (5 sources)")
            orchestrator.scrape_priority_sources()
        else:
            logger.info("Scraping all sources")
            orchestrator.scrape_all_sources()
        
        print("✅ Scraping complete\n")
    else:
        print("\n⏭️  STEP 1/4: Skipping scraping (using existing data)\n")
    
    # Step 2: Data Processing
    print("\n🔧 STEP 2/4: Data Processing & Chunking")
    print("-" * 80)
    
    from processor.data_processor import DataProcessor
    from processor.chunker import UseChaseChunker
    
    # Process raw data into use cases
    processor = DataProcessor()
    use_cases = processor.process_all()
    
    # Create chunks for embedding
    chunker = UseChaseChunker()
    chunks = chunker.create_chunks()
    chunker.save_chunks()
    
    print(f"✅ Processed {len(use_cases)} use cases into {len(chunks)} chunks\n")
    
    # Step 3: Embedding & Vector Storage
    print("\n🧠 STEP 3/4: Creating Embeddings & Vector Storage")
    print("-" * 80)
    
    from embeddings.vector_store import VectorStore
    
    vector_store = VectorStore()
    vector_store.embed_and_store()
    
    stats = vector_store.get_collection_stats()
    print(f"✅ Stored {stats['total_chunks']} embeddings in vector database\n")
    
    # Step 4: Verify Setup
    print("\n✅ STEP 4/4: Verification")
    print("-" * 80)
    
    print("\n📊 Pipeline Summary:")
    print(f"   • Use cases extracted: {len(use_cases)}")
    print(f"   • Chunks created: {len(chunks)}")
    print(f"   • Embeddings stored: {stats['total_chunks']}")
    
    print("\n🎉 Pipeline complete! Your AI Consultant is ready to use.")
    print("\n📝 Next steps:")
    print("   1. Set your API keys in .env file (ANTHROPIC_API_KEY or OPENAI_API_KEY)")
    print("   2. Run interactive chatbot: python src/chatbot/consultant.py")
    print("   3. Or start API server: python src/chatbot/api.py")
    print("   4. Test with: python examples/test_consultant.py")
    print("\n" + "="*80 + "\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Consultant Bot - Pipeline')
    parser.add_argument(
        '--mode',
        choices=['priority', 'all'],
        default='priority',
        help='Scraping mode: priority (5 sources) or all sources'
    )
    parser.add_argument(
        '--skip-scraping',
        action='store_true',
        help='Skip scraping and use existing data'
    )
    
    args = parser.parse_args()
    
    try:
        run_pipeline(mode=args.mode, skip_scraping=args.skip_scraping)
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
