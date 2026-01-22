"""
Embedding and chunking utilities for RAG
"""
import json
from pathlib import Path
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UseChaseChunker:
    """Create embeddings-friendly chunks from use cases"""
    
    def __init__(self, use_cases_file: str = "data/processed/use_cases.json"):
        self.use_cases_file = Path(use_cases_file)
        self.chunks = []
    
    def create_chunks(self) -> List[Dict]:
        """Convert use cases into chunks optimized for retrieval"""
        
        with open(self.use_cases_file, 'r', encoding='utf-8') as f:
            use_cases = json.load(f)
        
        logger.info(f"Creating chunks from {len(use_cases)} use cases")
        
        for i, uc in enumerate(use_cases):
            # Create multiple chunk variations for better retrieval
            
            # Chunk 1: Problem-focused
            problem_chunk = {
                'chunk_id': f"{i}_problem",
                'chunk_type': 'problem',
                'text': self._create_problem_text(uc),
                'metadata': {
                    'business_problem': uc['business_problem'],
                    'data_type': uc['data_type'],
                    'source': uc.get('source', ''),
                    'url': uc.get('url', '')
                }
            }
            self.chunks.append(problem_chunk)
            
            # Chunk 2: Solution-focused
            solution_chunk = {
                'chunk_id': f"{i}_solution",
                'chunk_type': 'solution',
                'text': self._create_solution_text(uc),
                'metadata': {
                    'recommended_tech': uc['recommended_tech'],
                    'models': uc['models'],
                    'reasoning': uc['reasoning'],
                    'source': uc.get('source', ''),
                    'url': uc.get('url', '')
                }
            }
            self.chunks.append(solution_chunk)
            
            # Chunk 3: Complete use case (for comprehensive context)
            complete_chunk = {
                'chunk_id': f"{i}_complete",
                'chunk_type': 'complete',
                'text': self._create_complete_text(uc),
                'metadata': uc
            }
            self.chunks.append(complete_chunk)
        
        logger.info(f"Created {len(self.chunks)} chunks")
        return self.chunks
    
    def _create_problem_text(self, uc: Dict) -> str:
        """Create problem-focused text for embedding"""
        return f"""Business Problem: {uc['business_problem']}
Data Type: {uc['data_type']}
Context: This problem involves {uc['data_type']} data and requires AI/ML solutions."""
    
    def _create_solution_text(self, uc: Dict) -> str:
        """Create solution-focused text for embedding"""
        tech_str = ', '.join(uc['recommended_tech'])
        models_str = ', '.join(uc['models']) if uc['models'] else 'Various models'
        
        return f"""Recommended Technologies: {tech_str}
Specific Models/Approaches: {models_str}
Reasoning: {uc['reasoning']}
This solution is appropriate for problems involving {uc['data_type']} data."""
    
    def _create_complete_text(self, uc: Dict) -> str:
        """Create complete use case text for embedding"""
        tech_str = ', '.join(uc['recommended_tech'])
        models_str = ', '.join(uc['models']) if uc['models'] else 'Various models'
        
        return f"""USE CASE: {uc['business_problem']}

DATA TYPE: {uc['data_type']}

RECOMMENDED AI/ML TECHNOLOGIES: {tech_str}

SPECIFIC MODELS AND APPROACHES: {models_str}

REASONING: {uc['reasoning']}

This is a proven approach for {uc['business_problem'].lower()} problems."""
    
    def save_chunks(self, output_file: str = "data/processed/chunks.jsonl"):
        """Save chunks to file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for chunk in self.chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
        
        logger.info(f"Saved {len(self.chunks)} chunks to {output_path}")


def main():
    """Main entry point"""
    chunker = UseChaseChunker()
    chunks = chunker.create_chunks()
    chunker.save_chunks()
    
    print(f"\n{'='*60}")
    print(f"📦 Chunking Summary")
    print(f"{'='*60}")
    print(f"Total chunks created: {len(chunks)}")
    
    chunk_types = {}
    for chunk in chunks:
        chunk_type = chunk['chunk_type']
        chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
    
    print(f"\nChunks by type:")
    for chunk_type, count in chunk_types.items():
        print(f"  {chunk_type}: {count}")
    
    print(f"\n✅ Chunking complete!")


if __name__ == '__main__':
    main()
