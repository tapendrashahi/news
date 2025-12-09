"""
Research Agent

Implements web search and news gathering functionality using:
- Serper API for Google search
- NewsAPI for news articles
- GNews API for additional news sources
"""

import os
import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ResearchAgent:
    """
    Agent responsible for researching topics using multiple data sources.
    
    Features:
    - Web search via Serper API (Google Search)
    - News articles via NewsAPI and GNews
    - Source credibility scoring
    - Quote and fact extraction
    """
    
    def __init__(self):
        """Initialize research agent with API credentials."""
        self.serper_api_key = os.getenv('SERPER_API_KEY')
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.gnews_api_key = os.getenv('GNEWS_API_KEY')
        
        # Validate API keys
        if not self.serper_api_key:
            logger.warning("SERPER_API_KEY not found in environment")
        if not self.newsapi_key:
            logger.warning("NEWSAPI_KEY not found in environment")
        if not self.gnews_api_key:
            logger.warning("GNEWS_API_KEY not found in environment")
        
        # Credibility scores for news sources (0-100)
        self.source_credibility = {
            'reuters.com': 95,
            'apnews.com': 95,
            'bbc.com': 90,
            'nytimes.com': 85,
            'theguardian.com': 85,
            'washingtonpost.com': 85,
            'wsj.com': 85,
            'economist.com': 85,
            'ft.com': 85,
            'bloomberg.com': 85,
            'cnbc.com': 80,
            'cnn.com': 75,
            'foxnews.com': 70,
            'default': 60
        }
    
    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return ''
    
    def _calculate_credibility(self, url: str) -> int:
        """Calculate credibility score for a source URL."""
        domain = self._get_domain(url)
        return self.source_credibility.get(domain, self.source_credibility['default'])
    
    def search_web(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search the web using Serper API (Google Search).
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with title, link, snippet
        """
        if not self.serper_api_key:
            logger.warning("Serper API key not available, skipping web search")
            return []
        
        try:
            url = "https://google.serper.dev/search"
            headers = {
                'X-API-KEY': self.serper_api_key,
                'Content-Type': 'application/json'
            }
            payload = {
                'q': query,
                'num': num_results
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get('organic', []):
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'source': self._get_domain(item.get('link', '')),
                    'credibility': self._calculate_credibility(item.get('link', '')),
                    'type': 'web_search'
                })
            
            logger.info(f"Serper search returned {len(results)} results for: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Serper API error: {e}")
            return []
    
    def search_news_newsapi(self, query: str, days_back: int = 7) -> List[Dict[str, Any]]:
        """
        Search news using NewsAPI.
        
        Args:
            query: Search query
            days_back: How many days back to search
            
        Returns:
            List of news articles
        """
        if not self.newsapi_key:
            logger.warning("NewsAPI key not available, skipping NewsAPI search")
            return []
        
        try:
            url = "https://newsapi.org/v2/everything"
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            params = {
                'q': query,
                'from': from_date,
                'sortBy': 'relevancy',
                'language': 'en',
                'pageSize': 20,
                'apiKey': self.newsapi_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for article in data.get('articles', []):
                url = article.get('url', '')
                results.append({
                    'title': article.get('title', ''),
                    'url': url,
                    'snippet': article.get('description', ''),
                    'content': article.get('content', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'author': article.get('author', ''),
                    'published_at': article.get('publishedAt', ''),
                    'image_url': article.get('urlToImage', ''),
                    'credibility': self._calculate_credibility(url),
                    'type': 'newsapi'
                })
            
            logger.info(f"NewsAPI returned {len(results)} articles for: {query}")
            return results
            
        except Exception as e:
            logger.error(f"NewsAPI error: {e}")
            return []
    
    def search_news_gnews(self, query: str, max_articles: int = 10) -> List[Dict[str, Any]]:
        """
        Search news using GNews API.
        
        Args:
            query: Search query
            max_articles: Maximum number of articles to return
            
        Returns:
            List of news articles
        """
        if not self.gnews_api_key:
            logger.warning("GNews API key not available, skipping GNews search")
            return []
        
        try:
            url = "https://gnews.io/api/v4/search"
            params = {
                'q': query,
                'lang': 'en',
                'max': max_articles,
                'apikey': self.gnews_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for article in data.get('articles', []):
                url = article.get('url', '')
                results.append({
                    'title': article.get('title', ''),
                    'url': url,
                    'snippet': article.get('description', ''),
                    'content': article.get('content', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'published_at': article.get('publishedAt', ''),
                    'image_url': article.get('image', ''),
                    'credibility': self._calculate_credibility(url),
                    'type': 'gnews'
                })
            
            logger.info(f"GNews returned {len(results)} articles for: {query}")
            return results
            
        except Exception as e:
            logger.error(f"GNews API error: {e}")
            return []
    
    def collect_references(self, keyword: str, max_sources: int = 20) -> Dict[str, Any]:
        """
        Collect comprehensive research data from multiple sources.
        
        Args:
            keyword: Topic to research
            max_sources: Maximum number of sources to collect
            
        Returns:
            Dictionary containing all research data
        """
        logger.info(f"Collecting references for: {keyword}")
        
        all_sources = []
        
        # 1. Web search via Serper
        web_results = self.search_web(keyword, num_results=10)
        all_sources.extend(web_results)
        
        # 2. News via NewsAPI
        newsapi_results = self.search_news_newsapi(keyword, days_back=30)
        all_sources.extend(newsapi_results)
        
        # 3. News via GNews
        gnews_results = self.search_news_gnews(keyword, max_articles=10)
        all_sources.extend(gnews_results)
        
        # Sort by credibility and limit
        all_sources.sort(key=lambda x: x.get('credibility', 0), reverse=True)
        all_sources = all_sources[:max_sources]
        
        # Extract statistics and quotes
        statistics = self._extract_statistics(all_sources)
        quotes = self._extract_quotes(all_sources)
        perspectives = self._identify_perspectives(all_sources)
        
        research_data = {
            'sources': all_sources,
            'source_count': len(all_sources),
            'statistics': statistics,
            'quotes': quotes,
            'perspectives': perspectives,
            'credibility_avg': sum(s.get('credibility', 0) for s in all_sources) / len(all_sources) if all_sources else 0,
            'last_updated': datetime.now().isoformat(),
            'api_usage': {
                'serper': len(web_results),
                'newsapi': len(newsapi_results),
                'gnews': len(gnews_results)
            }
        }
        
        logger.info(f"Research complete: {len(all_sources)} sources collected (avg credibility: {research_data['credibility_avg']:.1f})")
        
        return research_data
    
    def _extract_statistics(self, sources: List[Dict]) -> List[Dict[str, str]]:
        """Extract statistical data from source snippets."""
        statistics = []
        
        # Look for numbers and percentages in snippets
        import re
        number_pattern = r'\b\d+(?:,\d{3})*(?:\.\d+)?%?\b'
        
        for source in sources[:10]:  # Check first 10 sources
            snippet = source.get('snippet', '') + ' ' + source.get('content', '')
            numbers = re.findall(number_pattern, snippet)
            
            if numbers:
                statistics.append({
                    'value': ', '.join(numbers[:3]),  # First 3 numbers
                    'context': snippet[:200],
                    'source': source.get('source', ''),
                    'url': source.get('url', '')
                })
        
        return statistics[:5]  # Return top 5
    
    def _extract_quotes(self, sources: List[Dict]) -> List[Dict[str, str]]:
        """Extract potential quotes from source content."""
        quotes = []
        
        # Look for quoted text in snippets
        import re
        quote_pattern = r'"([^"]{20,200})"'
        
        for source in sources[:15]:
            content = source.get('snippet', '') + ' ' + source.get('content', '')
            found_quotes = re.findall(quote_pattern, content)
            
            for quote_text in found_quotes[:2]:  # Max 2 quotes per source
                quotes.append({
                    'text': quote_text,
                    'author': source.get('author', 'Unknown'),
                    'source': source.get('source', ''),
                    'url': source.get('url', ''),
                    'credibility': source.get('credibility', 60)
                })
        
        # Sort by credibility and limit
        quotes.sort(key=lambda x: x.get('credibility', 0), reverse=True)
        return quotes[:8]  # Return top 8 quotes
    
    def _identify_perspectives(self, sources: List[Dict]) -> List[str]:
        """Identify different perspectives/viewpoints from sources."""
        perspectives = []
        
        # Group sources by domain to identify different perspectives
        domain_groups = {}
        for source in sources:
            domain = source.get('source', 'unknown')
            if domain not in domain_groups:
                domain_groups[domain] = []
            domain_groups[domain].append(source)
        
        # Extract unique perspectives
        for domain, domain_sources in list(domain_groups.items())[:5]:
            snippet = domain_sources[0].get('snippet', '')
            if snippet:
                perspectives.append({
                    'source': domain,
                    'viewpoint': snippet[:150] + '...',
                    'credibility': domain_sources[0].get('credibility', 60),
                    'url': domain_sources[0].get('url', '')
                })
        
        return perspectives
