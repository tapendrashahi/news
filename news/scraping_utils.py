"""
Web Scraping Utilities for News Articles
Uses BeautifulSoup and requests for article extraction
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from datetime import datetime
from django.utils import timezone
import re

logger = logging.getLogger(__name__)


class NewsArticleScraper:
    """Scraper for extracting news articles from websites"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timeout = 15
        
    def scrape_article_from_url(self, url):
        """
        Extract article content from a given URL.
        
        Args:
            url (str): The URL of the article
            
        Returns:
            dict: Article data or None if failed
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract title
            title = self._extract_title(soup)
            
            # Extract main content
            content = self._extract_content(soup)
            
            # Extract images
            images = self._extract_images(soup, url)
            
            # Extract author
            author = self._extract_author(soup)
            
            # Extract publish date
            publish_date = self._extract_date(soup)
            
            # Create summary (first 500 chars of content)
            summary = content[:500] + "..." if len(content) > 500 else content
            
            return {
                'title': title,
                'content': content,
                'summary': summary,
                'source_url': url,
                'source_website': urlparse(url).netloc,
                'author': author,
                'published_date': publish_date,
                'image_urls': images[:5],  # Limit to 5 images
            }
            
        except Exception as e:
            logger.error(f"Error scraping article from {url}: {str(e)}")
            return None
    
    def _extract_title(self, soup):
        """Extract article title"""
        # Try multiple selectors
        title_selectors = [
            ('meta', {'property': 'og:title'}),
            ('meta', {'name': 'twitter:title'}),
            'h1',
            'title'
        ]
        
        for selector in title_selectors:
            if isinstance(selector, tuple):
                tag, attrs = selector
                element = soup.find(tag, attrs)
                if element:
                    return element.get('content', '').strip()
            else:
                element = soup.find(selector)
                if element:
                    return element.get_text().strip()
        
        return 'Untitled Article'
    
    def _extract_content(self, soup):
        """Extract main article content"""
        # Try to find article content
        content_selectors = [
            ('article',),
            ('div', {'class': re.compile(r'(article|content|post|entry)', re.I)}),
            ('div', {'id': re.compile(r'(article|content|post|entry)', re.I)}),
            ('main',),
        ]
        
        for selector in content_selectors:
            tag = selector[0]
            attrs = selector[1] if len(selector) > 1 else {}
            element = soup.find(tag, attrs)
            
            if element:
                # Get all paragraphs
                paragraphs = element.find_all('p')
                if paragraphs:
                    text = ' '.join([p.get_text().strip() for p in paragraphs])
                    if len(text) > 200:  # Minimum content length
                        return text
        
        # Fallback: get all paragraphs
        all_paragraphs = soup.find_all('p')
        return ' '.join([p.get_text().strip() for p in all_paragraphs[:10]])
    
    def _extract_images(self, soup, base_url):
        """Extract article images"""
        images = []
        
        # Try og:image first
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            images.append(urljoin(base_url, og_image['content']))
        
        # Find img tags in article
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src and not src.startswith('data:'):
                full_url = urljoin(base_url, src)
                if full_url not in images:
                    images.append(full_url)
        
        return images
    
    def _extract_author(self, soup):
        """Extract article author"""
        author_selectors = [
            ('meta', {'name': 'author'}),
            ('meta', {'property': 'article:author'}),
            ('span', {'class': re.compile(r'author', re.I)}),
            ('a', {'rel': 'author'}),
        ]
        
        for selector in author_selectors:
            tag, attrs = selector
            element = soup.find(tag, attrs)
            if element:
                return element.get('content') or element.get_text().strip() or 'Unknown'
        
        return 'Unknown'
    
    def _extract_date(self, soup):
        """Extract publish date"""
        date_selectors = [
            ('meta', {'property': 'article:published_time'}),
            ('meta', {'name': 'publish_date'}),
            ('time', {}),
        ]
        
        for selector in date_selectors:
            tag, attrs = selector
            element = soup.find(tag, attrs)
            if element:
                date_str = element.get('content') or element.get('datetime') or element.get_text()
                try:
                    # Try to parse ISO format
                    parsed_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    if parsed_date.tzinfo is None:
                        parsed_date = timezone.make_aware(parsed_date)
                    return parsed_date
                except:
                    pass
        
        return timezone.now()
    
    def _extract_keywords(self, content):
        """Extract keywords from content"""
        # Simple keyword extraction: get most common meaningful words
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
        # Remove common stop words
        stop_words = {'that', 'this', 'with', 'from', 'have', 'been', 'were', 'will', 'would', 'could', 'should'}
        keywords = [w for w in words if w not in stop_words]
        # Get unique keywords
        unique_keywords = list(dict.fromkeys(keywords))[:10]
        return unique_keywords
    
    def search_website_for_keyword(self, website_url, keyword, max_results=5):
        """
        Search a website for articles containing a keyword.
        
        Args:
            website_url (str): Base URL of the website
            keyword (str): Keyword to search for
            max_results (int): Maximum number of articles to return
            
        Returns:
            list: List of article URLs found
        """
        article_urls = []
        
        try:
            # Try common search patterns
            search_urls = [
                f"{website_url}/search?q={keyword}",
                f"{website_url}/search/{keyword}",
                f"{website_url}/?s={keyword}",
                f"{website_url}",  # Fallback to homepage
            ]
            
            for search_url in search_urls:
                try:
                    response = requests.get(
                        search_url,
                        headers=self.headers,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Find article links (common patterns)
                        links = soup.find_all('a', href=True)
                        
                        for link in links:
                            href = link.get('href')
                            
                            # Convert relative URLs to absolute
                            if href:
                                full_url = urljoin(website_url, href)
                                
                                # Filter for article-like URLs
                                if self._is_article_url(full_url) and full_url not in article_urls:
                                    # Check if link text or title contains keyword
                                    link_text = link.get_text().lower()
                                    if keyword.lower() in link_text or keyword.lower() in href.lower():
                                        article_urls.append(full_url)
                                        
                                        if len(article_urls) >= max_results:
                                            return article_urls
                        
                        # If we found articles, break
                        if article_urls:
                            break
                            
                except Exception as e:
                    logger.debug(f"Failed to search {search_url}: {str(e)}")
                    continue
            
            # If no articles found through search, scrape homepage for recent articles
            if not article_urls:
                article_urls = self._scrape_homepage_articles(website_url, max_results)
                
        except Exception as e:
            logger.error(f"Error searching {website_url} for '{keyword}': {str(e)}")
        
        return article_urls[:max_results]
    
    def _scrape_homepage_articles(self, website_url, max_results=5):
        """Scrape recent articles from website homepage"""
        article_urls = []
        
        try:
            response = requests.get(
                website_url,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a', href=True)
                
                for link in links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(website_url, href)
                        if self._is_article_url(full_url) and full_url not in article_urls:
                            article_urls.append(full_url)
                            if len(article_urls) >= max_results:
                                break
                                
        except Exception as e:
            logger.error(f"Error scraping homepage {website_url}: {str(e)}")
        
        return article_urls
    
    def _is_article_url(self, url):
        """Check if URL looks like an article"""
        # Exclude common non-article patterns
        exclude_patterns = [
            '/tag/', '/category/', '/author/', '/page/',
            '/wp-content/', '/wp-includes/', '/static/',
            '/assets/', '/images/', '/css/', '/js/',
            '/login', '/register', '/search', '/contact',
            '.jpg', '.png', '.gif', '.pdf', '.xml', '.json'
        ]
        
        url_lower = url.lower()
        
        # Exclude if matches exclude patterns
        if any(pattern in url_lower for pattern in exclude_patterns):
            return False
        
        # Include if matches common article patterns
        include_patterns = [
            '/article/', '/news/', '/post/', '/blog/',
            '/story/', '/2024/', '/2025/',  # Year in URL often indicates article
        ]
        
        if any(pattern in url_lower for pattern in include_patterns):
            return True
        
        # Check URL structure (articles often have multiple path segments)
        path = urlparse(url).path
        segments = [s for s in path.split('/') if s]
        
        # Articles usually have 2+ path segments and some meaningful length
        return len(segments) >= 2 and len(path) > 20


def scrape_articles_for_config(config):
    """
    Scrape articles based on a NewsSourceConfig.
    OPTIMIZED: Scrapes homepage articles only, then filters by keywords.
    This is MUCH faster than searching for each keyword individually.
    
    Args:
        config: NewsSourceConfig instance
        
    Returns:
        list: List of scraped article data dictionaries
    """
    scraper = NewsArticleScraper()
    scraped_articles = []
    seen_urls = set()  # Track unique URLs
    
    # Limit websites to prevent timeout (120s max)
    websites_to_use = config.source_websites[:10] if len(config.source_websites) > 10 else config.source_websites
    
    # Convert keywords to lowercase for matching
    keywords_lower = [kw.lower() for kw in config.keywords]
    
    logger.info(f"🚀 FAST SCRAPE: {len(websites_to_use)} websites, filtering by {len(keywords_lower)} keywords")
    
    # Process each website (limited list)
    for idx, website in enumerate(websites_to_use, 1):
        # Ensure URL has a scheme
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        
        try:
            logger.info(f"[{idx}/{len(websites_to_use)}] Scraping homepage: {website}")
            
            # FAST APPROACH: Get recent articles from homepage directly (no search!)
            article_urls = scraper._scrape_homepage_articles(website, max_results=10)
            
            if not article_urls:
                logger.warning(f"No articles found on {website}")
                continue
            
            # Extract content and filter by keywords
            for url in article_urls:
                if url in seen_urls:
                    continue
                
                seen_urls.add(url)
                    
                try:
                    article_data = scraper.scrape_article_from_url(url)
                    
                    if article_data and len(article_data.get('content', '')) > 200:
                        # Check if article matches ANY keyword
                        matched = []
                        content_lower = article_data['content'].lower()
                        title_lower = article_data['title'].lower()
                        
                        for keyword in keywords_lower:
                            if keyword in content_lower or keyword in title_lower:
                                matched.append(keyword)
                        
                        # Only save if matches at least one keyword
                        if matched:
                            article_data['matched_keywords'] = matched
                            article_data['category'] = config.category
                            article_data['reference_urls'] = []
                            
                            scraped_articles.append(article_data)
                            logger.info(f"✅ Found: {article_data['title'][:50]}... (keywords: {', '.join(matched[:3])})")
                            
                            # Stop if we've reached max articles
                            if len(scraped_articles) >= config.max_articles_per_scrape:
                                logger.info(f"🎯 Reached max: {config.max_articles_per_scrape} articles")
                                return scraped_articles
                        else:
                            logger.debug(f"⏭️  Skipped (no match): {article_data['title'][:50]}...")
                            
                except Exception as e:
                    logger.error(f"Error extracting article from {url}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error processing website {website}: {str(e)}")
            continue
    
    logger.info(f"Batch scrape completed: {len(scraped_articles)} articles found")
    return scraped_articles
