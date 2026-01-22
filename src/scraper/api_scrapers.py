"""
API-specific scrapers for structured data sources
"""
import requests
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class HuggingFaceScraper:
    """Scraper for Hugging Face model catalog"""
    
    def __init__(self):
        self.base_url = "https://huggingface.co/api"
    
    def scrape_tasks(self) -> List[Dict]:
        """Get all tasks and their associated models"""
        tasks_url = f"{self.base_url}/tasks"
        
        try:
            response = requests.get(tasks_url, timeout=30)
            response.raise_for_status()
            tasks_data = response.json()
            
            logger.info(f"Fetched {len(tasks_data)} tasks from Hugging Face")
            return tasks_data
            
        except Exception as e:
            logger.error(f"Error fetching HF tasks: {e}")
            return []
    
    def scrape_models_for_task(self, task: str, limit: int = 20) -> List[Dict]:
        """Get top models for a specific task"""
        models_url = f"{self.base_url}/models"
        params = {
            'filter': f'task:{task}',
            'sort': 'downloads',
            'limit': limit
        }
        
        try:
            response = requests.get(models_url, params=params, timeout=30)
            response.raise_for_status()
            models = response.json()
            
            logger.info(f"Fetched {len(models)} models for task: {task}")
            return models
            
        except Exception as e:
            logger.error(f"Error fetching models for {task}: {e}")
            return []
    
    def extract_model_capabilities(self, model_id: str) -> Dict:
        """Extract detailed information about a model"""
        model_url = f"https://huggingface.co/{model_id}"
        
        try:
            # Get model card
            card_url = f"https://huggingface.co/{model_id}/raw/main/README.md"
            response = requests.get(card_url, timeout=30)
            
            if response.status_code == 200:
                readme = response.text
                
                # Extract key sections
                capability = {
                    'model_id': model_id,
                    'description': self._extract_section(readme, 'description'),
                    'use_cases': self._extract_section(readme, 'intended uses'),
                    'limitations': self._extract_section(readme, 'limitations'),
                    'training_data': self._extract_section(readme, 'training data')
                }
                
                return capability
            
        except Exception as e:
            logger.error(f"Error extracting model capabilities for {model_id}: {e}")
        
        return {}
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract content under a specific section heading"""
        lines = text.split('\n')
        section_content = []
        in_section = False
        
        for line in lines:
            if section_name.lower() in line.lower() and line.startswith('#'):
                in_section = True
                continue
            
            if in_section:
                if line.startswith('#'):
                    break
                section_content.append(line)
        
        return '\n'.join(section_content).strip()


class PapersWithCodeScraper:
    """Scraper for Papers with Code (optional, advanced)"""
    
    def __init__(self):
        self.base_url = "https://paperswithcode.com/api/v1"
    
    def scrape_sota_methods(self, task: str) -> List[Dict]:
        """Get state-of-the-art methods for a task"""
        # Implementation depends on Papers with Code API availability
        pass
