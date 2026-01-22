"""
Data processing and chunking system
Converts raw scraped data into structured problem->solution mappings
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AIUseCase:
    """Structured representation of an AI use case"""
    business_problem: str
    data_type: str
    recommended_tech: List[str]  # ['ML', 'DL', 'RL']
    models: List[str]  # Specific models/architectures
    reasoning: str  # Why these techniques are appropriate
    industry: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    additional_context: Optional[Dict] = None
    
    def to_dict(self):
        return asdict(self)


class DataProcessor:
    """Process raw scraped data into structured use cases"""
    
    # Keywords for identifying AI/ML/DL/RL
    TECH_KEYWORDS = {
        'ML': ['machine learning', 'ml', 'supervised', 'unsupervised', 'classification', 
               'regression', 'clustering', 'random forest', 'svm', 'decision tree',
               'xgboost', 'gradient boosting', 'linear regression', 'logistic regression'],
        'DL': ['deep learning', 'dl', 'neural network', 'cnn', 'rnn', 'lstm', 'gru',
               'transformer', 'bert', 'gpt', 'attention', 'encoder', 'decoder',
               'resnet', 'vgg', 'yolo', 'unet', 'gan', 'autoencoder'],
        'RL': ['reinforcement learning', 'rl', 'policy', 'reward', 'agent', 'environment',
               'q-learning', 'dqn', 'ppo', 'a3c', 'actor-critic', 'markov decision'],
        'NLP': ['nlp', 'natural language', 'text', 'sentiment', 'translation', 
                'named entity', 'tokenization', 'embeddings', 'language model']
    }
    
    # Data type indicators
    DATA_TYPE_KEYWORDS = {
        'text': ['text', 'document', 'nlp', 'language', 'sentiment', 'chat', 'email'],
        'image': ['image', 'vision', 'photo', 'visual', 'ocr', 'face', 'object detection'],
        'video': ['video', 'stream', 'frame', 'motion'],
        'audio': ['audio', 'speech', 'voice', 'sound'],
        'tabular': ['tabular', 'structured', 'database', 'csv', 'spreadsheet', 'sql'],
        'time-series': ['time series', 'temporal', 'sequential', 'forecasting', 'prediction'],
        'graph': ['graph', 'network', 'relationship', 'connected'],
        'unstructured': ['unstructured', 'raw', 'mixed']
    }
    
    def __init__(self, raw_data_dir: str = "data/raw", output_dir: str = "data/processed"):
        self.raw_data_dir = Path(raw_data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process_all(self):
        """Process all raw data files"""
        use_cases = []
        
        for source_dir in self.raw_data_dir.iterdir():
            if source_dir.is_dir():
                logger.info(f"Processing source: {source_dir.name}")
                use_cases.extend(self._process_source_dir(source_dir))
        
        # Save all use cases
        self._save_use_cases(use_cases)
        
        logger.info(f"✅ Processed {len(use_cases)} use cases")
        return use_cases
    
    def _process_source_dir(self, source_dir: Path) -> List[AIUseCase]:
        """Process all files from a single source"""
        use_cases = []
        
        for file_path in source_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract use cases based on source type
                extracted = self._extract_use_cases(data)
                use_cases.extend(extracted)
                
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
        
        return use_cases
    
    def _extract_use_cases(self, data: Dict) -> List[AIUseCase]:
        """Extract use cases from raw scraped data"""
        use_cases = []
        
        source = data.get('source', 'unknown')
        url = data.get('url', '')
        content = data.get('content', {})
        
        # Process sections
        sections = content.get('sections', [])
        
        for section in sections:
            heading = section.get('heading', '')
            section_content = section.get('content', [])
            
            # Check if this section describes a use case
            if self._is_use_case_section(heading, section_content):
                use_case = self._create_use_case(
                    heading, 
                    section_content, 
                    source, 
                    url
                )
                if use_case:
                    use_cases.append(use_case)
        
        # Also check extracted patterns
        extracted_patterns = data.get('extracted_patterns', {})
        if extracted_patterns:
            pattern_use_cases = self._extract_from_patterns(
                extracted_patterns, 
                source, 
                url
            )
            use_cases.extend(pattern_use_cases)
        
        return use_cases
    
    def _is_use_case_section(self, heading: str, content: List[str]) -> bool:
        """Check if a section describes a use case"""
        use_case_indicators = [
            'use case', 'solution', 'application', 'example', 
            'scenario', 'problem', 'challenge', 'implementation'
        ]
        
        heading_lower = heading.lower()
        return any(indicator in heading_lower for indicator in use_case_indicators)
    
    def _create_use_case(
        self, 
        heading: str, 
        content: List[str], 
        source: str, 
        url: str
    ) -> Optional[AIUseCase]:
        """Create structured use case from section content"""
        
        # Combine content
        full_text = f"{heading}\n" + "\n".join(content)
        text_lower = full_text.lower()
        
        # Extract business problem (usually in heading or first paragraph)
        business_problem = heading if heading else content[0] if content else "Unknown problem"
        
        # Identify data types
        data_types = []
        for data_type, keywords in self.DATA_TYPE_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                data_types.append(data_type)
        
        data_type = ', '.join(data_types) if data_types else 'unstructured'
        
        # Identify recommended technologies
        recommended_tech = []
        for tech, keywords in self.TECH_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                if tech not in recommended_tech:
                    recommended_tech.append(tech)
        
        if not recommended_tech:
            # Default to ML if AI is mentioned
            if 'ai' in text_lower or 'artificial intelligence' in text_lower:
                recommended_tech = ['ML']
        
        # Extract specific models/architectures
        models = self._extract_models(full_text)
        
        # Extract reasoning
        reasoning = self._extract_reasoning(content)
        
        # Only create use case if we have meaningful information
        if recommended_tech or models:
            return AIUseCase(
                business_problem=business_problem,
                data_type=data_type,
                recommended_tech=recommended_tech,
                models=models,
                reasoning=reasoning,
                source=source,
                url=url
            )
        
        return None
    
    def _extract_models(self, text: str) -> List[str]:
        """Extract specific model names and architectures"""
        models = []
        text_lower = text.lower()
        
        # Common models and architectures
        model_names = [
            'bert', 'gpt', 'transformer', 'resnet', 'vgg', 'yolo',
            'lstm', 'gru', 'cnn', 'rnn', 'unet', 'gan', 'vae',
            'xgboost', 'random forest', 'svm', 'decision tree',
            'linear regression', 'logistic regression', 'k-means',
            'dbscan', 'pca', 'autoencoder', 'attention'
        ]
        
        for model in model_names:
            if model in text_lower:
                models.append(model.upper() if len(model) <= 4 else model.title())
        
        return list(set(models))
    
    def _extract_reasoning(self, content: List[str]) -> str:
        """Extract reasoning or explanation for why this approach works"""
        reasoning_keywords = ['because', 'why', 'advantage', 'benefit', 'suitable', 
                             'appropriate', 'effective', 'enables', 'allows']
        
        reasoning_sentences = []
        
        for paragraph in content:
            sentences = re.split(r'[.!?]+', paragraph)
            for sentence in sentences:
                if any(kw in sentence.lower() for kw in reasoning_keywords):
                    reasoning_sentences.append(sentence.strip())
        
        return ' '.join(reasoning_sentences[:3]) if reasoning_sentences else "Appropriate for this use case"
    
    def _extract_from_patterns(
        self, 
        patterns: Dict, 
        source: str, 
        url: str
    ) -> List[AIUseCase]:
        """Extract use cases from pattern-matched content"""
        use_cases = []
        
        problems = patterns.get('problem', [])
        solutions = patterns.get('solution', [])
        
        # Match problems with solutions
        for i, problem_item in enumerate(problems):
            if i < len(solutions):
                solution_item = solutions[i]
                
                problem_text = problem_item.get('context', '')
                solution_text = solution_item.get('context', '')
                
                combined_text = f"{problem_text}\n{solution_text}"
                
                use_case = self._create_use_case(
                    problem_item.get('keyword', 'Use case'),
                    [problem_text, solution_text],
                    source,
                    url
                )
                
                if use_case:
                    use_cases.append(use_case)
        
        return use_cases
    
    def _save_use_cases(self, use_cases: List[AIUseCase]):
        """Save processed use cases to JSON"""
        output_file = self.output_dir / "use_cases.json"
        
        use_cases_dict = [uc.to_dict() for uc in use_cases]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(use_cases_dict, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(use_cases)} use cases to {output_file}")
        
        # Also save as JSONL for easy loading
        jsonl_file = self.output_dir / "use_cases.jsonl"
        with open(jsonl_file, 'w', encoding='utf-8') as f:
            for uc in use_cases_dict:
                f.write(json.dumps(uc, ensure_ascii=False) + '\n')
        
        logger.info(f"Saved JSONL format to {jsonl_file}")


def main():
    """Main entry point"""
    processor = DataProcessor()
    use_cases = processor.process_all()
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 Processing Summary")
    print(f"{'='*60}")
    print(f"Total use cases extracted: {len(use_cases)}")
    
    # Count by tech type
    tech_counts = {}
    for uc in use_cases:
        for tech in uc.recommended_tech:
            tech_counts[tech] = tech_counts.get(tech, 0) + 1
    
    print(f"\nUse cases by technology:")
    for tech, count in sorted(tech_counts.items()):
        print(f"  {tech}: {count}")
    
    print(f"\n✅ Processing complete!")


if __name__ == '__main__':
    main()
