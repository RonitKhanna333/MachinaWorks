"""
Main scraping orchestrator
"""
import json
import asyncio
from pathlib import Path
from typing import List, Dict
import logging

from base_scraper import create_scraper, StaticScraper, DynamicScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScraperOrchestrator:
    """Orchestrates scraping across multiple sources"""
    
    def __init__(self, config_path: str = "configs/sources.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.output_dir = Path("data/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def scrape_priority_sources(self):
        """Scrape only priority sources (minimal set)"""
        priority_sources = self.config['priority_sources']
        logger.info(f"Scraping {len(priority_sources)} priority sources")
        
        for source_config in priority_sources:
            self._scrape_source(source_config)
    
    def scrape_all_sources(self):
        """Scrape all sources (priority + extended)"""
        all_sources = self.config['priority_sources'] + self.config['extended_sources']
        logger.info(f"Scraping {len(all_sources)} total sources")
        
        for source_config in all_sources:
            self._scrape_source(source_config)
    
    def _scrape_source(self, source_config: Dict):
        """Scrape a single source"""
        source_name = source_config['name']
        logger.info(f"\n{'='*60}\nScraping: {source_name}\n{'='*60}")
        
        strategy = source_config.get('scraping_strategy', 'static')
        
        if strategy == 'static':
            self._scrape_static(source_config)
        elif strategy == 'dynamic':
            asyncio.run(self._scrape_dynamic(source_config))
        elif strategy == 'api':
            self._scrape_api(source_config)
    
    def _scrape_static(self, source_config: Dict):
        """Scrape static pages"""
        scraper = StaticScraper({**source_config, **self.config})
        urls = source_config.get('urls', [])
        
        for url in urls:
            try:
                data = scraper.scrape(url)
                if data:
                    scraper.save_raw_data(data, self.output_dir / source_config['name'].replace(' ', '_'))
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
    
    async def _scrape_dynamic(self, source_config: Dict):
        """Scrape dynamic pages"""
        scraper = DynamicScraper({**source_config, **self.config})
        await scraper.setup()
        
        try:
            urls = source_config.get('urls', [])
            for url in urls:
                try:
                    data = await scraper.scrape(url)
                    if data:
                        scraper.save_raw_data(data, self.output_dir / source_config['name'].replace(' ', '_'))
                except Exception as e:
                    logger.error(f"Error scraping {url}: {e}")
        finally:
            await scraper.teardown()
    
    def _scrape_api(self, source_config: Dict):
        """Scrape via API (e.g., Hugging Face)"""
        import requests
        
        api_endpoint = source_config.get('api_endpoint')
        if not api_endpoint:
            logger.warning(f"No API endpoint configured for {source_config['name']}")
            return
        
        try:
            logger.info(f"Fetching from API: {api_endpoint}")
            response = requests.get(api_endpoint, timeout=30)
            response.raise_for_status()
            
            data = {
                'source': source_config['name'],
                'category': source_config['category'],
                'api_response': response.json()
            }
            
            output_file = self.output_dir / source_config['name'].replace(' ', '_') / 'api_data.json'
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved API data to {output_file}")
            
        except Exception as e:
            logger.error(f"Error fetching API data: {e}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Consultation Bot - Web Scraper')
    parser.add_argument(
        '--mode',
        choices=['priority', 'all'],
        default='priority',
        help='Scrape priority sources only or all sources'
    )
    parser.add_argument(
        '--config',
        default='configs/sources.json',
        help='Path to sources configuration file'
    )
    
    args = parser.parse_args()
    
    orchestrator = ScraperOrchestrator(args.config)
    
    if args.mode == 'priority':
        orchestrator.scrape_priority_sources()
    else:
        orchestrator.scrape_all_sources()
    
    logger.info("\n✅ Scraping complete!")


if __name__ == '__main__':
    main()
