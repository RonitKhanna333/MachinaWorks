"""
Base scraper interface and utilities
"""
import time
import json
import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all scrapers"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.get('scraping_config', {}).get(
                'user_agent', 
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
        })
        self.timeout = config.get('scraping_config', {}).get('timeout', 30)
        self.retry_attempts = config.get('scraping_config', {}).get('retry_attempts', 3)
        self.delay = config.get('scraping_config', {}).get('delay_between_requests', 2)
    
    @abstractmethod
    def scrape(self, url: str) -> Dict:
        """Scrape content from a URL"""
        pass
    
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch HTML content with retry logic"""
        for attempt in range(self.retry_attempts):
            try:
                logger.info(f"Fetching {url} (attempt {attempt + 1}/{self.retry_attempts})")
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                time.sleep(self.delay)
                return response.text
            except requests.RequestException as e:
                logger.error(f"Error fetching {url}: {e}")
                if attempt == self.retry_attempts - 1:
                    return None
                time.sleep(self.delay * 2)
        return None
    
    def save_raw_data(self, data: Dict, output_dir: Path):
        """Save scraped data to JSON"""
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{data['source']}_{data['timestamp']}.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved data to {filepath}")


class StaticScraper(BaseScraper):
    """Scraper for static HTML pages"""
    
    def scrape(self, url: str) -> Dict:
        """Scrape content from static HTML"""
        html = self.fetch_page(url)
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract based on source configuration
        data = {
            'url': url,
            'source': self.config.get('name', 'unknown'),
            'category': self.config.get('category', 'general'),
            'timestamp': time.strftime('%Y%m%d_%H%M%S'),
            'content': {}
        }
        
        # Extract using configured selectors
        selectors = self.config.get('selectors', {})
        
        # Title
        title_selector = selectors.get('title', 'h1')
        title_elem = soup.select_one(title_selector)
        data['content']['title'] = title_elem.get_text(strip=True) if title_elem else ''
        
        # Main content
        content_selector = selectors.get('content', 'article, main')
        content_elem = soup.select_one(content_selector)
        
        if content_elem:
            # Extract paragraphs
            paragraphs = [p.get_text(strip=True) for p in content_elem.find_all('p')]
            data['content']['paragraphs'] = paragraphs
            
            # Extract headings with content
            sections = []
            for heading in content_elem.find_all(['h2', 'h3']):
                section = {
                    'heading': heading.get_text(strip=True),
                    'content': []
                }
                
                # Get content until next heading
                for sibling in heading.find_next_siblings():
                    if sibling.name in ['h2', 'h3']:
                        break
                    if sibling.name == 'p':
                        section['content'].append(sibling.get_text(strip=True))
                    elif sibling.name in ['ul', 'ol']:
                        items = [li.get_text(strip=True) for li in sibling.find_all('li')]
                        section['content'].extend(items)
                
                sections.append(section)
            
            data['content']['sections'] = sections
        
        # Extract based on patterns
        patterns = self.config.get('extract_patterns', {})
        extracted_patterns = {}
        
        for pattern_type, keywords in patterns.items():
            extracted_patterns[pattern_type] = []
            text = soup.get_text().lower()
            
            for keyword in keywords:
                if keyword.lower() in text:
                    # Find context around keyword
                    idx = text.find(keyword.lower())
                    context_start = max(0, idx - 200)
                    context_end = min(len(text), idx + 200)
                    context = text[context_start:context_end].strip()
                    extracted_patterns[pattern_type].append({
                        'keyword': keyword,
                        'context': context
                    })
        
        data['extracted_patterns'] = extracted_patterns
        
        return data


class DynamicScraper(BaseScraper):
    """Scraper for dynamic JavaScript-heavy pages using Playwright"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.playwright = None
        self.browser = None
    
    async def setup(self):
        """Initialize Playwright browser"""
        from playwright.async_api import async_playwright
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True
        )
    
    async def teardown(self):
        """Close browser and Playwright"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def scrape(self, url: str) -> Dict:
        """Scrape content from dynamic page"""
        page = await self.browser.new_page()
        
        try:
            logger.info(f"Loading dynamic page: {url}")
            await page.goto(url, wait_until='networkidle', timeout=self.timeout * 1000)
            
            # Wait for content to load
            await page.wait_for_timeout(3000)
            
            # Get page content
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            data = {
                'url': url,
                'source': self.config.get('name', 'unknown'),
                'category': self.config.get('category', 'general'),
                'timestamp': time.strftime('%Y%m%d_%H%M%S'),
                'content': {}
            }
            
            # Extract using configured selectors
            selectors = self.config.get('selectors', {})
            
            # Title
            title_selector = selectors.get('title', 'h1')
            title_elem = soup.select_one(title_selector)
            data['content']['title'] = title_elem.get_text(strip=True) if title_elem else ''
            
            # Main content sections
            sections = []
            for elem in soup.select('section, article, div.content'):
                heading = elem.find(['h1', 'h2', 'h3'])
                if heading:
                    section = {
                        'heading': heading.get_text(strip=True),
                        'content': [p.get_text(strip=True) for p in elem.find_all('p')]
                    }
                    sections.append(section)
            
            data['content']['sections'] = sections
            
            return data
            
        finally:
            await page.close()


def create_scraper(source_config: Dict) -> BaseScraper:
    """Factory function to create appropriate scraper"""
    strategy = source_config.get('scraping_strategy', 'static')
    
    if strategy == 'static':
        return StaticScraper(source_config)
    elif strategy == 'dynamic':
        return DynamicScraper(source_config)
    elif strategy == 'api':
        # Will implement API scraper separately
        raise NotImplementedError("API scraper not yet implemented")
    else:
        raise ValueError(f"Unknown scraping strategy: {strategy}")
